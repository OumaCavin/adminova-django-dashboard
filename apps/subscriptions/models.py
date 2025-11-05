"""
Subscription models for Adminova
Manages subscription plans and user subscriptions
Created by Cavin Otieno
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from apps.core.models import TimeStampedModel


class Plan(TimeStampedModel):
    """
    Subscription plan model
    """
    BILLING_CYCLE_CHOICES = [
        ('monthly', 'Monthly'),
        ('annually', 'Annually'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price in KSh')
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE_CHOICES, default='monthly')
    
    # Features stored as JSON
    features = models.JSONField(default=dict, help_text='Plan features and limits')
    
    # Display options
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'subscription_plans'
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'
        ordering = ['display_order', 'price']
    
    def __str__(self):
        return f"{self.name} - KSh {self.price}/{self.billing_cycle}"
    
    def get_duration_days(self):
        """Get the number of days for this plan's billing cycle"""
        if self.billing_cycle == 'monthly':
            return 30
        elif self.billing_cycle == 'annually':
            return 365
        return 30


class Subscription(TimeStampedModel):
    """
    User subscription model
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired'),
        ('trialing', 'Trialing'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trialing')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    
    # Auto-renewal
    auto_renew = models.BooleanField(default=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        """Set end_date based on plan duration if not set"""
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.get_duration_days())
        super().save(*args, **kwargs)
    
    def is_active(self):
        """Check if subscription is active"""
        return self.status == 'active' and self.end_date > timezone.now()
    
    def is_expired(self):
        """Check if subscription has expired"""
        return self.end_date <= timezone.now()
    
    def renew(self):
        """Renew the subscription for another billing cycle"""
        self.start_date = self.end_date
        self.end_date = self.start_date + timedelta(days=self.plan.get_duration_days())
        self.status = 'active'
        self.save()
    
    def cancel(self):
        """Cancel the subscription"""
        self.status = 'canceled'
        self.canceled_at = timezone.now()
        self.auto_renew = False
        self.save()
