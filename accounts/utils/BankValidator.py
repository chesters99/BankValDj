from math import floor

from rules.models import Rule


class RuleModel:
    """ The RuleModel class holds an array of the applicable templates for a sort
        code and a function to get these templates (__init__)"""

    def __init__(self, sort_code):
        """connect to database and return rule(s) for specified sort codes"""
        self.message = None
        self.rule = list({})
        if not (len(sort_code) == 6) or not (sort_code.isdigit()):
            self.message = "Sort Code must be 6 digits"
            return

        rules = Rule.objects.filter(start_sort__lte=sort_code, end_sort__gte=sort_code)
        if not any(rules):
            self.message = "Warning:No Rule Found"
            return

        for count, rule in enumerate(rules):
            self.rule.append({'start_sort': rule.start_sort, 'end_sort': rule.end_sort,
                              'mod_rule': rule.mod_rule, 'weight': list(), 'mod_exception': rule.mod_exception})
            self.rule[count]['weight'] = [rule.weight0, rule.weight1, rule.weight2, rule.weight3, rule.weight4,
                                          rule.weight5, rule.weight6, rule.weight7, rule.weight8, rule.weight9,
                                          rule.weight10, rule.weight11, rule.weight12, rule.weight13]


class BulkTestModel:
    """Class reads a list of test cases from a text file into a tuple called *test* """

    def __init__(self, filename):
        self.message = None
        try:
            self.test = [(line[0:6], line[7:15]) for line in open(filename, 'r')]
        except IOError as err:
            self.message = 'Cant open file. Error:' + str(err.strerror)
            return


