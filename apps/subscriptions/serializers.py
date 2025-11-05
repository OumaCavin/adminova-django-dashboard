"""
Serializers for Subscriptions app
Created by Cavin Otieno
"""
from rest_framework import serializers
from .models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for subscription plans"""
    class Meta:
        model = Plan
        fields = [
            'id', 'name', 'slug', 'description', 'price',
            'billing_cycle', 'features', 'is_active',
            'is_popular', 'display_order'
        ]
        read_only_fields = ['id', 'slug']


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for subscriptions"""
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'plan', 'plan_id', 'status', 'start_date',
            'end_date', 'auto_renew', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'start_date', 'end_date', 'created_at']
