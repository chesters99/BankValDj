import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SITE_ID = 1
ADMINS = (('Graham', 'chesters99@yahoo.com'),)

SECRET_KEY = os.environ.get("SECRET_KEY")

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
    'cacheops',
) + LOCAL_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DATABASE_NAME"),
        'USER': os.environ.get("DATABASE_USER"),
        'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
        'HOST': os.environ.get("DATABASE_HOST"),  # Or an IP Address that your DB is hosted on
        'PORT': os.environ.get("DATABASE_PORT"),
        'CONN_MAX_AGE': 600,
    },
}

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',  # use caching per page, not by whole site
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'BankValDj.middleware.CurrentUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',  # set site object on every request
    'django.middleware.locale.LocaleMiddleware',
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
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365
X_FRAME_OPTIONS = 'SAMEORIGIN'

ROOT_URLCONF = '%s.urls' % os.path.basename(BASE_DIR)
WSGI_APPLICATION = '%s.wsgi.application' % os.path.basename(BASE_DIR)

AUTH_PROFILE_MODULE = 'main.UserProfile'

LANGUAGE_CODE = 'en-GB'
TIME_ZONE = 'Europe/London'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'root')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOGIN_URL = '/main/loginuser/'
LOGIN_REDIRECT_URL = '/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static', 'source'), )
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )

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
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'djerrors.log'),
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
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

# django cacheops ORM caching setup
CACHEOPS_REDIS = {
    'host': 'localhost', # redis-server is on same machine
    'port': 6379,        # default redis port
    'db': 1,             # SELECT non-default redis database
    'socket_timeout': 3,   # connection timeout in seconds, optional
    # 'password': '...',     # optional
    # 'unix_socket_path': '' # replaces host and port
}

CACHEOPS = {
    'auth.*'    : {'ops': 'all', 'timeout': 24*60*60},
    'site.*'    : {'ops': 'all', 'timeout': 24*60*60},
    'rules.rule': {'ops': 'all', 'timeout': 24*60*60},
    'eventlog.log': {'ops': 'all', 'timeout': 24*60*60},
    # '*.*'       : {'ops': 'all', 'timeout': 24*60*60}, # causes problems with django content types
}


STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
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
