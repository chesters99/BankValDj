import json, sys, os
import psycopg2.extensions
from .base import *

DEBUG = True

with open(os.path.join(BASE_DIR, 'BankValDj', 'settings', 'secret/localvm_secrets.json')) as f:
    secrets = json.loads(f.read())


SECRET_KEY = secrets["SECRET_KEY"]
STRIPE_SECRET_KEY = secrets["STRIPE_SECRET_KEY"]
STRIPE_PUBLIC_KEY = secrets["STRIPE_PUBLIC_KEY"]

#email settings for google in localvm only
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True # or EMAIL_PORT = 465 and EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'gchester99@gmail.com'
EMAIL_HOST_PASSWORD = 'hudson-99'
DEFAULT_FROM_EMAIL = 'gchester99@gmail.com'
SERVER_EMAIL = 'gchester99@gmail.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': secrets["DATABASE_NAME"],
        'USER': secrets["DATABASE_USER"],
        'PASSWORD': secrets["DATABASE_PASSWORD"],
        'HOST': secrets["DATABASE_HOST"],  # Or an IP Address that your DB is hosted on
        'PORT': secrets["DATABASE_PORT"],
    },
    'OPTIONS': {
        'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
    },
}

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
    'debug_toolbar_line_profiler',
)

MIDDLEWARE_CLASSES =  (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE_CLASSES

os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '0.0.0.0:8080'

if 'manage.py' in sys.argv[0]: # turn on django debug toolbar only under manage.py runserver, not uwsgi
    INTERNAL_IPS = ('127.0.0.1', '10.0.2.2') # include virtualbox VM address

DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    #'debug_toolbar.panels.profiling.ProfilingPanel',
    'debug_toolbar_line_profiler.panel.ProfilingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
