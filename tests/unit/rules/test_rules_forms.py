from rules.forms import *
from django.test import TestCase

class RuleFormTests(TestCase):
    """Test templates forms"""

    def test_ruleform_with_valid_data(self):
        form_data = {'start_sort': '999999', 'end_sort': '999999', 'mod_rule': 'MOD10', 'mod_exception': '3',
                     'weight': '0,1,2,3,4,5,6,7,8,9,10,11,12,13','created_by': '1'}
        form = RuleForm(data=form_data)
        assert form.is_valid(), form.errors.as_text()
        assert form.instance.start_sort == '999999'

    def test_ruleform_with_invalid_data(self):  # w13 makes form not valid
        form_data = {'start_sort': '999999', 'end_sort': '999999', 'mod_rule': 'MOD10', 'mod_exception': '3',
                     'weight': '0,1,2,3,4,5,6,7,8,9,10,11,12,99999'}
        form = RuleForm(data=form_data)
        assert not form.is_valid(), form.errors.as_text()

    def test_loadrulesform_valid(self):
        form_data = {'filename': 'test.txt'}
        form = LoadRulesForm(data=form_data)
        assert form.is_valid(), form.errors.as_text()
