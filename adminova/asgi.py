"""
ASGI config for Adminova project.
Created by Cavin Otieno
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminova.settings.production')

application = get_asgi_application()
