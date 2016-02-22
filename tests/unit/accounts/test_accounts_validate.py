from django.test import TestCase
from accounts.utils.BankValidator import Validator


class AccountValidation(TestCase):
    fixtures = ['users.json','rules.json']

    def test_general_account_validation(self):
        bv = Validator()
        assert bv.validate('089999', '12345678901') is False
        assert bv.message == 'Invalid Account Number Length:11'
        assert bv.validate('0X9999', '12345678901') is False
        assert bv.message == 'Sort Code must be numeric:0X9999'
        assert bv.validate('09999', '12345678') is False
        assert bv.message == 'Sort Code must be 6 digits:09999'
        assert bv.validate('089999', '134567X') is False
        assert bv.message == 'Account Number must be numeric:134567X'
        assert bv.validate('089999', '123456') is False
        assert bv.validate('089999', '1234567') is False
        assert bv.validate('089999', '123456789') is False
        assert bv.validate('089999', '1234567890') is False
        assert bv.validate('086086', '1234567890') is True
        assert bv.validate('123123', '123123') is True
        assert bv.message == 'Warning:No Rule Found'

    def test_vocalink_supplied_tests(self):
        bv = Validator()
        assert bv.validate('089999', '66374958') is True
        assert bv.validate('107999', '88837491') is True
        assert bv.validate('202959', '63748472') is True
        assert bv.validate('871427', '46238510') is True
        assert bv.validate('872427', '46238510') is True
        assert bv.validate('871427', '09123496') is True
        assert bv.validate('871427', '99123496') is True
        assert bv.validate('820000', '73688637') is True
        assert bv.validate('827999', '73988638') is True
        assert bv.validate('827101', '28748352') is True
        assert bv.validate('134020', '63849203') is True
        assert bv.validate('118765', '64371389') is True
        assert bv.validate('200915', '41011166') is True
        assert bv.validate('938611', '07806039') is True
        assert bv.validate('938600', '42368003') is True
        assert bv.validate('938063', '55065200') is True
        assert bv.validate('772798', '99345694') is True
        assert bv.validate('086090', '06774744') is True
        assert bv.validate('309070', '02355688') is True
        assert bv.validate('309070', '12345668') is True
        assert bv.validate('309070', '12345677') is True
        assert bv.validate('309070', '99345694') is True
        assert bv.validate('938063', '15764273') is False
        assert bv.validate('938063', '15764264') is False
        assert bv.validate('938063', '15763217') is False
        assert bv.validate('118765', '64371388') is False
        assert bv.validate('203099', '66831036') is False
        assert bv.validate('203099', '58716970') is False
        assert bv.validate('089999', '66374959') is False
        assert bv.validate('107999', '88837493') is False
        assert bv.validate('074456', '12345112') is True
        assert bv.validate('070116', '34012583') is True
        assert bv.validate('074456', '11104102') is True
        assert bv.validate('180002', '00000190') is True
