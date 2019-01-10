from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rules.models import Rule
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.contrib.auth.models import User

from tests.initialise import load_test_rules


class ApisTests(TestCase):
    """Test APIs"""
    @classmethod
    def setUpTestData(cls):
        load_test_rules()

    def test_validate_api_valid(self):
        c = APIClient()
        response = c.get(reverse('apis:validate'), {'bank_account': '500000-12312312'})
        assert response.status_code == 200, response.status_code

    def test_validate_api_invalid(self):
        c = APIClient()
        response = c.get(reverse('apis:validate'), {'bank_account': '500000-12312313'})
        assert response.status_code == 406, response.status_code

    def test_get_rules_range(self):
        user = User.objects.first()
        c = APIClient()
        token, created = Token.objects.get_or_create(user=user)
        c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c.get(reverse('apis:rulelist'), {'start_sort': '300000', 'end_sort': '300050'})
        assert response.status_code == 200, response.status_code
        assert '300008' in response.content.decode()

    def test_get_a_rule(self):
        user = User.objects.first()
        rule = Rule.objects.first()
        c = APIClient()
        token, created = Token.objects.get_or_create(user=user)
        c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c.get(reverse('apis:rule', kwargs={'pk': rule.id}))
        assert response.status_code == 200, response.status_code
        assert rule.start_sort in response.content.decode()

    def test_update_a_rule(self):
        user = User.objects.first()
        rule_id = Rule.objects.first().id
        c = APIClient()
        token, created = Token.objects.get_or_create(user=user)
        c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c.put(reverse('apis:rule', kwargs={'pk': rule_id}),
                         {'pk': rule_id, 'start_sort': '999999', 'end_sort': '999999', 'mod_rule': 'MOD10',
                          'weight': [0,1,2,3,4,5,6,7,8,9,10,11,12,13], 'mod_exception': ''})
        assert response.status_code == 200, response.status_code
        assert '999999' in response.content.decode()

    def test_create_a_rule(self):
        user = User.objects.first()
        c = APIClient()
        token, created = Token.objects.get_or_create(user=user)
        c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c.post(reverse('apis:rule', kwargs={'pk': '999999'}),
                            {'start_sort': '999999', 'end_sort': '999999', 'mod_rule': 'MOD10',
                            'weight': [0,1,2,3,4,5,6,7,8,9,10,11,12,13], 'mod_exception': ''})
        assert response.status_code == 201, response.status_code
        assert '999999' in response.content.decode()

    def test_delete_a_rule(self):
        user = User.objects.first()
        rule_id = Rule.objects.first().id
        c = APIClient()
        token, created = Token.objects.get_or_create(user=user)
        c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c.delete(reverse('apis:rule', kwargs={'pk': rule_id}))
        assert response.status_code == 204, response.status_code

    def test_unauthorized_put_and_post_transactions(self):
        rule_id = Rule.objects.first().id
        c = APIClient()
        response = c.put(reverse('apis:rule', kwargs={'pk': rule_id}),
                                            {'start_sort': '999999', 'end_sort': '999999', 'mod_rule': 'MOD10',
                                            'weight': [0,1,2,3,4,5,6,7,8,9,10,11,12,13], 'mod_exception': ''})
        assert response.status_code == 401, response.status_code
        assert 'Authentication credentials were not provided' in response.content.decode(), response.content.decode()
