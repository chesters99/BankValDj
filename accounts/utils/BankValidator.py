from math import floor
# from django.core.cache import cache

try: # setup database access either via Django or if run in batch then via psycopg2
    from rules.models import Rule # running under django
except ImportError:
    Rule=None # flag NOT running under django


class Validator:
    """ Contains all the logic and data to modulus check UK Bank Accounts"""
    MODULUS_10 = 'MOD10'
    MODULUS_11 = 'MOD11'
    DOUBLE_ALT = 'DBLAL'
    EXCEPTION5_OVERRIDE1 = (0, 0, 1, 2, 5, 3, 6, 4, 8, 7, 10, 9, 3, 1)
    EXCEPTION5_OVERRIDE2 = (0, 0, 0, 0, 0, 0, 0, 0, 8, 7, 10, 9, 3, 1)
    EXCEPTION5_TABLE = {
        '938173': '938017', '938620': '938343', '938289': '938068',
        '938622': '938130', '938297': '938076', '938628': '938181',
        '938600': '938611', '938643': '938246', '938602': '938343',
        '938647': '938611', '938604': '938603', '938648': '938246',
        '938608': '938408', '938649': '938394', '938609': '938424',
        '938651': '938335', '938613': '938017', '938653': '938424'}

    def __init__(self):
        """constructor initialises empty object"""
        self.message = None

    def _standardise(self, sort_code, account_number):
        """This function adjusts the sort code and account number formats

        :param sort_code: sort code
        :param account_number: account number
        :return: sort code and account number tuple
        """
        if not sort_code.isdigit():
            self.message = 'Sort Code must be numeric:' + sort_code
        elif len(sort_code) != 6:
            self.message = 'Sort Code must be 6 digits:' + sort_code
        elif not account_number.isdigit():
            self.message = 'Account Number must be numeric:' + account_number
        else:
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
                self.message = 'Invalid Account Number Length:' + str(len(account_number))
        return sort_code, account_number

    def _modulus_check(self, sort_code, account_number, rule):
        """Calculates the modulus and returns the remainder (failed if > 0)
        :param sort_code: sort code
        :param account_number: account number
        :param rule: rule to be applied
        :return: remainder
        """
        bank_account = sort_code + account_number
        if rule['mod_rule'] == self.MODULUS_11:
            remainder = sum([int(c) * rule['weight'][i] for i, c in enumerate(bank_account)]) % 11
            if rule['mod_exception'] == '4' and remainder == int(account_number[6:8]):
                remainder = 0
            elif rule['mod_exception'] == '5':
                if remainder == 0 and account_number[6] == '0':
                    pass  # valid account
                elif remainder == 11 - int(account_number[6]):
                    remainder = 0
                else:
                    remainder = 999

        elif rule['mod_rule'] == self.MODULUS_10:
            remainder = sum([int(c) * rule['weight'][i] for i, c in enumerate(bank_account)]) % 10

        elif rule['mod_rule'] == self.DOUBLE_ALT:
            total = 0
            for i, c in enumerate(bank_account):
                temp = int(c) * rule['weight'][i]
                total += temp % 10 + floor(temp / 10)
            total += 27 if rule['mod_exception'] == '1' else 0
            remainder = total % 10
            if rule['mod_exception'] == '5':
                if remainder == 0 and account_number[7] == '0':
                    pass
                elif remainder == 10 - int(account_number[7]):
                    remainder = 0
                else:
                    remainder = 999

        else:
            return -1  # invalid modulus rule - ie corrupt rule file
        return remainder


    def _get_rules(self, sort_code ): # caching not active as was 10% faster than postgres (use django-cacheops instead)
        # from django.core import serializers
        # DOES_NOT_EXIST = 'DoesNotExist'
        # cached_rules = cache.get(sort_code)
        # if cached_rules == DOES_NOT_EXIST:
        #     print('cache get DOES_NOT_EXIST')
        #     return {}
        # elif cached_rules is not None:
        #     rules = {}
        #     for i, obj in enumerate(serializers.deserialize("json", cached_rules)):
        #         rules[i]=obj.object
        #         print('cache get {start} {end}'.format(start=obj.object.start_sort, end=bj.object.mod_exception))
        # else:
        #     rules = Rule.objects.filter(start_sort__lte=sort_code, end_sort__gte=sort_code)
        #     if rules:
        #         data = serializers.serialize("json", rules)
        #         cache.set(sort_code, data)
        #         print('db get and cached {start}'.format(start=rules[0].start_sort)
        #     else:
        #         cache.set(sort_code, DOES_NOT_EXIST)
        #         print('db get doesnt exit - set cache does not exist')
        if Rule: # running under Django so use Django ORM
            rules = Rule.objects.filter(start_sort__lte=sort_code, end_sort__gte=sort_code).values()
        else:
            rules = []
            cursor.execute('SELECT * from rules_rule where start_sort <=%s and end_sort >=%s', (sort_code, sort_code))
            for row in cursor:
                rules.append(row)
        return rules


    def validate(self, sort_code, account_number):
        """ Perform modulus-based UK Bank Account validations

        :param sort_code: (*str*) : 6 characters
        :param account_number: (*str*) : 6-11 Characters
        :return: if account is valid then returns *True* and *self.message* = None (unless there is a warning).
                 if account is not valid then returns *False* and description in *self.message*
        """
        # Step 1 - Check sort code and account number are in correct format and adjust if possible
        self.message = None
        sort_code, account_number = self._standardise(sort_code, account_number)
        if self.message is not None:
            return False

        # Step 2 - Get the first and second applicable modulus templates
        # rules = Rule.objects.filter(start_sort__lte=sort_code, end_sort__gte=sort_code)
        rules = self._get_rules(sort_code)
        if not rules:
            self.message = "Warning:No Rules Found"
            return True # must assume ok if no applicable rules are found

        # Step 3 - Apply nasty exception handling overrides
        if rules[0]['mod_exception'] in ('2', '9'):
            if account_number[0] != '0' and account_number[6] != '9':
                rules[0]['weight'] = rules[1]['weight'] = self.EXCEPTION5_OVERRIDE1
            if account_number[0] != '0' and account_number[6] == '9':
                rules[0]['weight'] = rules[1]['weight'] = self.EXCEPTION5_OVERRIDE2
        if rules[0]['mod_exception'] == '5':
            if sort_code in self.EXCEPTION5_TABLE:
                sort_code = self.EXCEPTION5_TABLE[sort_code]
        if rules[0]['mod_exception'] == '6' and account_number[6] == account_number[7] \
                and account_number[0] in ('4', '5', '6', '7', '8'):
            return True  # cant templates so return as successful
        if rules[0]['mod_exception'] == '7' and account_number[6] == '9':
            for i in range(0, 8):
                rules[0]['weight'][i] = 0
        if rules[0]['mod_exception'] == '8':
            sort_code = '090126'
        if rules[0]['mod_exception'] == '10' and account_number[0:2] in ('09', '99') \
                and account_number[6] == '9':
            for i in range(0, 8):
                rules[0]['weight'][i] = 0

        # Step 4 - Perform 1st modulus check
        first_remainder = self._modulus_check(sort_code, account_number, rules[0])
        if first_remainder < 0:
            self.message = 'Invalid Modulus Rule'
            return False
        if first_remainder == 0:
            if rules[0]['mod_exception'] in ('2', '9', '10', '11', '12', '13', '14'):
                return True
            if len(rules) == 1:
                return True
            if rules[1]['mod_exception'] == '3' and account_number[2] in ('6', '9'):
                return True
            # need to perform 2nd check for some exceptions even if first check was ok
            second_remainder = self._modulus_check(sort_code, account_number, rules[1])
            if second_remainder < 0:
                self.message = 'Invalid Modulus Rule'
                return False
            if second_remainder == 0:
                return True
            else:
                self.message = 'Failed 2nd Mod Check after passing 1st'
                return False

        # Step 5 - if first check failed then see if second check may be required and perform it
        if first_remainder > 0:
            if rules[0]['mod_exception'] not in ('2', '9', '10', '11', '12', '13', '14'):
                self.message = 'Failed 1st Mod Check and no exceptions are available'
                return False
            else:
                try:
                    second_rule = rules[1]
                except (KeyError, IndexError):
                    second_rule = None

                if rules[0]['mod_exception'] in ('2', '9'):
                    sort_code = '309634'
                    second_rule = self._get_rules(sort_code)[0]

                if rules[0]['mod_exception'] == '14':
                    if account_number[7] not in ('0', '1', '9'):
                        self.message = 'Failed Exception Rule 14'
                        return False
                    else:
                        account_number = '0' + account_number[0:7]
                        second_rule = rules[0]

                if second_rule:  # if there is a second check then perform it
                    second_remainder = self._modulus_check(sort_code, account_number, second_rule)
                    if second_remainder < 0:
                        self.message = 'Invalid Modulus Rule'
                        return False
                else:
                    self.message = '2nd test required but no rule exists'
                    return False

                if second_remainder == 0:
                    return True
                else:
                    self.message = 'Failed 2nd Mod Check after failing 1st - exceptions 2,9,10,11,12,13,14'
                    return False
        return True

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        exit(sys.exit('must specify sort code and account number parameters'))
    p_sort_code = sys.argv[1]
    p_account_number = sys.argv[2]

    import psycopg2
    import psycopg2.extras
    try:
        database = psycopg2.connect("dbname='bankvaldj' user='django' host='localhost' password='bankvaldj'")
        cursor = database.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    except psycopg2.OperationalError:
        exit(sys.exit('psycopg2: Unable to connect to the database with rules table'))

    bv=Validator()
    result=bv.validate(p_sort_code, p_account_number)
    print('{sort}-{account} {result}'.format(sort=p_sort_code, account=p_account_number,
        result='Invalid Account - ' + bv.message if bv.message else 'Valid Account' ))
    if database:
        database.close()
    exit(sys.exit(0))
