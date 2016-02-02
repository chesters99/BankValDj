import json
from .base import *

DEBUG = True


with open(os.path.join(BASE_DIR, 'BankValDj', 'settings', 'secret/local_secrets.json')) as f:
    secrets = json.loads(f.read())
SECRET_KEY = secrets["SECRET_KEY"]
STRIPE_SECRET_KEY = secrets["STRIPE_SECRET_KEY"]
STRIPE_PUBLIC_KEY = secrets["STRIPE_PUBLIC_KEY"]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # log emails to console

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
    # 'template_timings_panel',  # for debug toolbar
    #    'silk',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'silk.middleware.SilkyMiddleware',
)

# import pymysql # temporary fix for broken mysql connector in 1.7
# pymysql.install_as_MySQLdb() # temporary fix for broken mysql connector in 1.7
# DATABASES ={ 'ENGINE': 'mysql.connector.django', # temporary fix for broken mysql connector in 1.7

DATABASES = {
    #    'default': {
    #        'ENGINE': secret["DATABASE_ENGINE"],
    #        'NAME': secret["DATABASE_NAME"],
    #        'USER': secret["DATABASE_USER"],
    #        'PASSWORD': secret["DATABASE_PASSWORD"],
    #        'HOST': secret["DATABASE_HOST"],
    #        'PORT': secret["DATABASE_PORT"],
    #        'OPTIONS': { 'autocommit': True, },
    #    }

    #    'postgresql': {
    #        'ENGINE': secret["DATABASE_ENGINE"],
    #        'NAME': secret["DATABASE_NAME"],
    #        'USER': secret["DATABASE_USER"],
    #        'PASSWORD': secret["DATABASE_PASSWORD"],
    #        'HOST': secret["DATABASE_HOST"],
    #        'PORT': secret["DATABASE_PORT"],
    #    },
    #
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # using sqlite as is faster than mysql for testing
        'NAME': os.path.join(BASE_DIR, 'sqlite3.db'),
#        'TEST_NAME': os.path.join(BASE_DIR, 'sqlite3_test.db'),  # needed for selenium bug using sqlite in memory
        # 'ATOMIC_REQUESTS': True,  # use @atomic_transaction on requests which need transactions to avoid overhead
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_PATCH_SETTINGS = False
# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.profiling.ProfilingPanel',
#     'template_timings_panel.panels.TemplateTimings.TemplateTimings',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
# ]
