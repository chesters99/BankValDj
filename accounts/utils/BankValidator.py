from math import floor
from django.core.cache import cache
from django.core import serializers
from django.core.exceptions import AppRegistryNotReady

try: # setup database access either via Django or if run in batch then via psycopg2
    from rules.models import Rule # running under django
except (ImportError, AppRegistryNotReady):
    Rule=None # flag NOT running under django

class BankValidationException(Exception):
    pass

class Validator:
    """ Contains all the logic and data to modulus check UK Bank Accounts
    """
    _CACHE = False # caching not active as was only 10% faster than postgres (use django-cacheops instead)
    _MODULUS_10 = 'MOD10'
    _MODULUS_11 = 'MOD11'
    _DOUBLE_ALT = 'DBLAL'
    _EXCEPTION5_OVERRIDE1 = (0, 0, 1, 2, 5, 3, 6, 4, 8, 7, 10, 9, 3, 1)
    _EXCEPTION5_OVERRIDE2 = (0, 0, 0, 0, 0, 0, 0, 0, 8, 7, 10, 9, 3, 1)
    _EXCEPTION5_TABLE = {
        '938173': '938017', '938620': '938343', '938289': '938068', '938622': '938130', '938297': '938076',
        '938628': '938181', '938600': '938611', '938643': '938246', '938602': '938343', '938647': '938611',
        '938604': '938603', '938648': '938246', '938608': '938408', '938649': '938394', '938609': '938424',
        '938651': '938335', '938613': '938017', '938653': '938424'}


    def _standardise(self, sort_code, account_number):
        """This function adjusts the sort code and account number formats
        :param sort_code: sort code
        :param account_number: account number
        :return: sort code and account number tuple
        """
        if not sort_code.isdigit():
            raise BankValidationException('Sort Code must be numeric')
        if len(sort_code) != 6:
            raise BankValidationException('Sort Code must be 6 digits')
        if not account_number.isdigit():
            raise BankValidationException('Account Number must be numeric')

        account_number_length = len(account_number)
        if account_number_length == 8:
            pass
        elif account_number_length == 6:
            account_number = '00' + account_number
        elif account_number_length == 7:
            account_number = '0' + account_number
        elif account_number_length == 9:
            sort_code = sort_code[0:5] + account_number[0]
            account_number = account_number[1:9]
        elif account_number_length == 10:
            if sort_code == '086086':
                account_number = account_number[0:8]  # Co-op Bank
            else:
                account_number = account_number.replace('-', '') # Natwest
                account_number = account_number[2:10]
        else:
            raise BankValidationException('Invalid Account Number Length:{0}'.format(len(account_number)))
        return sort_code, account_number

    def _modulus_check(self, sort_code, account_number, rule):
        """Calculates the modulus and returns the remainder (failed if > 0)
        :param sort_code: str - 6 chars
        :param account_number: str - 8 chars
        :param rule: dict - rule to be applied
        :return: remainder
        """
        bank_account = sort_code + account_number
        if rule['mod_rule'] == self._MODULUS_11:
            remainder = sum([int(c) * rule['weight'][i] for i, c in enumerate(bank_account)]) % 11
            if rule['mod_exception'] == '4' and remainder == int(account_number[6:8]):
                return 0
            elif rule['mod_exception'] == '5':
                if remainder == 0 and account_number[6] == '0':
                    return 0
                elif remainder == 11 - int(account_number[6]):
                    return 0
                else:
                    return 999

        elif rule['mod_rule'] == self._MODULUS_10:
            remainder = sum([int(c) * rule['weight'][i] for i, c in enumerate(bank_account)]) % 10

        elif rule['mod_rule'] == self._DOUBLE_ALT:
            total = 0
            for i, c in enumerate(bank_account):
                temp = int(c) * rule['weight'][i]
                total += temp % 10 + floor(temp / 10)
            total += 27 if rule['mod_exception'] == '1' else 0
            remainder = total % 10
            if rule['mod_exception'] == '5':
                if remainder == 0 and account_number[7] == '0':
                    return 0
                elif remainder == 10 - int(account_number[7]):
                    return 0
                else:
                    return 999

        else:
            raise BankValidationException('Invalid Modulus Rule')  # ie corrupt rule file
        return remainder


    def _get_rules(self, sort_code ):
        """ get rules from database or cache depending on class variable
        :param sort_code: str
        :rtype: rules as list[int][str]
        """
        def _get_rules_from_database(fsort_code):
            """ get rules from Django ORM or psycopg depending if run from command line or Django
            :param fsort_code: str
            :rtype: rules as list[int][str]
            """
            if Rule: # running under Django so use Django ORM, otherwise use psycopg2 direct access
                dbrules = Rule.objects.filter(start_sort__lte=fsort_code, end_sort__gte=fsort_code).values()
            else:
                dbrules = []
                cursor.execute('SELECT * from rules_rule where start_sort <=%s and end_sort >=%s', (fsort_code, fsort_code))
                for row in cursor:
                    rules.append(row)
            return dbrules

        if not self._CACHE:
            return _get_rules_from_database(sort_code)

        rule_does_not_exist = 'DoesNotExist'
        cached_rules = cache.get(sort_code)
        if cached_rules == rule_does_not_exist:
            print('cache get DOES_NOT_EXIST')
            return None
        elif cached_rules is not None:
            rules = {}
            for i, obj in enumerate(serializers.deserialize("json", cached_rules)):
                rules[i]=obj.object
                print('cache get {start} {end}'.format(start=obj.object['start_sort'], end=obj.object['end_sort']))
        else:
            rules = _get_rules_from_database(sort_code)
            if rules:
                data = serializers.serialize("json", rules)
                cache.set(sort_code, data)
                print('db get and cached {start}'.format(start=rules[0]['start_sort']))
            else:
                cache.set(sort_code, rule_does_not_exist)
                print('db get doesnt exit - set cache does not exist')
        return rules


    def validate(self, sort_code, account_number):
        """ Perform modulus-based UK Bank Account validations
        :param sort_code: (*str*) : 6 characters
        :param account_number: (*str*) : 6-11 Characters
        :return: if account is valid then returns *True*, if account cant be checked then returns *False* (ie still ok)
                 if account is not valid then raises BankValidation Exception
        """
        # Step 1 - Check sort code and account number are in correct format and adjust if possible
        sort_code, account_number = self._standardise(sort_code, account_number)

        # Step 2 - Get the first and second applicable modulus templates
        rules = self._get_rules(sort_code)
        if not rules:
            return False # must assume ok if no applicable rules are found, return False as a warning

        # Step 3 - Apply lots of nasty exception handling overrides
        if rules[0]['mod_exception'] in ('2', '9'):
            if account_number[0] != '0' and account_number[6] != '9':
                rules[0]['weight'] = rules[1]['weight'] = self._EXCEPTION5_OVERRIDE1
            if account_number[0] != '0' and account_number[6] == '9':
                rules[0]['weight'] = rules[1]['weight'] = self._EXCEPTION5_OVERRIDE2
        elif rules[0]['mod_exception'] == '5':
            sort_code = self._EXCEPTION5_TABLE.get(sort_code, sort_code)
        elif rules[0]['mod_exception'] == '6' and account_number[6] == account_number[7] and '4' <= account_number[0] <= '8':
            return True  # cant validate so return as successful
        elif rules[0]['mod_exception'] == '7' and account_number[6] == '9':
            rules[0]['weight'][:8] = [0] * 8
        elif rules[0]['mod_exception'] == '8':
            sort_code = '090126'
        elif rules[0]['mod_exception'] == '10' and account_number[0:2] in ('09', '99') and account_number[6] == '9':
            rules[0]['weight'][:8] = [0] * 8

        # Step 4 - Perform 1st modulus check
        if self._modulus_check(sort_code, account_number, rules[0]) == 0:
            if (rules[0]['mod_exception'] in ('2', '9', '10', '11', '12', '13', '14')) or \
               (len(rules) == 1) or \
               (rules[1]['mod_exception'] == '3' and account_number[2] in ('6', '9')):
                return True
            if self._modulus_check(sort_code, account_number, rules[1]) > 0: # need to perform 2nd check for some exceptions even if first check was ok
                raise BankValidationException('Failed 2nd Mod Check after passing 1st')
            return True

        # Step 5 - if first check failed then see if second check may be required and perform it
        else:
            if rules[0]['mod_exception'] not in ('2', '9', '10', '11', '12', '13', '14'):
                raise BankValidationException('Failed 1st Mod Check and no exceptions are available')
            else:
                if rules[0]['mod_exception'] in ('2', '9'):
                    sort_code = '309634'
                    second_rule = self._get_rules(sort_code)[0]
                elif rules[0]['mod_exception'] == '14':
                    if account_number[7] not in ('0', '1', '9'):
                        raise BankValidationException('Failed Exception Rule 14')
                    else:
                        account_number = '0' + account_number[0:7]
                        second_rule = rules[0]
                else:
                    try:
                        second_rule = rules[1]
                    except (KeyError, IndexError):
                        raise BankValidationException('2nd test required but no rule exists')
                if self._modulus_check(sort_code, account_number, second_rule) > 0:
                    raise BankValidationException('Failed 2nd Mod Check after failing 1st - exceps 2,9,10,11,12,13,14')
        return True

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        exit(sys.exit('must specify sort code and account number parameters'))
    p_sort_code = sys.argv[1]
    p_account_number = sys.argv[2]

    import psycopg2, psycopg2.extras
    try:
        database = psycopg2.connect("dbname='bankvaldj' user='django' host='localhost' password='bankvaldj'")
        cursor = database.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    except psycopg2.OperationalError:
        exit(sys.exit('psycopg2: Unable to connect to the database with rules table'))

    bv=Validator()
    try:
        bv.validate(p_sort_code, p_account_number)
        print('Valid Account')
    except BankValidationException as e:
        print('{sort}-{account} Invalid Bank Account- {result}'.format(sort=p_sort_code, account=p_account_number, result=e ))

    if database:
        database.close()
    exit(sys.exit(0))
