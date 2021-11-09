"""
WSGI config for api_et project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os



from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_et.settings')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_et.settings.production")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")


application = get_wsgi_application()
