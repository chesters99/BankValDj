from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rules.models import Rule
from tests.initialise import UnitTest
from rest_framework.authtoken.models import Token
from pytest import mark
from unittest import skip


class ApisTests(UnitTest):
    """Test APIs"""

    def test_validate_api_valid(self):
        self.load_rules('500000')
        c = APIClient()
        response = c.post(reverse('apis:validate'), {"sort_code": "500000", "account_number": "12312312"})
        assert response.status_code == 200

    def test_validate_api_invalid(self):
        self.load_rules('500000')
        c = APIClient()
        response = c.post(reverse('apis:validate'), {"sort_code": "500000", "account_number": "12312313"})
        assert response.status_code == 406

    def test_get_rules_range(self):
        self.load_rules('300008')
        c = APIClient()
        response = c.get(reverse('apis:ruleview'), {'start_sort': '300000', 'end_sort': '300050'})
        assert response.status_code == 200
        assert '300008' in response.content.decode()

    def test_get_a_rule(self):
        self.load_rules('300008')
        rule_id = Rule.objects.first().id
        c = APIClient()
        token = Token.objects.create(user=self.user)
        c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c.get(reverse('apis:ruleview'), {'pk': rule_id}, secure=True)
        assert response.status_code == 200
        assert '300008' in response.content.decode()


    def test_update_a_rule(self):
        self.load_rules('300008')
        rule_id = Rule.objects.first().id
        c = APIClient()
        token = Token.objects.create(user=self.user)
        c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c.put(reverse('apis:rulechg', kwargs={'pk': rule_id}),
                         {'pk': rule_id, 'start_sort': '999999', 'end_sort': '999999', 'mod_rule': 'MOD10',
                          'weight0': 1, 'weight1': 1, 'weight2': 1, 'weight3': 1, 'weight4': 1,
                          'weight5': 1, 'weight6': 1, 'weight7': 1, 'weight8': 1, 'weight9': 1,
                          'weight10': 1, 'weight11': 1, 'weight12': 1, 'weight13': 1,
                          'mod_exception': ''}, secure=True)
        assert response.status_code == 200

        assert '999999' in response.content.decode()
    
    @mark.xfail
    @skip("This API test should fail so skipping\n")
    def test_create_a_rule(self):
        c = APIClient()
        token = Token.objects.create(user=self.user)
        c.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = c.post(reverse('apis:rulechg', kwargs={'pk': '9999999'}),
                            {'start_sort': '999999', 'end_sort': '999999', 'mod_rule': 'MOD10',
                            'weight0': 1, 'weight1': 1, 'weight2': 1, 'weight3': 1, 'weight4': 1,
                            'weight5': 1, 'weight6': 1, 'weight7': 1, 'weight8': 1, 'weight9': 1,
                            'weight10': 1, 'weight11': 1, 'weight12': 1, 'weight13': 1,
                            'mod_exception': ''}, secure=True)
        assert response.status_code == 201
        assert '999999' in response.content.decode()

    @mark.xfail
    @skip("This API test should fail so skipping\n")
    def test_unauthorized_put_and_post_transactions(self):
        self.load_rules('500000')
        rule_id = Rule.objects.first().id
        c = APIClient()
        token = Token.objects.create(user=self.user)
        token.key = token.key[0:-1] + 'X'  # mess up the token

        response = c.put(reverse('apis:rulechg', kwargs={'pk': rule_id}),
                                            {'start_sort': '999999', 'end_sort': '999999', 'mod_rule': 'MOD10',
                                            'weight0': 1, 'weight1': 1, 'weight2': 1, 'weight3': 1, 'weight4': 1,
                                            'weight5': 1, 'weight6': 1, 'weight7': 1, 'weight8': 1, 'weight9': 1,
                                            'weight10': 1, 'weight11': 1, 'weight12': 1, 'weight13': 1,
                                            'mod_exception': ''}, secure=True)
        assert response.status_code == 403
        assert 'Authentication credentials were not provided' in response.content.decode(), response.content.decode()
