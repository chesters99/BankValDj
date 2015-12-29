from tests.initialise import FunctionalTest


class RulesTests(FunctionalTest):

    def test_search_for_a_rule_found(self):
        self.load_rules('400000')
        self.browser.get(self.my_server_url + '/rules/search/')
        form = self.browser.find_element_by_name('form')
        sortcode_field = self.browser.find_element_by_name('q')
        sortcode_field.send_keys('400000')
        form.submit()
        body = self.browser.find_element_by_tag_name('body')
        assert 'MOD11' in body.text, body.text
        assert 'DBLAL' in body.text, body.text

    def test_load_rules_file(self):
        self.login()
        self.browser.get(self.my_server_url + '/rules/load/')
        if not self.production:
            button = self.browser.find_element_by_name('submit')
            button.click()
        body = self.browser.find_element_by_tag_name('body')
        assert 'Filename:' in body.text
        if not self.production:
            assert 'Rules loaded successfully' in body.text, body.text
