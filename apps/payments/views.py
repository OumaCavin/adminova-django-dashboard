"""
API views for Payments app
Created by Cavin Otieno
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json
import logging

from .models import MpesaPayment
from .serializers import MpesaPaymentSerializer, InitiatePaymentSerializer
from .mpesa_service import MpesaService
from apps.subscriptions.models import Plan, Subscription

logger = logging.getLogger(__name__)


class MpesaPaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for M-Pesa payments"""
    serializer_class = MpesaPaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MpesaPayment.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def initiate(self, request):
        """Initiate M-Pesa STK Push payment"""
        serializer = InitiatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        amount = serializer.validated_data['amount']
        plan_id = serializer.validated_data.get('plan_id')
        description = serializer.validated_data.get('description', 'Payment')
        
        # Create or get subscription if plan_id is provided
        subscription = None
        if plan_id:
            try:
                plan = Plan.objects.get(id=plan_id, is_active=True)
                amount = plan.price  # Use plan price
                description = f"Subscription: {plan.name}"
                
                # Create pending subscription
                subscription = Subscription.objects.create(
                    user=request.user,
                    plan=plan,
                    status='trialing'
                )
            except Plan.DoesNotExist:
                return Response(
                    {'error': 'Invalid plan ID'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            # Initiate STK Push
            mpesa_service = MpesaService()
            payment = mpesa_service.initiate_stk_push(
                phone_number=phone_number,
                amount=amount,
                account_reference=f"USER{request.user.id}",
                transaction_desc=description,
                user=request.user
            )
            
            # Link payment to subscription
            if subscription:
                payment.subscription = subscription
                payment.save()
            
            return Response({
                'message': 'STK Push initiated successfully. Please check your phone.',
                'checkout_request_id': payment.checkout_request_id,
                'amount': str(payment.amount),
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error initiating payment: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def mpesa_callback(request):
    """
    M-Pesa callback endpoint
    Handles callbacks from Safaricom Daraja API
    """
    try:
        callback_data = json.loads(request.body.decode('utf-8'))
        logger.info(f"Received M-Pesa callback: {callback_data}")
        
        # Process callback
        mpesa_service = MpesaService()
        success = mpesa_service.process_callback(callback_data)
        
        if success:
            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Success'})
        else:
            return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Failed'})
            
    except Exception as e:
        logger.error(f"Error processing M-Pesa callback: {str(e)}")
        return JsonResponse({'ResultCode': 1, 'ResultDesc': str(e)})
