"""
API views for Subscriptions app
Created by Cavin Otieno
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for subscription plans"""
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet for user subscriptions"""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get user's active subscription"""
        subscription = Subscription.objects.filter(
            user=request.user,
            status='active'
        ).first()
        
        if subscription:
            serializer = self.get_serializer(subscription)
            return Response(serializer.data)
        return Response({'detail': 'No active subscription found.'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a subscription"""
        subscription = self.get_object()
        subscription.cancel()
        return Response({'detail': 'Subscription canceled successfully.'})
