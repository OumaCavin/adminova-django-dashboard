"""
Admin configuration for Subscriptions app
Created by Cavin Otieno
"""
from django.contrib import admin
from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Admin configuration for Plan model"""
    list_display = ['name', 'price', 'billing_cycle', 'is_active', 'is_popular', 'display_order']
    list_filter = ['billing_cycle', 'is_active', 'is_popular']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order', 'price']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin configuration for Subscription model"""
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'auto_renew']
    list_filter = ['status', 'auto_renew', 'plan']
    search_fields = ['user__email', 'user__username']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    readonly_fields = ['created_at', 'updated_at']
