"""
URL configuration for Dashboard app
Created by Cavin Otieno
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pricing/', views.pricing, name='pricing'),
]
