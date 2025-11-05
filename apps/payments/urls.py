"""
URL configuration for Payments app
Created by Cavin Otieno
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MpesaPaymentViewSet, mpesa_callback

router = DefaultRouter()
router.register(r'mpesa', MpesaPaymentViewSet, basename='mpesa-payment')

urlpatterns = [
    path('', include(router.urls)),
    path('mpesa/callback/', mpesa_callback, name='mpesa-callback'),
]
