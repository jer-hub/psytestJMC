from .common import *

DEBUG = True
# DEBUG_PROPAGATE_EXCEPTIONS = True
# ALLOWED_HOSTS = ["127.0.0.1"]

SECRET_KEY = 'django-insecure-enn_1_qy&r1^^fqcus4@s^mb5&5%bg1--mogq=b**8be^w)l$0'

SITE_ID = 2

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

USE_TZ=True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False