"""
Subscription middleware for Adminova
Checks user subscription status and enforces access control
Created by Cavin Otieno
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class SubscriptionCheckMiddleware:
    """
    Middleware to check if user has an active subscription
    before accessing protected views
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that don't require subscription check
        self.exempt_urls = [
            '/admin/',
            '/api/',
            '/accounts/login/',
            '/accounts/logout/',
            '/accounts/signup/',
            '/pricing/',
            '/checkout/',
        ]
    
    def __call__(self, request):
        # Skip for exempt URLs
        if any(request.path.startswith(url) for url in self.exempt_urls):
            return self.get_response(request)
        
        # Skip for unauthenticated users
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Skip for staff/superusers
        if request.user.is_staff or request.user.is_superuser:
            return self.get_response(request)
        
        # Check if user has an active subscription
        has_active_subscription = request.user.subscriptions.filter(
            status='active'
        ).exists()
        
        if not has_active_subscription:
            messages.warning(request, 'You need an active subscription to access this feature.')
            return redirect('pricing')
        
        response = self.get_response(request)
        return response
