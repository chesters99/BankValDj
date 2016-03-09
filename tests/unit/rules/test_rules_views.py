from django.test import TestCase
from rules.models import Rule
from tests.initialise import load_test_rules

class RulesViewTests(TestCase):
    """Test Rule Views"""

    @classmethod
    def setUpTestData(cls):
        load_test_rules()

    def login_as_superuser(self, client):
        response = client.post('/main/loginuser/', {'username': 'graham', 'password': 'testpass'})
        assert response.status_code == 302, response.status_code

    def test_search_rules_view(self):
        response = self.client.get('/rules/search/', {'q': '400000'})
        assert response.status_code == 200
        assert 'MOD11' in response.content.decode(), response.content.decode()
        assert 'DBLAL' in response.content.decode(), response.content.decode()

    def test_detail_view(self):
        self.login_as_superuser(self.client)
        rule = Rule.objects.filter(start_sort='400000')[:1].get()
        response = self.client.get('/rules/detail/%s/' % rule.id)
        assert response.status_code == 200
        assert 'Rule Detail' in response.content.decode(), response.content.decode()
        assert 'MOD11' in response.content.decode(), response.content.decode()

    def test_update_view(self):
        rule = Rule.objects.filter(start_sort='400000')[:1].get()
        self.login_as_superuser(self.client)

        response1 = self.client.post('/rules/update/%s/' % rule.id, {'mod_rule': 'DBLAL'})
        assert response1.status_code == 200
        assert 'Enter Rule' in response1.content.decode(), response1.content.decode()
        assert 'DBLAL' in response1.content.decode(), response1.content.decode()

        response2 = self.client.get('/rules/update/%s/' % rule.id)
        assert response2.status_code == 200
        assert 'Enter Rule' in response2.content.decode(), response2.content.decode()
        assert 'DBLAL' in response2.content.decode(), response2.content.decode()

    def test_delete_view(self):
        rule = Rule.objects.filter(start_sort='400000')[:1].get()
        self.login_as_superuser(self.client)

        response1 = self.client.get('/rules/delete/%s/' % rule.id)
        assert response1.status_code == 200
        assert 'Are you sure you want to delete' in response1.content.decode(), response1.content.decode()

        response2 = self.client.post('/rules/delete/%s/' % rule.id, follow=True)
        assert response2.status_code == 200
        assert 'Rule Deleted' in response2.content.decode(), response2.content.decode()

    def test_loadrules_view(self):
        self.login_as_superuser(self.client)
        response = self.client.post('/rules/load/', {'filename': 'valacdos.txt'})
        assert response.status_code == 200
        assert 'Rules loaded successfully' in response.content.decode(), response.content.decode()
