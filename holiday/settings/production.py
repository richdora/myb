from .base import *

import os

DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = ['43.201.208.185','boongmark.com']


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
            'level': 'INFO',
            'propagate': True,
        },
    },
}



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': secrets['DB_NAME'],
        'USER': secrets['DB_USER'],
        'PASSWORD': secrets['DB_PASSWORD'],
        'HOST': secrets['DB_HOST'],
        'PORT': secrets['DB_PORT'],
    }
}



"""
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
"""
"""
{
    "SECRET_KEY": "django-insecure-@+-v-13m^%@j)m739u)=o@k2ud%z2yudgu5dc*$*@-(86n8l+-",
    "DB_NAME": "boongmark",
    "DB_USER": "dbmasteruser",
    "DB_PASSWORD": ";Z}gl4RjjaV8!ST40QoCRY|*yA{t?8qC",
    "DB_HOST": "ls-b846cf94dffffe6800c27ade9ff95ade0f2c79ba.cdqzykhsiown.ap-northeast-2.rds.amazonaws.com",
    "DB_PORT": "5432",
    "YOUTUBE_API_KEY": "AIzaSyAgQOLRQYizg-LK_0hmWJa5nLfE18wZD3o"
}
"""

