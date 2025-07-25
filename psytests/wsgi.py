"""
WSGI config for psytests project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use Vercel settings when deployed on Vercel, otherwise use dev settings
settings_module = 'psytests.settings.vercel' if 'VERCEL' in os.environ else 'psytests.settings.dev'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()

# Vercel compatibility
app = application
