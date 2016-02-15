from tests.initialise import FunctionalTest

class RulesTests(FunctionalTest):

    def test_search_for_a_rule_found(self):
        self.login()
        self.load_rules()
        self.browser.get(self.my_server_url + '/rules/search/')
        form = self.browser.find_element_by_name('form')
        sortcode_field = self.browser.find_element_by_name('q')
        sortcode_field.send_keys('400000')
        form.submit()
        body = self.browser.find_element_by_tag_name('body')
        assert 'MOD11' in body.text, body.text
        assert 'DBLAL' in body.text, body.text

