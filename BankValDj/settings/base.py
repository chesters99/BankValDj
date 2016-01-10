import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE_ID = 1
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # in case debug mode is turned off this is required

ADMINS = (('Graham', 'chesters99@yahoo.com'),)
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
# EMAIL_USE_TLS = True # causes starttls error on amazon ec2
SERVER_EMAIL = 'django@gchester.com'

LOCAL_APPS = (
    'main',
    'accounts',
    'rules',
    'subs',
    'apis',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.admindocs',
    'localflavor',
    'rest_framework',
    'rest_framework.authtoken',
    'djcelery',
    'eventlog',
    'djstripe',
) + LOCAL_APPS


MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',  # caching must be disabled on transaction processing sites
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',  # set site object on every request
    'django.middleware.locale.LocaleMiddleware',
    'BankValDj.middleware.CurrentUserMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware', # caching must be disabled on transaction processing sites
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

ROOT_URLCONF = '%s.urls' % os.path.basename(BASE_DIR)
WSGI_APPLICATION = '%s.wsgi.application' % os.path.basename(BASE_DIR)

AUTH_PROFILE_MODULE = 'main.UserProfile'

LANGUAGE_CODE = 'en-GB'
TIME_ZONE = 'Europe/London'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
LOGIN_URL = '/main/loginuser/'
LOGIN_REDIRECT_URL = '/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
#               'djstripe.context_processors.djstripe_settings',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static', 'source'), )
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'errorfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/log/errors.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'formatter': 'verbose'
        },
        'null': {
            'level': 'INFO',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['errorfile', 'mail_admins'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    }
}


DJSTRIPE_PLANS = {
    'monthly': {
        'stripe_plan_id': 'monthly_plan',
        'name': 'Monthly Plan',
        'description': 'Monthly Subscription Plan',
        'price': 1000,
        'currency': 'gbp',
        'interval': 'month',
    },
}

# Celery and Celerybeat settings
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
