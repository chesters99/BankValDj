from os import path
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from rules.models import Rule, load_rules


class RuleModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('graham', 'chesters99@yahoo.com', 'testpass')
        load_rules(path.join(settings.MEDIA_ROOT, 'valacdos.txt'))

    def test_get_all_rules(self):
        rules = Rule.objects.all()
        assert rules.count() > 950

    def test_get_a_rule(self):
        rules = Rule.objects.filter(start_sort='400000')
        assert len(rules) >= 1
        assert rules.values()[0]['mod_rule'] == 'MOD11'

    def test_add_rule(self):
        rule = Rule(start_sort='100000', end_sort='100001', mod_rule='MOD10',
                    weight=[0,1,2,3,4,5,6,7,8,9,10,11,12,13], mod_exception='')
        rule.save()
        record = Rule.objects.get(pk=rule.id)
        assert record == rule
        assert '/rules/detail/' in str(rule.get_absolute_url())

    def test_delete_rule(self):
        rule = Rule(start_sort='100000', end_sort='100001', mod_rule='MOD10',
                    weight=[0,1,2,3,4,5,6,7,8,9,10,11,12,13], mod_exception='')
        rule.save()
        rule.delete()
        assert rule.id is None
