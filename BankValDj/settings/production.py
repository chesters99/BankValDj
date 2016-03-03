import json
from .base import *

DEBUG = False

with open(os.path.join(BASE_DIR, 'BankValDj', 'settings', 'secret/production_secrets.json')) as f:
    secrets = json.loads(f.read())

ALLOWED_HOSTS = ['.gchester.com',]

SECRET_KEY = secrets["SECRET_KEY"]
STRIPE_SECRET_KEY = secrets["STRIPE_SECRET_KEY"]
STRIPE_PUBLIC_KEY = secrets["STRIPE_PUBLIC_KEY"]

# email settings for postfix in production
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'django@gchester.com'
SERVER_EMAIL = 'djadmin@gchester.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': secrets["DATABASE_NAME"],
        'USER': secrets["DATABASE_USER"],
        'PASSWORD': secrets["DATABASE_PASSWORD"],
        'HOST': secrets["DATABASE_HOST"],  # Or an IP Address that your DB is hosted on
        'PORT': secrets["DATABASE_PORT"],
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
#SECURE_SSL_REDIRECT = True # do in nginx instead


