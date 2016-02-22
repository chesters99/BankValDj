from main.forms import *
from django.test import TestCase

class MainFormTests(TestCase):
    """Test templates forms"""

    def test_createuserform_valid(self):
        form_data = {'username': 'testuser', 'password': 'testpassword'}
        form = CreateUserForm(data=form_data)
        assert form.is_valid(), form.errors.as_text()

    def test_createuserform_invalid1(self):
        form_data = {'username': 'testu', 'password': 'testpassword'}
        form = CreateUserForm(data=form_data)
        assert not form.is_valid(), form.errors.as_text()
        assert 'Username must be more than 5 characters' in form.errors.as_text()

    def test_createuserform_invalid2(self):
        form_data = {'username': 'testuser', 'password': 'testp'}
        form = CreateUserForm(data=form_data)
        assert not form.is_valid(), form.errors.as_text()
        assert 'Password must be more than 5 characters' in form.errors.as_text()

    def test_createuserform_invalid3(self):
        form_data = {'username': 'testuser', 'password': 'testuser'}
        form = CreateUserForm(data=form_data)
        assert not form.is_valid(), form.errors.as_text()
        assert 'Username cannot be the same as password' in form.errors.as_text()
