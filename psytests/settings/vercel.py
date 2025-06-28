from .common import *
import dj_database_url
import os

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app', '.now.sh']

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-enn_1_qy&r1^^fqcus4@s^mb5&5%bg1--mogq=b**8be^w)l$0")

SITE_ID = 1

# Database configuration for Vercel (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE'),
        'USER': os.environ.get('PGUSER'),
        'PASSWORD': os.environ.get('PGPASSWORD'),
        'HOST': os.environ.get('PGHOST'),
        'PORT': os.environ.get('PGPORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Security settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Static files configuration for Vercel
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Use WhiteNoise to serve static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
