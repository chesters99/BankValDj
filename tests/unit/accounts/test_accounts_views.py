from tests.initialise import UnitTest


class ValidateViews(UnitTest):
    """Test templates Views"""

    def test_validate_account_view_valid(self):
        self.load_rules('500000')
        response = self.client.post('/en/accounts/validate/', {'sort_code': '500000', 'account_number': '12312312'})
        assert response.status_code == 200
        assert 'Sort code' in response.content.decode(), response.content.decode()
        assert 'Account number' in response.content.decode(), response.content.decode()
        assert 'is a valid bank account' in response.content.decode(), response.content.decode()

    def test_validate_account_view_invalid(self):
        self.load_rules('500000')
        response = self.client.post('/en/accounts/validate/', {'sort_code': '500000', 'account_number': '12312313'})
        assert response.status_code == 200
        assert 'Sort code' in response.content.decode(), response.content.decode()
        assert 'Account number' in response.content.decode(), response.content.decode()
        assert 'Failed 1st Mod Check' in response.content.decode(), response.content.decode()

    def test_bulktest(self):
        self.load_rules()
        response = self.client.post('/en/accounts/bulktest/', {'filename': 'vocalinkTests.txt'})
        assert response.status_code == 200
        assert 'Valid=True' in response.content.decode(), response.content.decode()
        assert 'Valid=False' in response.content.decode(), response.content.decode()
