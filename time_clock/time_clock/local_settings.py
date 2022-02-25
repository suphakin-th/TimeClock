from .settings import INSTALLED_APPS, MIDDLEWARE

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS.append('django_extensions')
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ('127.0.0.1',)

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
        'NAME': 'TimeClock',
        'USER': 'root',
        'PASSWORD': 'password',
        'TEST': {
            'NAME': 'hrd_test',
        },
        'HOST': 'mariadb',
        'PORT': '3306'
    }
}

SWAGGER_SETTINGS = {
    'IS_ENABLE': True,
    'SHOW_REQUEST_HEADERS': True,
    'IS_SUPERUSER': True,
    'VALIDATOR_URL': None,
}

