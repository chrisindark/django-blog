from mysite.settings.common import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_var('SECRET_KEY', default='secret-key')

ALLOWED_HOSTS = (
    'localhost',
    '0.0.0.0',
    '127.0.0.1',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG', # message level to be written to console
            # logging handler that outputs log messages to terminal
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            # this sets root level logger to log debug and higher level
            # logs to console. All other loggers inherit settings from
            # root level logger.
            'handlers': ['console'],
            'level': 'DEBUG',
            # this tells logger to send logging message
            # to its parent (will send if set to True)
            'propagate': False
        },
        'django.db': {
            # 'level': 'DEBUG'
            # django also has database level logging
        },
    },
}

INSTALLED_APPS += (
    'django_extensions',
)

MIDDLEWARE += ()

# Database
DATABASES = {}
if os.environ.get('DJB_HEROKU_ENV'):
    DATABASES['default'] = dj_database_url.config()
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_var('DB_NAME'),
        'USER': get_env_var('DB_USERNAME'),
        'PASSWORD': get_env_var('DB_PASSWORD'),
        'HOST': get_env_var('DB_HOST'),
        'PORT': get_env_var('DB_PORT'),
    }

SITE_NAME = 'DjangoBlog'
APP_NAME = 'DjangoBlog'
STATIC_APP_URL = get_env_var('STATIC_APP_URL', default='http://localhost:8000/')
DOMAIN_URL = STATIC_APP_URL.split('://')[1]
LOGIN_URL='/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/accounts/logout/'
LOGOUT_REDIRECT_URL = '/'

CORS_ORIGIN_WHITELIST = ()
CORS_ORIGIN_ALLOW_ALL = True

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_HOST = get_env_var('EMAIL_HOST')
EMAIL_PORT = get_env_var('EMAIL_PORT')
EMAIL_HOST_USER = get_env_var('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_var('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


GOOGLE_OAUTH2_CLIENT_ID = get_env_var('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = get_env_var('GOOGLE_OAUTH2_CLIENT_SECRET')
GOOGLE_OAUTH2_CALLBACK_URL = STATIC_APP_URL + 'auth/google/callback'

GITHUB_OAUTH2_CLIENT_ID = get_env_var('GITHUB_OAUTH2_CLIENT_ID')
GITHUB_OAUTH2_CLIENT_SECRET = get_env_var('GITHUB_OAUTH2_CLIENT_SECRET')
GITHUB_OAUTH2_CALLBACK_URL = STATIC_APP_URL + 'auth/github/callback'
