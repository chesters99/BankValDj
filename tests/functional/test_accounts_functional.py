from tests.initialise import FunctionalTest


class ValidateTests(FunctionalTest):

    def test_validate_account_browser(self):
        self.load_rules('500000')
        self.browser.get(self.my_server_url + '/en/accounts/validate')
        sortcode_field = self.browser.find_element_by_name('sort_code')
        sortcode_field.send_keys('500000')
        account_field = self.browser.find_element_by_name('account_number')
        account_field.send_keys('12312312')
        button = self.browser.find_element_by_name('submit')
        button.click()
        body = self.browser.find_element_by_tag_name('body')
        assert 'valid bank account' in body.text, body.text

    def test_run_bulktest_file(self):
        self.load_rules()
        self.browser.get(self.my_server_url + '/en/accounts/bulktest/')
        button = self.browser.find_element_by_name('submit')
        button.click()
        body = self.browser.find_element_by_tag_name('body')
        print(body.text)
        assert 'Valid=True' in body.text, body.text
        assert 'Valid=False' in body.text, body.text