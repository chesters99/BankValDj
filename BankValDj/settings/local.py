import json
from .base import *

DEBUG = True


with open(os.path.join(BASE_DIR, 'BankValDj', 'settings', 'secret/localvm_secrets.json')) as f:
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

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
