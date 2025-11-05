"""
Context processors for Adminova
Provides site-wide context variables for templates
Created by Cavin Otieno
"""
from django.conf import settings


def site_settings(request):
    """
    Adds site settings to template context
    """
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_AUTHOR': settings.SITE_AUTHOR,
        'SITE_EMAIL': settings.SITE_EMAIL,
        'CURRENCY_SYMBOL': settings.CURRENCY_SYMBOL,
        'CURRENCY_CODE': settings.CURRENCY_CODE,
    }
