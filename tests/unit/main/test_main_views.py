from django.test import RequestFactory
from main.views import Graph
from tests.initialise import UnitTest


class MainViews(UnitTest):
    """Test templates Views"""
    def test_with_requestfactory(self):  # request factory is faster than django web client
        factory = RequestFactory()
        request = factory.get('/')
        request.session = {}
        request.user = self.user
        response = Graph.as_view()(request)
        assert response.status_code == 200

    def test_index_view(self):
        response = self.client.get('/en/', {})
        assert response.status_code == 200
        assert 'Home' in response.content.decode(), response.content.decode()
        assert 'Validate' in response.content.decode(), response.content.decode()
        assert 'Test' in response.content.decode(), response.content.decode()
        assert 'Admin' in response.content.decode(), response.content.decode()

    def test_about_view(self):
        response = self.client.get('/en/main/about/', {})
        assert response.status_code == 200
        assert 'About' in response.content.decode(), response.content.decode()

    def test_contact_view(self):
        response = self.client.get('/en/main/contact/', {})
        assert response.status_code == 200
        assert 'Contact' in response.content.decode(), response.content.decode()

    def test_showdoc_view(self):
        response = self.client.get('/en/main/showdoc/', {})
        assert response.status_code == 200
        assert 'Design Document' in response.content.decode(), response.content.decode()

    def test_graph_view(self):
        response = self.client.get('/en/main/graph/', {})
        assert response.status_code == 200
        assert 'Graph' in response.content.decode(), response.content.decode()

    def test_createuser_view_success(self):
        self.login_as_superuser(self.client)
        response = self.client.post('/en/main/createuser/', {'username': 'testuser', 'password': 'testpass'})
        assert response.status_code == 200
        assert 'User Created Successfully' in response.content.decode(), response.content.decode()
        assert 'testuser' in response.content.decode(), response.content.decode()

    def test_createuser_view_fail_password(self):
        self.login_as_superuser(self.client)
        response = self.client.post('/en/main/createuser/', {'username': 'testuser', 'password': 'te'})
        assert response.status_code == 200
        assert 'Password must be more than' in response.content.decode(), response.content.decode()

    def test_createuser_view_fail_not_logged_in(self):
        response = self.client.post('/en/main/createuser/', {'username': 'testuser', 'password': 'te'})
        assert response.status_code == 302

    def test_logoutuser_view(self):
        self.login_as_superuser(self.client)
        response = self.client.post('/en/main/logoutuser/', follow=True)
        assert response.status_code == 200
        assert 'Logged Out Successfully' in response.content.decode(), response.content.decode()

    def test_loginuser_view(self):
        self.login_as_superuser(self.client)
        response = self.client.post('/en/main/loginuser',
                                    {'username': self.username, 'password': self.password}, follow=True)
        assert response.status_code == 200
        assert 'successfully logged in' in response.content.decode(), response.content.decode()

    def test_page_not_found(self):
        response = self.client.post('/en/xxxxxxxx/', {})
        assert response.status_code == 404
        assert 'Page not found' in response.content.decode(), response.content.decode()
        assert 'to go back to the home page' in response.content.decode(), response.content.decode()

    def test_sitemap(self):
        response = self.client.get('/en/sitemap.xml', {})
        assert response.status_code == 200
        assert 'www.sitemaps.org/schemas' in response.content.decode(), response.content.decode()
