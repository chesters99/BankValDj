from random import randint
from os import environ
from django.test import LiveServerTestCase
from selenium import webdriver


class MainTests(LiveServerTestCase):
    fixtures = ['users.json','rules.json']

    def setUp(self):
        self.browser = webdriver.Remote(
            command_executor='http://%s:%s/wd/hub' %('10.0.2.2', 4444),
            desired_capabilities=webdriver.DesiredCapabilities.CHROME)
        self.username = 'graham'
        self.password = 'testpass'
        self.hostname = environ.get('TEST_HOST') or ''
        self.production = self.hostname in ['http://gchester.com', 'http://www.gchester.com' ]
        if self.hostname and 'http://' in self.hostname:
            self.my_server_url = self.hostname
        else:
            self.my_server_url = self.live_server_url
#        print('\nServer=' + self.my_server_url + '  Production=' + str(self.production))

    def tearDown(self):
        self.browser.quit()

    def login(self):
        self.browser.get(self.my_server_url + '/main/loginuser/')
        body = self.browser.find_element_by_tag_name('body')
        assert 'Username' in body.text
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(self.username)
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(self.password)
        button = self.browser.find_element_by_name('submit')
        button.click()  # no test for success as user_logged_in signal doesnt work in selenium

    def test_static_pages(self):
        self.browser.get(self.my_server_url)
        header = self.browser.find_element_by_tag_name('header')
        assert all(s in header.text for s in ('Bank Account Validation', 'Home', 'Validate', 'Rules')), header.text
        contact = self.browser.find_element_by_link_text('Contact')
        assert contact.location['x'] > 300, 'CSS not loaded - <About> hyperlink is not on right' + contact.location

        self.browser.get(self.my_server_url + '/main/showdoc/')
        body = self.browser.find_element_by_tag_name('body')
        assert 'Design Document' in body.text

        self.browser.get(self.my_server_url + '/main/about/')
        body = self.browser.find_element_by_tag_name('body')
        assert 'About this website' in body.text

        self.browser.get(self.my_server_url + '/main/contact/')
        body = self.browser.find_element_by_tag_name('body')
        assert 'Contact Information' in body.text

    def test_login_logout_ok(self):
        self.login()
        self.browser.get(self.my_server_url + '/main/logoutuser/')
        body = self.browser.find_element_by_tag_name('body')
        assert 'Logged Out Successfully' in body.text

    def test_app_registered_with_admin(self):
        self.login()
        self.browser.get(self.my_server_url + '/admin/')
        body = self.browser.find_element_by_tag_name('body')
        assert 'Django administration' in body.text
        assert 'Rules' in body.text, body.text
        assert 'Users' in body.text, body.text

    def test_create_a_user(self):
        self.login()
        self.browser.get(self.my_server_url + '/main/createuser/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('testuser_'+str(randint(0,10000)))
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('testuserp')
        button = self.browser.find_element_by_name('submit')
        button.click()
        body = self.browser.find_element_by_tag_name('body')
        assert 'Existing Users' in body.text
        assert 'User Created Successfully' in body.text, body.text

    def test_search_for_a_rule_found(self):
        self.login()
        self.browser.get(self.my_server_url + '/rules/search/')
        form = self.browser.find_element_by_name('form')
        sortcode_field = self.browser.find_element_by_name('q')
        sortcode_field.send_keys('400000')
        form.submit()
        body = self.browser.find_element_by_tag_name('body')
        assert 'MOD11' in body.text, body.text
        assert 'DBLAL' in body.text, body.text

    def test_validate_accounts_browser(self):
        self.login()
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
