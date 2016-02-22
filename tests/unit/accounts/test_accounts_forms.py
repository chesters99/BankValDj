from django.test import TestCase
from accounts.forms import *


class AccountsFormTests(TestCase):
    """Test Accounts forms"""

    def test_validateaccountform_valid(self):
        form_data = {'sort_code': '123123', 'account_number': '12312312'}
        form = ValidateAccountForm(data=form_data)
        assert form.is_valid(), form.errors.as_text()

    def test_validateaccountform_invalid_sort_code(self):
        form_data = {'sort_code': '12312X', 'account_number': '12312312'}
        form = ValidateAccountForm(data=form_data)
        assert not form.is_valid(), form.errors.as_text()
        assert 'Sort Code must be numeric' in form.errors.as_text()

        form_data = {'sort_code': '1231239', 'account_number': '12312312'}
        form = ValidateAccountForm(data=form_data)
        assert not form.is_valid(), form.errors.as_text()
        assert 'Ensure this value has' in form.errors.as_text()

    def test_validateaccountform_invalid_account_number(self):
        form_data = {'sort_code': '123123', 'account_number': '1231231X'}
        form = ValidateAccountForm(data=form_data)
        assert not form.is_valid(), form.errors.as_text()
        assert 'Account Number must be numeric' in form.errors.as_text()

        form_data = {'sort_code': '1231239', 'account_number': '12312312123123'}
        form = ValidateAccountForm(data=form_data)
        assert not form.is_valid(), form.errors.as_text()
        assert 'Ensure this value has' in form.errors.as_text()

    def test_bulktestform_valid(self):
        form_data = {'filename': 'testfile.txt'}
        form = BulkTestForm(data=form_data)
        assert form.is_valid(), form.errors.as_text()
