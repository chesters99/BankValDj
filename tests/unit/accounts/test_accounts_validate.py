from django.test import TestCase
from accounts.utils.BankValidator import Validator, BankValidationException
from tests.initialise import load_test_rules


class AccountValidation(TestCase):
    @classmethod
    def setUpTestData(cls):
        load_test_rules()

    def test_general_account_validation(self):
        bv = Validator()
        with self.assertRaisesRegexp(BankValidationException, 'Invalid Account Number Length'):
            bv.validate('089999', '12345678901')
        with self.assertRaisesRegexp(BankValidationException, 'Sort Code must be numeric'):
            bv.validate('0X9999', '12345678901')
        with self.assertRaisesRegexp(BankValidationException, 'Sort Code must be 6 digits'):
            bv.validate('09999', '12345678')
        with self.assertRaisesRegexp(BankValidationException, 'Account Number must be numeric'):
            bv.validate('089999', '134567X')
        with self.assertRaises(BankValidationException):
            bv.validate('089999', '123456')
        with self.assertRaises(BankValidationException):
            assert bv.validate('089999', '1234567')
        with self.assertRaises(BankValidationException):
            bv.validate('089999', '123456789')
        with self.assertRaises(BankValidationException):
            bv.validate('089999', '1234567890')


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
        with self.assertRaisesRegexp(BankValidationException, 'Failed 2nd Mod Check after passing 1st'):
            bv.validate('938063', '15764273')
        with self.assertRaisesRegexp(BankValidationException, 'Failed 1st Mod Check and no exceptions are available'):
            bv.validate('938063', '15764264')
        with self.assertRaisesRegexp(BankValidationException, 'Failed 1st Mod Check and no exceptions are available'):
            bv.validate('938063', '15763217')
        with self.assertRaisesRegexp(BankValidationException, 'Failed 1st Mod Check and no exceptions are available'):
            bv.validate('118765', '64371388')
        with self.assertRaisesRegexp(BankValidationException, 'Failed 2nd Mod Check after passing 1st'):
            bv.validate('203099', '66831036')
        with self.assertRaisesRegexp(BankValidationException, 'Failed 1st Mod Check and no exceptions are available'):
            bv.validate('203099', '58716970')
        with self.assertRaisesRegexp(BankValidationException, 'Failed 1st Mod Check and no exceptions are available'):
            bv.validate('089999', '66374959')
        with self.assertRaisesRegexp(BankValidationException, 'Failed 1st Mod Check and no exceptions are available'):
            bv.validate('107999', '88837493')
        assert bv.validate('074456', '12345112') is True
        assert bv.validate('070116', '34012583') is True
        assert bv.validate('074456', '11104102') is True
        assert bv.validate('180002', '00000190') is True
