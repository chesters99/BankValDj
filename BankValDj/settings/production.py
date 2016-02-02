import json
from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

with open(os.path.join(BASE_DIR, 'BankValDj', 'settings', 'secret/production_secrets.json')) as f:
    secrets = json.loads(f.read())
SECRET_KEY = secrets["SECRET_KEY"]
STRIPE_SECRET_KEY = secrets["STRIPE_SECRET_KEY"]
STRIPE_PUBLIC_KEY = secrets["STRIPE_PUBLIC_KEY"]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 5
X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = ['gchester.com', 'www.gchester.com', '54.164.140.224']  # usually overridden later by fabric deployment

import pymysql  # temporary fix for broken mysql connector in 1.7
pymysql.install_as_MySQLdb()  # temporary fix for broken mysql connector in 1.7
# DATABASES ={ 'ENGINE': 'mysql.connector.django', # temporary fix for broken mysql connector in 1.7

DATABASES = {
    'default': {
        'ENGINE': secrets["DATABASE_ENGINE"],
        'NAME': secrets["DATABASE_NAME"],
        'USER': secrets["DATABASE_USER"],
        'PASSWORD': secrets["DATABASE_PASSWORD"],
        'HOST': secrets["DATABASE_HOST"],  # Or an IP Address that your DB is hosted on
        'PORT': secrets["DATABASE_PORT"],
        'OPTIONS': {'autocommit': True, },
        # 'ATOMIC_REQUESTS': True,  # use @atomic_transaction on requests which need transactions to avoid overhead
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}
