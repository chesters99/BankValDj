from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1','.gchester.com']  # in case debug mode is turned off this is required

# email settings for google in localvm only
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True # oe EMAIL_USE_SSL = True, EMAIL_PORT = 465
EMAIL_HOST_USER = 'gchester99@gmail.com'
EMAIL_HOST_PASSWORD = 'hudson-99'
DEFAULT_FROM_EMAIL = 'gchester99@gmail.com'
SERVER_EMAIL = 'gchester99@gmail.com'

os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '0.0.0.0:8080'

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
    'debug_toolbar_line_profiler',
    #'template_timings_panel', commented out due to bug with django 1.9 (being fixed)
)

MIDDLEWARE_CLASSES =  (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE_CLASSES

import sys
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
    # 'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    #'debug_toolbar.panels.profiling.ProfilingPanel',
    'debug_toolbar_line_profiler.panel.ProfilingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
