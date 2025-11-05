"""
M-Pesa integration service for Adminova
Handles M-Pesa STK Push and callback processing
Created by Cavin Otieno
"""
import base64
import json
import logging
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from .models import MpesaPayment, MpesaAccessToken

logger = logging.getLogger(__name__)


class MpesaService:
    """Service class for M-Pesa integration"""
    
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.callback_url = settings.MPESA_CALLBACK_URL
        
        # Set base URLs based on environment
        if settings.MPESA_ENVIRONMENT == 'sandbox':
            self.base_url = 'https://sandbox.safaricom.co.ke'
        else:
            self.base_url = 'https://api.safaricom.co.ke'
    
    def get_access_token(self):
        """
        Get OAuth access token from M-Pesa API
        Implements token caching to reduce API calls
        """
        # Check if we have a valid cached token
        try:
            token_obj = MpesaAccessToken.objects.filter(
                expires_at__gt=timezone.now()
            ).latest('created_at')
            logger.info("Using cached M-Pesa access token")
            return token_obj.access_token
        except MpesaAccessToken.DoesNotExist:
            pass
        
        # Generate new token
        url = f'{self.base_url}/oauth/v1/generate?grant_type=client_credentials'
        auth_string = f'{self.consumer_key}:{self.consumer_secret}'
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        
        headers = {
            'Authorization': f'Basic {auth_base64}',
            'Content-Type': 'application/json',
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            access_token = data.get('access_token')
            expires_in = int(data.get('expires_in', 3600))
            
            # Cache the token
            MpesaAccessToken.objects.create(
                access_token=access_token,
                expires_at=timezone.now() + timedelta(seconds=expires_in - 60)  # Expire 1 minute early
            )
            
            logger.info("Generated new M-Pesa access token")
            return access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting M-Pesa access token: {str(e)}")
            raise Exception(f"Failed to get M-Pesa access token: {str(e)}")
    
    def generate_password(self, timestamp):
        """Generate password for STK Push request"""
        data_to_encode = f'{self.shortcode}{self.passkey}{timestamp}'
        encoded = base64.b64encode(data_to_encode.encode('utf-8'))
        return encoded.decode('utf-8')
    
    def initiate_stk_push(self, phone_number, amount, account_reference, transaction_desc, user):
        """
        Initiate STK Push request to M-Pesa
        
        Args:
            phone_number: Phone number in format 2547XXXXXXXX
            amount: Amount to charge in KSh
            account_reference: Reference for the transaction
            transaction_desc: Description of the transaction
            user: User object making the payment
        
        Returns:
            MpesaPayment object
        """
        # Get access token
        access_token = self.get_access_token()
        
        # Generate timestamp and password
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = self.generate_password(timestamp)
        
        # Prepare STK Push payload
        url = f'{self.base_url}/mpesa/stkpush/v1/processrequest'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
        
        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(amount),
            'PartyA': phone_number,
            'PartyB': self.shortcode,
            'PhoneNumber': phone_number,
            'CallBackURL': self.callback_url,
            'AccountReference': account_reference,
            'TransactionDesc': transaction_desc,
        }
        
        try:
            logger.info(f"Initiating STK Push for {phone_number}, Amount: {amount}")
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Create payment record
            payment = MpesaPayment.objects.create(
                user=user,
                amount=amount,
                phone_number=phone_number,
                checkout_request_id=data.get('CheckoutRequestID'),
                merchant_request_id=data.get('MerchantRequestID'),
                description=transaction_desc,
                status='pending',
            )
            
            logger.info(f"STK Push initiated successfully. Checkout Request ID: {payment.checkout_request_id}")
            return payment
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error initiating STK Push: {str(e)}")
            raise Exception(f"Failed to initiate M-Pesa payment: {str(e)}")
    
    def process_callback(self, callback_data):
        """
        Process M-Pesa callback from STK Push
        
        Args:
            callback_data: Callback payload from M-Pesa
        """
        try:
            body = callback_data.get('Body', {})
            stk_callback = body.get('stkCallback', {})
            
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')
            
            # Find payment record
            try:
                payment = MpesaPayment.objects.get(checkout_request_id=checkout_request_id)
            except MpesaPayment.DoesNotExist:
                logger.error(f"Payment not found for Checkout Request ID: {checkout_request_id}")
                return False
            
            # Check if already processed (idempotency)
            if payment.status != 'pending':
                logger.info(f"Payment {checkout_request_id} already processed. Status: {payment.status}")
                return True
            
            # Process based on result code
            if result_code == 0:
                # Success
                callback_metadata = stk_callback.get('CallbackMetadata', {})
                items = callback_metadata.get('Item', [])
                
                # Extract metadata
                metadata = {}
                for item in items:
                    name = item.get('Name')
                    value = item.get('Value')
                    metadata[name] = value
                
                receipt_number = metadata.get('MpesaReceiptNumber')
                transaction_date_str = str(metadata.get('TransactionDate', ''))
                
                # Parse transaction date
                transaction_date = None
                if transaction_date_str:
                    try:
                        transaction_date = datetime.strptime(transaction_date_str, '%Y%m%d%H%M%S')
                    except ValueError:
                        transaction_date = timezone.now()
                
                payment.mark_completed(receipt_number, transaction_date, metadata)
                logger.info(f"Payment {checkout_request_id} completed. Receipt: {receipt_number}")
                
                # Activate subscription if linked
                if payment.subscription:
                    payment.subscription.status = 'active'
                    payment.subscription.save()
                    logger.info(f"Activated subscription {payment.subscription.id}")
                
                return True
            else:
                # Failed
                payment.mark_failed(result_code, result_desc)
                logger.warning(f"Payment {checkout_request_id} failed. Code: {result_code}, Desc: {result_desc}")
                return False
                
        except Exception as e:
            logger.error(f"Error processing M-Pesa callback: {str(e)}")
            return False
