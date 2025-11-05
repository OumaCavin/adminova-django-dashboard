"""
Admin configuration for Payments app
Created by Cavin Otieno
"""
from django.contrib import admin
from .models import MpesaPayment, MpesaAccessToken


@admin.register(MpesaPayment)
class MpesaPaymentAdmin(admin.ModelAdmin):
    """Admin configuration for MpesaPayment model"""
    list_display = [
        'user',
        'amount',
        'phone_number',
        'status',
        'mpesa_receipt_number',
        'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = [
        'user__email',
        'phone_number',
        'checkout_request_id',
        'merchant_request_id',
        'mpesa_receipt_number'
    ]
    readonly_fields = [
        'checkout_request_id',
        'merchant_request_id',
        'mpesa_receipt_number',
        'result_code',
        'result_description',
        'transaction_date',
        'metadata',
        'created_at',
        'updated_at'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(MpesaAccessToken)
class MpesaAccessTokenAdmin(admin.ModelAdmin):
    """Admin configuration for MpesaAccessToken model"""
    list_display = ['access_token_preview', 'expires_at', 'created_at']
    readonly_fields = ['access_token', 'expires_at', 'created_at']
    ordering = ['-created_at']
    
    def access_token_preview(self, obj):
        """Show preview of access token"""
        return f"{obj.access_token[:20]}..." if len(obj.access_token) > 20 else obj.access_token
    access_token_preview.short_description = 'Access Token'
