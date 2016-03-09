from django.test import TestCase
from tests.initialise import load_test_rules


class ValidateViews(TestCase):
    """Test templates Views"""
    @classmethod
    def setUpTestData(cls):
        load_test_rules()
    
    def test_validate_account_view_valid(self):
        response = self.client.post('/accounts/validate/', {'sort_code': '500000', 'account_number': '12312312'})
        assert response.status_code == 200
        assert 'Sort code' in response.content.decode(), response.content.decode()
        assert 'Account number' in response.content.decode(), response.content.decode()
        assert 'is a valid bank account' in response.content.decode(), response.content.decode()

    def test_validate_account_view_invalid(self):
        response = self.client.post('/accounts/validate/', {'sort_code': '500000', 'account_number': '12312313'})
        assert response.status_code == 200
        assert 'Sort code' in response.content.decode(), response.content.decode()
        assert 'Account number' in response.content.decode(), response.content.decode()
        assert 'Failed 1st Mod Check' in response.content.decode(), response.content.decode()

    def test_bulktest(self):
        response = self.client.post('/accounts/bulktest/', {'filename': 'vocalinkTests.txt'})
        assert response.status_code == 200
        assert 'Valid=True' in response.content.decode(), response.content.decode()
        assert 'Valid=False' in response.content.decode(), response.content.decode()
