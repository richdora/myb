from .base import *


ALLOWED_HOSTS =[]
STATIC_ROOT = os.path.join(BASE_DIR, 'local_staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]