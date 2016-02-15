from tests.initialise import FunctionalTest


class ValidateTests(FunctionalTest):

    def test_validate_accounts_browser(self):
        self.login()
        self.load_rules()

        self.browser.get(self.my_server_url + '/accounts/validate')
        sortcode_field = self.browser.find_element_by_name('sort_code')
        sortcode_field.send_keys('500000')
        account_field = self.browser.find_element_by_name('account_number')
        account_field.send_keys('12312312')
        button = self.browser.find_element_by_name('submit')
        button.click()
        body = self.browser.find_element_by_tag_name('body')
        assert 'valid bank account' in body.text, body.text
        assert 'Warning' not in body.text, body.text

        self.browser.get(self.my_server_url + '/accounts/bulktest/')
        button = self.browser.find_element_by_name('submit')
        button.click()
        body = self.browser.find_element_by_tag_name('body')
        assert 'Valid=True' in body.text, body.text
        assert 'Valid=False' in body.text, body.text


