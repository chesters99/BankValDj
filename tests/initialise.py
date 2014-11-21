import os
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from django.contrib.auth.models import User
from django.conf import settings
from rules.models import Rule, get_rules, load_rules


class FunctionalTest(LiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()  # fix for ignore-certificate-errors warning in Chrome
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        self.browser = webdriver.Chrome(chrome_options=options)
        self.browser.implicitly_wait(5)

        self.username = 'graham'
        self.password = 'testpass'
        self.user = User.objects.create(id=1, username=self.username, is_superuser=True, is_staff=True)
        self.user.set_password(self.password)
        self.user.save()

        self.hostname = os.environ.get('TEST_HOST') or ''
        self.production = self.hostname in ['http://gchester.com', ]
        if self.hostname and 'http://' in self.hostname:
            self.my_server_url = self.hostname
        else:
            self.my_server_url = self.live_server_url
        print('\nServer=' + self.my_server_url + '  Production=' + str(self.production))

    def tearDown(self):
        self.browser.quit()

    def login(self):
        self.browser.get(self.my_server_url + '/en/main/loginuser/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Username', body.text)
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(self.username)
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(self.password)
        button = self.browser.find_element_by_name('submit')
        button.click()  # no test for success as user_logged_in signal doesnt work in selenium

    def load_rules(self, sort_code=None):
        filename = os.path.join(settings.MEDIA_ROOT, 'valacdos.txt')
        rows = get_rules(filename)
        if rows is None:
            print('File %s not found' % filename)
            return
        records = load_rules(rows=rows, sort_code=sort_code)
        print("Records Loaded %s " % records)


class UnitTest(TestCase):
    def setUp(self):
        self.username = 'graham'
        self.password = 'testpass'
        self.user = User.objects.create(username=self.username, is_superuser=True, is_staff=True)
        self.user.set_password(self.password)
        self.user.save()

    def tearDown(self):
        pass

    def login_as_superuser(self, client):
        response = client.post('/en/main/loginuser/', {'username': 'graham', 'password': 'testpass'})
        assert response.status_code == 302

    def load_rules(self, sort_code=None):
        filename = os.path.join(settings.MEDIA_ROOT, 'valacdos.txt')
        rows = get_rules(filename)
        if rows is None:
            print('File %s not found' % filename)
            return
        records = load_rules(rows=rows, sort_code=sort_code)
        print("Records Loaded %s " % records)
