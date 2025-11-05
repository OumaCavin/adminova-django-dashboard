"""
Serializers for Payments app
Created by Cavin Otieno
"""
from rest_framework import serializers
from .models import MpesaPayment


class MpesaPaymentSerializer(serializers.ModelSerializer):
    """Serializer for M-Pesa payments"""
    class Meta:
        model = MpesaPayment
        fields = [
            'id', 'amount', 'phone_number', 'status',
            'mpesa_receipt_number', 'checkout_request_id',
            'description', 'created_at'
        ]
        read_only_fields = [
            'id', 'status', 'mpesa_receipt_number',
            'checkout_request_id', 'created_at'
        ]


class InitiatePaymentSerializer(serializers.Serializer):
    """Serializer for initiating M-Pesa payment"""
    phone_number = serializers.CharField(
        max_length=15,
        help_text='Phone number in format 2547XXXXXXXX'
    )
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=1,
        help_text='Amount in KSh'
    )
    plan_id = serializers.IntegerField(
        required=False,
        help_text='Subscription plan ID (optional)'
    )
    description = serializers.CharField(
        max_length=255,
        required=False,
        default='Payment'
    )
    
    def validate_phone_number(self, value):
        """Validate phone number format"""
        if not value.startswith('254'):
            raise serializers.ValidationError('Phone number must start with 254')
        if len(value) != 12:
            raise serializers.ValidationError('Phone number must be 12 digits (254XXXXXXXXX)')
        return value
