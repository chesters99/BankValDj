import json
from .base import *

DEBUG = False

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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'debug': False,

            'context_processors': [
                # 'djstripe.context_processors.djstripe_settings',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.cached.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]
