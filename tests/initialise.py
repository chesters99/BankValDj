from django.contrib.auth.models import User
from os import path
from django.conf import settings
from rules.models import load_rules


def load_test_rules(sort_code=None):
    load_test_user()
    load_rules(path.join(settings.MEDIA_ROOT, 'valacdos.txt'),sort_code)


def load_test_user():
    User.objects.create_superuser('graham', 'chesters99@yahoo.com', 'testpass')
