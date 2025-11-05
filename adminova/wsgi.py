"""
WSGI config for Adminova project.
Created by Cavin Otieno
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminova.settings.production')

application = get_wsgi_application()
