from tests.initialise import FunctionalTest


class MainTests(FunctionalTest):
    def test_home_page_ok(self):
        self.browser.get(self.my_server_url + '/en')
        header = self.browser.find_element_by_tag_name('header')
        assert all(s in header.text for s in ('Bank Account Validation', 'Home', 'Validate', 'Rules')), header.text
        contact = self.browser.find_element_by_link_text('Contact')
        assert contact.location['x'] > 300, 'CSS not loaded - <About> hyperlink is not on right side of page'

    def test_show_design_document_ok(self):
        self.browser.get(self.my_server_url + '/en/main/showdoc/')
        body = self.browser.find_element_by_tag_name('body')
        assert 'Design Document' in body.text

    def test_about_page_ok(self):
        self.browser.get(self.my_server_url + '/en/main/about/')
        body = self.browser.find_element_by_tag_name('body')
        assert 'About this website' in body.text

    def test_contact_page_ok(self):
        self.browser.get(self.my_server_url + '/en/main/contact/')
        body = self.browser.find_element_by_tag_name('body')
        assert 'Contact Information' in body.text

    def test_logout_ok(self):
        self.login()
        self.browser.get(self.my_server_url + '/en/main/logoutuser/')
        body = self.browser.find_element_by_tag_name('body')
        assert 'Logged Out Successfully' in body.text

    def test_app_rules_is_registered_with_admin(self):
        self.login()
        self.browser.get(self.my_server_url + '/en/admin/')
        body = self.browser.find_element_by_tag_name('body')
        assert 'Django administration' in body.text
        assert 'Rules' in body.text, body.text

    def test_create_a_user(self):
        self.login()
        self.browser.get(self.my_server_url + '/en/main/createuser/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('testuser1')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('testuser1p')
        if not self.production:
            button = self.browser.find_element_by_name('submit')  # make test read only so can run against production
            button.click()
        body = self.browser.find_element_by_tag_name('body')
        assert 'Existing Users' in body.text
        if not self.production:
            assert 'User Created Successfully' in body.text
