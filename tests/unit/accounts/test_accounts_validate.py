from django.test import TestCase
from accounts.utils.BankValidator import Validator, BankValidationException
from tests.initialise import load_test_rules


class AccountValidation(TestCase):
    @classmethod
    def setUpTestData(cls):
        load_test_rules()

    def test_general_account_validation(self):
        bv = Validator()
        self.assertRaisesRegexp(BankValidationException, 'Invalid Account Number Length', bv.validate, '089999', '12345678901')
        self.assertRaisesRegexp(BankValidationException, 'Sort Code must be numeric', bv.validate, '0X9999', '12345678901')
        self.assertRaisesRegexp(BankValidationException, 'Sort Code must be', bv.validate, '09999', '12345678')
        self.assertRaisesRegexp(BankValidationException, 'Account Number must be numeric', bv.validate, '089999', '134567X')
        self.assertRaises(BankValidationException, bv.validate, '089999', '123456')
        self.assertRaises(BankValidationException, bv.validate, '089999', '1234567')
        self.assertRaises(BankValidationException, bv.validate, '089999', '123456789')
        self.assertRaises(BankValidationException, bv.validate, '089999', '1234567890')


    def test_vocalink_supplied_tests(self):
        bv = Validator()
        self.assertTrue(bv.validate('089999', '66374958'))
        self.assertTrue(bv.validate('107999', '88837491'))
        self.assertTrue(bv.validate('202959', '63748472'))
        self.assertTrue(bv.validate('871427', '46238510'))
        self.assertTrue(bv.validate('872427', '46238510'))
        self.assertTrue(bv.validate('871427', '09123496'))
        self.assertTrue(bv.validate('871427', '99123496'))
        self.assertTrue(bv.validate('820000', '73688637'))
        self.assertTrue(bv.validate('827999', '73988638'))
        self.assertTrue(bv.validate('827101', '28748352'))
        self.assertTrue(bv.validate('134020', '63849203'))
        self.assertTrue(bv.validate('118765', '64371389'))
        self.assertTrue(bv.validate('200915', '41011166'))
        self.assertTrue(bv.validate('938611', '07806039'))
        self.assertTrue(bv.validate('938600', '42368003'))
        self.assertTrue(bv.validate('938063', '55065200'))
        self.assertTrue(bv.validate('772798', '99345694'))
        self.assertTrue(bv.validate('086090', '06774744'))
        self.assertTrue(bv.validate('309070', '02355688'))
        self.assertTrue(bv.validate('309070', '12345668'))
        self.assertTrue(bv.validate('309070', '12345677'))
        self.assertTrue(bv.validate('309070', '99345694'))
        self.assertRaisesRegexp(BankValidationException, 'Failed 2nd Mod Check', bv.validate, '938063', '15764273')
        self.assertRaisesRegexp(BankValidationException, 'Failed 1st Mod Check', bv.validate, '938063', '15764264')
        self.assertRaisesRegexp(BankValidationException, 'Failed 1st Mod Check', bv.validate, '938063', '15763217')
        self.assertRaisesRegexp(BankValidationException, 'Failed 1st Mod Check', bv.validate, '118765', '64371388')
        self.assertRaisesRegexp(BankValidationException, 'Failed 2nd Mod Check', bv.validate, '203099', '66831036')
        self.assertRaisesRegexp(BankValidationException, 'Failed 1st Mod Check', bv.validate, '203099', '58716970')
        self.assertRaisesRegexp(BankValidationException, 'Failed 1st Mod Check', bv.validate, '089999', '66374959')
        self.assertRaisesRegexp(BankValidationException, 'Failed 1st Mod Check', bv.validate, '107999', '88837493')
        self.assertTrue(bv.validate('074456', '12345112'))
        self.assertTrue(bv.validate('070116', '34012583'))
        self.assertTrue(bv.validate('074456', '11104102'))
        self.assertTrue(bv.validate('180002', '00000190'))
