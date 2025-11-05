"""
Dashboard views for Adminova
Created by Cavin Otieno
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.subscriptions.models import Plan, Subscription
from apps.payments.models import MpesaPayment


def home(request):
    """Home page view"""
    plans = Plan.objects.filter(is_active=True).order_by('display_order', 'price')
    return render(request, 'dashboard/home.html', {
        'plans': plans,
    })


@login_required
def dashboard(request):
    """Main dashboard view"""
    active_subscription = Subscription.objects.filter(
        user=request.user,
        status='active'
    ).first()
    
    recent_payments = MpesaPayment.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    return render(request, 'dashboard/dashboard.html', {
        'active_subscription': active_subscription,
        'recent_payments': recent_payments,
    })


def pricing(request):
    """Pricing page view"""
    plans = Plan.objects.filter(is_active=True).order_by('display_order', 'price')
    return render(request, 'dashboard/pricing.html', {
        'plans': plans,
    })
