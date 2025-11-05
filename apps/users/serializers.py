"""
Serializers for Users app
Created by Cavin Otieno
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    class Meta:
        model = Profile
        fields = [
            'address', 'city', 'country', 'postal_code',
            'receive_notifications', 'receive_marketing_emails'
        ]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model"""
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone_number', 'avatar', 'bio', 'is_premium',
            'email_verified', 'date_joined', 'profile'
        ]
        read_only_fields = ['id', 'is_premium', 'email_verified', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user
