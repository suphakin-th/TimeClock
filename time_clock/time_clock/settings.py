import os
import sys
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/hswto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.environ.get('SECRET_KEY', None))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_swagger',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_filters',
    'account',
    'log',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

INTERNAL_IPS = ('127.0.0.1',)


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
]
ROOT_URLCONF = 'time_clock.urls'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'time_clock.wsgi.application'
AUTH_USER_MODEL = 'account.Account'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

TIME_ZONE = 'Asia/Bangkok'

DATE_FORMAT = '%d %b %Y'
DATE_FORMAT_INDEX = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'
DATETIME_FORMAT = '%e %B %Y %H:%M:%S'
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_URL = 'http://127.0.0.1:8000'

STATIC_URL = '/static/back/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATIC_ROOT = os.path.join(BASE_DIR, 'deploy_static/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

DATA_UPLOAD_MAX_NUMBER_FIELDS = 102400
LOGIN_URL = '/admin/login/'
LOGOUT_URL = '/admin/logout/'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'EXCEPTION_HANDLER': 'utils.rest_framework.exception.exception_handler',

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),

    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'PAGE_SIZE': 24,
    # "DATE_INPUT_FORMATS": ["%d/%m/%Y"],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

ROUTER_INCLUDE_ROOT_VIEW = False

SWAGGER_SETTINGS = {
    'IS_ENABLE': True,
    'SHOW_REQUEST_HEADERS': True,
    'IS_SUPERUSER': True,
    'VALIDATOR_URL': None,
}

IS_ENABLE_CONFIG_SETTINGS = True
IS_ENABLE_CACHED_LOCATION_SETTINGS = True

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_SAVE_EVERY_REQUEST = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'memcached',
    }
}


PROJECT = 'PROJECT'
SUPER_ADMIN_GROUP_ID = 1
DEFAULT_TIMEOUT = 10

IS_HIDE_ADMIN_URL = False

FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800

# MODEL
PASSWORD_MIN = 4

IS_SEND_EMAIL = True
IS_SEND_FCM = True

TESTING = sys.argv[1:2] == ['test']
IS_LOCALHOST = sys.argv[1:2] == ['runserver']

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": 'AAAAdPi9HbQ:APA91bFTEeS6Gy9hpe4GTzo6MG37eC0sSD5Xa2J2RCuykmjhz426G3DCfJiGH_Wwy8LD0EzdsObP0SMdsLxrq47bFMqbLeYlMtu4CtkxgK8DHjVv5lTKdq6om6L3yb5jtA03rASUaANX',
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": False,
}

if TESTING:
    ENABLE_LOGGING = False
    CELERY_TASK_ALWAYS_EAGER = True
    MONGODB_HOST = 'mongo'
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    CACHES['default'] = {'BACKEND': 'django.core.cache.backends.dummy.DummyCache', }
    # FCM_DJANGO_SETTINGS["FCM_SERVER_KEY"] = 'AAAAdPi9HbQ:APA91bFTEeS6Gy9hpe4GTzo6MG37eC0sSD5Xa2J2RCuykmjhz426G3DCfJiGH_Wwy8LD0EzdsObP0SMdsLxrq47bFMqbLeYlMtu4CtkxgK8DHjVv5lTKdq6om6L3yb5jtA03rASUaANX'

CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
#
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'time_clock',
        'USER': 'root',
        'PASSWORD': 'password',
        'TEST': {
            'NAME': 'hrd_test',
        },
        'HOST': 'mariadb',
        'PORT': '3306'
    }
}

EXPLORER_CONNECTIONS = {'default': 'default'}
EXPLORER_DEFAULT_CONNECTION = 'default'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60)
}

DJANGO_ALLOW_ASYNC_UNSAFE = True
