import os
from django.conf import settings
from django.test import TestCase
from rules.models import Rule, get_rules, load_rules


class RuleModelTests(TestCase):
    fixtures = ['users.json','rules.json']

    def test_get_all_rules(self):
        rules = Rule.objects.all()
        assert rules.count() > 950

    def test_get_a_rule(self):
        rules = Rule.objects.filter(start_sort='400000')
        assert len(rules) >= 1
        assert rules.values()[0]['mod_rule'] == 'MOD11'

    def test_add_rule(self):
        rule = Rule(start_sort='100000', end_sort='100001', mod_rule='MOD10', weight0=0, weight1=1, weight2=2,
                    weight3=3, weight4=4, weight5=5, weight6=6, weight7=7, weight8=8, weight9=9, weight10=10,
                    weight11=11, weight12=12, weight13=13, mod_exception='')
        rule.save()
        record = Rule.objects.get(pk=rule.id)
        assert record == rule
        assert '/rules/detail/' in str(rule.get_absolute_url())

    def test_delete_rule(self):
        rule = Rule(start_sort='100000', end_sort='100001', mod_rule='MOD10', weight0=0, weight1=1, weight2=2,
                    weight3=3, weight4=4, weight5=5, weight6=6, weight7=7, weight8=8, weight9=9, weight10=10,
                    weight11=11, weight12=12, weight13=13, mod_exception='')
        rule.save()
        rule.delete()
        record = Rule.objects.get(pk=rule.id)
        assert record.active is False

    def test_get_and_load_rules(self):
        rows = get_rules(os.path.join(settings.MEDIA_ROOT, 'valacdos.txt'))
        assert len(rows) > 900
        records = load_rules(rows)
        assert records > 900
