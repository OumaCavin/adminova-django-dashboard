"""
Admin configuration for Users app
Created by Cavin Otieno
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model"""
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_premium', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'is_premium', 'email_verified']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'avatar', 'bio', 'email_verified', 'is_premium')}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profile model"""
    list_display = ['user', 'city', 'country', 'created_at']
    search_fields = ['user__email', 'user__username', 'city', 'country']
    list_filter = ['country', 'receive_notifications']
