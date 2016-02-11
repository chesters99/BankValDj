import json
from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

with open(os.path.join(BASE_DIR, 'BankValDj', 'settings', 'secret/production_secrets.json')) as f:
    secrets = json.loads(f.read())
SECRET_KEY = secrets["SECRET_KEY"]
STRIPE_SECRET_KEY = secrets["STRIPE_SECRET_KEY"]
STRIPE_PUBLIC_KEY = secrets["STRIPE_PUBLIC_KEY"]

os.environ['HTTPS'] = "on"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 5
X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = ['.gchester.com',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': secrets["DATABASE_NAME"],
        'USER': secrets["DATABASE_USER"],
        'PASSWORD': secrets["DATABASE_PASSWORD"],
        'HOST': secrets["DATABASE_HOST"],  # Or an IP Address that your DB is hosted on
        'PORT': secrets["DATABASE_PORT"],
    }
}

