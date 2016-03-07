from .base import *

DEBUG = False

ALLOWED_HOSTS = ['.gchester.com',]

# email settings for postfix in production
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'django@gchester.com'
SERVER_EMAIL = 'djadmin@gchester.com'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True # but done in nginx before reaching django
