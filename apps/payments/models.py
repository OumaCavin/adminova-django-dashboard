"""
M-Pesa Payment models for Adminova
Manages M-Pesa transactions and payment records
Created by Cavin Otieno
"""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class MpesaPayment(TimeStampedModel):
    """
    M-Pesa payment transaction model
    Tracks all M-Pesa STK Push transactions
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mpesa_payments'
    )
    subscription = models.ForeignKey(
        'subscriptions.Subscription',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )
    
    # Amount and phone number
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Amount in KSh')
    phone_number = models.CharField(max_length=15, help_text='Phone number in format 2547XXXXXXXX')
    
    # M-Pesa API identifiers
    checkout_request_id = models.CharField(max_length=100, unique=True, db_index=True)
    merchant_request_id = models.CharField(max_length=100, unique=True, db_index=True)
    mpesa_receipt_number = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    
    # Transaction status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result_code = models.IntegerField(null=True, blank=True)
    result_description = models.TextField(blank=True)
    
    # Callback metadata
    transaction_date = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Description
    description = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'mpesa_payments'
        verbose_name = 'M-Pesa Payment'
        verbose_name_plural = 'M-Pesa Payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['checkout_request_id']),
        ]
    
    def __str__(self):
        return f"Payment {self.mpesa_receipt_number or self.checkout_request_id} - KSh {self.amount} ({self.status})"
    
    def is_successful(self):
        """Check if payment was successful"""
        return self.status == 'completed' and self.result_code == 0
    
    def mark_completed(self, receipt_number, transaction_date, metadata=None):
        """Mark payment as completed"""
        self.status = 'completed'
        self.result_code = 0
        self.mpesa_receipt_number = receipt_number
        self.transaction_date = transaction_date
        if metadata:
            self.metadata = metadata
        self.save()
    
    def mark_failed(self, result_code, result_description):
        """Mark payment as failed"""
        self.status = 'failed'
        self.result_code = result_code
        self.result_description = result_description
        self.save()


class MpesaAccessToken(TimeStampedModel):
    """
    Stores M-Pesa OAuth access tokens with expiry tracking
    """
    access_token = models.TextField()
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'mpesa_access_tokens'
        verbose_name = 'M-Pesa Access Token'
        verbose_name_plural = 'M-Pesa Access Tokens'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Token expires at {self.expires_at}"
    
    def is_expired(self):
        """Check if token has expired"""
        from django.utils import timezone
        return timezone.now() >= self.expires_at
