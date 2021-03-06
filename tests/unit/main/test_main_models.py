from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase

from tests.initialise import load_test_user


class MainModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        load_test_user()

    def test_get_all_users(self):
        users = get_user_model().objects.all()
        assert users.count() >= 1, users.count()

    def test_get_superuser(self):
        users = get_user_model().objects.filter(is_superuser=True)
        assert users.count() >= 1, users.count()

    def test_get_sites(self):
        sites = Site.objects.all()
        assert sites.count() >= 1, sites.count()
