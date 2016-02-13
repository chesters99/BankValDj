import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE_ID = 1
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # in case debug mode is turned off this is required
ADMINS = (('Graham', 'chesters99@yahoo.com'),)

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
    'django.middleware.cache.UpdateCacheMiddleware',  # use caching per page, not by whole site
    'django.middleware.security.SecurityMiddleware',
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
    # 'django.middleware.cache.FetchFromCacheMiddleware', # use caching per page, not by whole site
)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '/tmp/redis.sock',
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

CSRF_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 5
X_FRAME_OPTIONS = 'DENY'

CONN_MAX_AGE = 300  # database pooling

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

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static', 'source'), )
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 3,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

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
            'filename': '../../django_errors.log',
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# Celery and Celerybeat settings
# from celery.schedules import crontab
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYBEAT_SCHEDULE = {
    ### crontab(hour=0, minute=0, day_of_week='saturday')
    # 'schedule-name': {  # example: 'file-backup'
    #     'task': 'accounts.tasks.test_task',  # example: 'files.tasks.cleanup'
    #     # 'schedule': crontab(...)
    #     'schedule': timedelta(seconds=10),
    #     'args': (3,),
    # },
}
