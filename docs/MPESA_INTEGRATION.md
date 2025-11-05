# M-Pesa Integration Guide for Adminova

## Overview

This guide provides comprehensive instructions for integrating Safaricom's M-Pesa payment gateway into the Adminova Django Dashboard application.

## Prerequisites

1. **Daraja Account**: Register at [Safaricom Daraja Portal](https://developer.safaricom.co.ke/)
2. **M-Pesa Shortcode**: Paybill or Till number
3. **API Credentials**: Consumer Key, Consumer Secret, and Passkey

## Environment Setup

### Sandbox Configuration

For testing, use sandbox credentials in your `.env` file:

```env
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your_sandbox_consumer_key
MPESA_CONSUMER_SECRET=your_sandbox_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_sandbox_passkey
MPESA_CALLBACK_URL=https://your-ngrok-url.ngrok-free.app/api/payments/mpesa/callback/
```

### Local Development with ngrok

1. **Install ngrok**: Download from [ngrok.com](https://ngrok.com/)

2. **Start your Django server**:
```bash
python manage.py runserver
```

3. **Start ngrok tunnel**:
```bash
ngrok http 8000
```

4. **Update callback URL** in `.env`:
```env
MPESA_CALLBACK_URL=https://your-unique-id.ngrok-free.app/api/payments/mpesa/callback/
```

## API Integration Flow

### 1. STK Push Initiation

Initiate payment from your frontend:

```python
import requests

url = 'http://localhost:8000/api/payments/mpesa/initiate/'
headers = {
    'Authorization': 'Token your-auth-token',
    'Content-Type': 'application/json'
}
data = {
    'phone_number': '254712345678',
    'amount': 100,
    'plan_id': 1,  # Optional: for subscription payments
    'description': 'Test Payment'
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### 2. User Experience Flow

1. User initiates payment via API or web interface
2. STK Push is sent to user's phone
3. User receives prompt to enter M-Pesa PIN
4. User authorizes payment
5. M-Pesa processes transaction
6. Callback is sent to your server
7. Payment status is updated in database
8. Subscription is activated (if applicable)

### 3. Callback Processing

The system automatically handles M-Pesa callbacks:

- **Success**: Payment marked as completed, subscription activated
- **Failure**: Payment marked as failed, user notified
- **Idempotency**: Duplicate callbacks are handled gracefully

## Testing

### Test Scenarios

1. **Successful Payment**
```bash
curl -X POST http://localhost:8000/api/payments/mpesa/initiate/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "254712345678",
    "amount": 100,
    "description": "Test Payment"
  }'
```

2. **Check Payment Status**
```bash
curl http://localhost:8000/api/payments/mpesa/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Sandbox Test Numbers

Use these phone numbers for testing:
- Success: `254708374149`
- Insufficient Balance: `254708374149`
- User Cancelled: `254708374149`

## Production Deployment

### Go-Live Checklist

- [ ] Obtain production credentials from Safaricom
- [ ] Complete IP whitelisting
- [ ] Update environment variables
- [ ] Configure production callback URL with HTTPS
- [ ] Test with real phone numbers
- [ ] Set up monitoring and logging
- [ ] Configure error notifications

### Production Configuration

Update `.env` for production:

```env
MPESA_ENVIRONMENT=production
MPESA_CONSUMER_KEY=your_production_consumer_key
MPESA_CONSUMER_SECRET=your_production_consumer_secret
MPESA_SHORTCODE=your_production_shortcode
MPESA_PASSKEY=your_production_passkey
MPESA_CALLBACK_URL=https://yourdomain.com/api/payments/mpesa/callback/
```

### Security Considerations

1. **HTTPS Only**: Callback URL must use HTTPS
2. **Token Caching**: Access tokens are cached to reduce API calls
3. **Idempotency**: Duplicate callbacks are handled
4. **Logging**: All transactions are logged for audit trail
5. **Error Handling**: Comprehensive error handling and notifications

## Monitoring

### Check Payment Logs

```bash
python manage.py shell
```

```python
from apps.payments.models import MpesaPayment

# Recent payments
recent = MpesaPayment.objects.all()[:10]
for payment in recent:
    print(f"{payment.user.email}: {payment.amount} - {payment.status}")

# Failed payments
failed = MpesaPayment.objects.filter(status='failed')
print(f"Failed payments: {failed.count()}")
```

### Admin Interface

Access the Django admin to monitor payments:
1. Go to http://localhost:8000/admin/
2. Navigate to "M-Pesa Payments"
3. View, filter, and search all transactions

## Troubleshooting

### Common Issues

1. **Callback not received**
   - Check ngrok is running
   - Verify callback URL in .env
   - Check firewall/network settings

2. **Invalid Access Token**
   - Verify consumer key and secret
   - Check token expiry
   - Review API credentials

3. **STK Push fails**
   - Validate phone number format (254XXXXXXXXX)
   - Check amount is valid (>= 1 KSh)
   - Verify shortcode and passkey

### Debug Mode

Enable debug logging in settings:

```python
LOGGING = {
    'loggers': {
        'apps.payments': {
            'level': 'DEBUG',
        },
    },
}
```

## Support

For M-Pesa integration support:
- **Email**: cavin.otieno012@gmail.com
- **Daraja Support**: https://developer.safaricom.co.ke/support

## References

- [Daraja API Documentation](https://developer.safaricom.co.ke/docs)
- [M-Pesa STK Push Guide](https://developer.safaricom.co.ke/APIs/MpesaExpressSimulate)
- [Safaricom Go-Live Process](https://developer.safaricom.co.ke/go-live)
