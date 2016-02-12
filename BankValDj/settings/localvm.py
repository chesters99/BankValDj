import json
from .base import *

DEBUG = True

with open(os.path.join(BASE_DIR, 'BankValDj', 'settings', 'secret/localvm_secrets.json')) as f:
    secrets = json.loads(f.read())
SECRET_KEY = secrets["SECRET_KEY"]
STRIPE_SECRET_KEY = secrets["STRIPE_SECRET_KEY"]
STRIPE_PUBLIC_KEY = secrets["STRIPE_PUBLIC_KEY"]

# to test emails, do the following
#from django.core.mail import EmailMessage
#email = EmailMessage('Mail Test', 'This is a test', to=['chesters99@yahoo.com'])
#email.send()

#email settings for google in localvm only
# EMAIL_PORT = 465
# EMAIL_USE_SSL = True # EMAIL_PORT = 465
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True # EMAIL_PORT = 465
EMAIL_HOST_USER = 'gchester99@gmail.com'
EMAIL_HOST_PASSWORD = 'hudson-99'
DEFAULT_FROM_EMAIL = 'gchester99@gmail.com'
SERVER_EMAIL = 'gchester99@gmail.com'

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
    # 'template_timings_panel',  # for debug toolbar
    #    'silk',
)

MIDDLEWARE_CLASSES =  (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'silk.middleware.SilkyMiddleware',
) + MIDDLEWARE_CLASSES


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
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2') # include virtualbox VM address
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