class Validator:
    """ Contains all the logic and data to modulus check UK Bank Accounts"""
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
        account_number = account_number.replace('-', '')
        if not sort_code.isdigit():
            self.message = 'Sort Code must be numeric:' + sort_code
        elif len(sort_code) != 6:
            self.message = 'Sort Code must be 6 digits:' + sort_code
        elif not account_number.isdigit():
            self.message = 'Account Number must be numeric:' + account_number
        else:
            if len(account_number) == 6:
                account_number = '00' + account_number
            elif len(account_number) == 7:
                account_number = '0' + account_number
            elif len(account_number) == 8:
                pass
            elif len(account_number) == 9:
                sort_code = sort_code[0:5] + account_number[0]
                account_number = account_number[1:9]
            elif len(account_number) == 10:
                if sort_code == '086086':
                    account_number = account_number[0:8]
                else:
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
        total = 0
        for i in range(0, 14):
            temp = int((sort_code + account_number)[i]) * int(rule['weight'][i])
            if rule['mod_rule'] == Rule.DOUBLE_ALT:
                total += temp % 10 + floor(temp / 10)
            else:
                total += temp
        if rule['mod_exception'] == '1':
            total += 27

        if rule['mod_rule'] == Rule.DOUBLE_ALT:
            remainder = total % 10
            if rule['mod_exception'] == '5':
                if remainder == 0 and account_number[7] == '0':
                    pass
                elif remainder == 10 - int(account_number[7]):
                    remainder = 0
                else:
                    remainder = 999

        elif rule['mod_rule'] == Rule.MODULUS_10:
            remainder = total % 10

        elif rule['mod_rule'] == Rule.MODULUS_11:
            remainder = total % 11
            if rule['mod_exception'] == '4' and remainder == int(account_number[6:8]):
                remainder = 0
            elif rule['mod_exception'] == '5':
                if remainder == 0 and account_number[6] == '0':
                    pass  # valid account
                elif remainder == 11 - int(account_number[6]):
                    remainder = 0
                else:
                    remainder = 999
        else:
            remainder = -1  # invalid modulus rule - ie corrupt rule file
        return remainder

    def validate(self, sort_code, account_number):
        """ Perform modulus-based UK Bank Account validations

        :param sort_code: (*str*) : 6 characters
        :param account_number: (*str*) : 6-11 Characters
        :return: if account is valid then returns *True* and *self.message* = None (unless there is a warning).
                 if account is not valid then returns *False* and description in *self.message*
        """
        # Step 1 - Check sort code and account number are in correct format and adjust if possible
        self.message = None
        (sort_code, account_number) = self._standardise(sort_code, account_number)
        if self.message is not None:
            return False

        # Step 2 - Get the first and second applicable modulus templates
        r_model = RuleModel(sort_code)
        if r_model.message is not None:
            self.message = r_model.message
            return True  # if cant templates then must assume Bank Account is valid

        # Step 3 - Apply nasty exception handling overrides
        if r_model.rule[0]['mod_exception'] in ('2', '9'):
            if account_number[0] != '0' and account_number[6] != '9':
                r_model.rule[0]['weight'] = r_model.rule[1]['weight'] = self.EXCEPTION5_OVERRIDE1
            if account_number[0] != '0' and account_number[6] == '9':
                r_model.rule[0]['weight'] = r_model.rule[1]['weight'] = self.EXCEPTION5_OVERRIDE2
        if r_model.rule[0]['mod_exception'] == '5':
            if sort_code in self.EXCEPTION5_TABLE:
                sort_code = self.EXCEPTION5_TABLE[sort_code]
        if r_model.rule[0]['mod_exception'] == '6' and account_number[6] == account_number[7] \
                and account_number[0] in ('4', '5', '6', '7', '8'):
            return True  # cant templates so return as successful
        if r_model.rule[0]['mod_exception'] == '7' and account_number[6] == '9':
            for i in range(0, 8):
                r_model.rule[0]['weight'][i] = 0
        if r_model.rule[0]['mod_exception'] == '8':
            sort_code = '090126'
        if r_model.rule[0]['mod_exception'] == '10' and account_number[0:2] in ('09', '99') \
                and account_number[6] == '9':
            for i in range(0, 8):
                r_model.rule[0]['weight'][i] = 0

        # Step 4 - Perform 1st modulus check
        first_remainder = self._modulus_check(sort_code, account_number, r_model.rule[0])
        if first_remainder < 0:
            self.message = 'Invalid Modulus Rule'
            return False
        if first_remainder == 0:
            if r_model.rule[0]['mod_exception'] in ('2', '9', '10', '11', '12', '13', '14'):
                return True
            if len(r_model.rule) == 1:
                return True
            if r_model.rule[1]['mod_exception'] == '3' and account_number[2] in ('6', '9'):
                return True
            # need to perform 2nd check for some exceptions even if first check was ok
            second_remainder = self._modulus_check(sort_code, account_number, r_model.rule[1])
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
            if r_model.rule[0]['mod_exception'] not in ('2', '9', '10', '11', '12', '13', '14'):
                self.message = 'Failed 1st Mod Check and no exceptions are available'
                return False
            else:
                if r_model.rule[0]['mod_exception'] in ('2', '9'):
                    sort_code = '309634'
                    r_model = RuleModel(sort_code)
                    if r_model.message is not None:
                        self.message = r_model.message
                        return True  # if cant templates then must assume Bank Account is valid
                    r_model.rule.append(r_model.rule[0])

                if r_model.rule[0]['mod_exception'] == '14':
                    if account_number[7] not in ('0', '1', '9'):
                        self.message = 'Failed Exception Rule 14'
                        return False
                    else:
                        account_number = '0' + account_number[0:7]
                        r_model.rule.append(r_model.rule[0])

                if len(r_model.rule) > 1:  # if there is a second check then perform it
                    second_remainder = self._modulus_check(sort_code, account_number, r_model.rule[1])
                    if second_remainder < 0:
                        self.message = 'Invalid Modulus Rule'
                        return False
                else:
                    self.message = '2nd test required but no rule exists'
                    return

                if second_remainder == 0:
                    return True
                else:
                    self.message = 'Failed 2nd Mod Check after failing 1st with exceptions 2,9,10,11,12,13,14'
                    return False
        return True
