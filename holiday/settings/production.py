from .base import *


ALLOWED_HOSTS = ['3.34.75.143','boongmark.com']


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'boongmark',
        'USER': 'dbmasteruser',
        'PASSWORD': ';Z}gl4RjjaV8!ST40QoCRY|*yA{t?8qC',
        'HOST': 'ls-b846cf94dffffe6800c27ade9ff95ade0f2c79ba.cdqzykhsiown.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}
