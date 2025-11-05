# Adminova API Testing Guide

## Overview

This guide provides comprehensive instructions for testing the Adminova API endpoints using various tools and methods.

## Getting Started

### 1. Start the Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`

### 2. API Documentation

Access interactive API documentation:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Authentication

### Get Authentication Token

**Endpoint**: `POST /api/auth/token/`

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

**Response**:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Using the Token

Include the token in subsequent requests:
```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  http://localhost:8000/api/auth/users/me/
```

## User Management

### Register New User

**Endpoint**: `POST /api/auth/users/`

```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Get Current User

**Endpoint**: `GET /api/auth/users/me/`

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/auth/users/me/
```

### Update User Profile

**Endpoint**: `PUT /api/auth/users/update_profile/`

```bash
curl -X PUT http://localhost:8000/api/auth/users/update_profile/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Nairobi",
    "country": "Kenya",
    "address": "123 Main St"
  }'
```

## Subscription Plans

### List All Plans

**Endpoint**: `GET /api/plans/`

```bash
curl http://localhost:8000/api/plans/
```

**Response**:
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "Starter",
      "slug": "starter",
      "description": "Perfect for individuals",
      "price": "499.00",
      "billing_cycle": "monthly",
      "features": {
        "users": 1,
        "storage": "1GB"
      },
      "is_active": true,
      "is_popular": false
    }
  ]
}
```

### Get Specific Plan

**Endpoint**: `GET /api/plans/{slug}/`

```bash
curl http://localhost:8000/api/plans/professional/
```

## Subscriptions

### Get Active Subscription

**Endpoint**: `GET /api/plans/subscriptions/active/`

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/plans/subscriptions/active/
```

### List User Subscriptions

**Endpoint**: `GET /api/plans/subscriptions/`

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/plans/subscriptions/
```

### Cancel Subscription

**Endpoint**: `POST /api/plans/subscriptions/{id}/cancel/`

```bash
curl -X POST \
  -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/plans/subscriptions/1/cancel/
```

## M-Pesa Payments

### Initiate Payment

**Endpoint**: `POST /api/payments/mpesa/initiate/`

```bash
curl -X POST http://localhost:8000/api/payments/mpesa/initiate/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "254712345678",
    "amount": "100.00",
    "description": "Test Payment"
  }'
```

**Response**:
```json
{
  "message": "STK Push initiated successfully. Please check your phone.",
  "checkout_request_id": "ws_CO_12345678",
  "amount": "100.00"
}
```

### Initiate Subscription Payment

**Endpoint**: `POST /api/payments/mpesa/initiate/`

```bash
curl -X POST http://localhost:8000/api/payments/mpesa/initiate/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "254712345678",
    "plan_id": 1
  }'
```

### List User Payments

**Endpoint**: `GET /api/payments/mpesa/`

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/payments/mpesa/
```

**Response**:
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "amount": "499.00",
      "phone_number": "254712345678",
      "status": "completed",
      "mpesa_receipt_number": "QGH12345AB",
      "checkout_request_id": "ws_CO_12345678",
      "description": "Subscription: Starter",
      "created_at": "2025-11-05T10:30:00Z"
    }
  ]
}
```

### Get Payment Details

**Endpoint**: `GET /api/payments/mpesa/{id}/`

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/payments/mpesa/1/
```

## Testing with Python

### Using requests library

```python
import requests

# Base URL
BASE_URL = 'http://localhost:8000/api'

# 1. Register user
register_data = {
    'email': 'test@example.com',
    'username': 'testuser',
    'password': 'SecurePass123!',
    'password_confirm': 'SecurePass123!',
    'first_name': 'Test',
    'last_name': 'User'
}
response = requests.post(f'{BASE_URL}/auth/users/', json=register_data)
print(f"Registration: {response.status_code}")

# 2. Get token
token_data = {
    'username': 'testuser',
    'password': 'SecurePass123!'
}
response = requests.post(f'{BASE_URL}/auth/token/', json=token_data)
token = response.json()['token']
print(f"Token: {token}")

# 3. Set headers
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# 4. Get subscription plans
response = requests.get(f'{BASE_URL}/plans/', headers=headers)
plans = response.json()['results']
print(f"Plans: {len(plans)}")

# 5. Initiate payment
payment_data = {
    'phone_number': '254712345678',
    'plan_id': plans[0]['id']
}
response = requests.post(
    f'{BASE_URL}/payments/mpesa/initiate/',
    json=payment_data,
    headers=headers
)
print(f"Payment initiated: {response.json()}")
```

## Testing with Postman

### 1. Import Collection

Create a new Postman collection with these requests:

1. **Register User** - POST `/api/auth/users/`
2. **Get Token** - POST `/api/auth/token/`
3. **Get Plans** - GET `/api/plans/`
4. **Initiate Payment** - POST `/api/payments/mpesa/initiate/`

### 2. Set Environment Variables

- `base_url`: `http://localhost:8000/api`
- `token`: (set after login)

### 3. Use Collection Variables

In Authorization header:
```
Token {{token}}
```

## Testing M-Pesa Callbacks

### 1. Use ngrok for Local Testing

```bash
ngrok http 8000
```

### 2. Update Callback URL

Update `.env`:
```env
MPESA_CALLBACK_URL=https://your-ngrok-url.ngrok-free.app/api/payments/mpesa/callback/
```

### 3. Test Callback Manually

```bash
curl -X POST http://localhost:8000/api/payments/mpesa/callback/ \
  -H "Content-Type: application/json" \
  -d '{
    "Body": {
      "stkCallback": {
        "MerchantRequestID": "12345-67890-1",
        "CheckoutRequestID": "ws_CO_12345678",
        "ResultCode": 0,
        "ResultDesc": "The service request is processed successfully.",
        "CallbackMetadata": {
          "Item": [
            {
              "Name": "Amount",
              "Value": 100
            },
            {
              "Name": "MpesaReceiptNumber",
              "Value": "QGH12345AB"
            },
            {
              "Name": "TransactionDate",
              "Value": 20251105103000
            },
            {
              "Name": "PhoneNumber",
              "Value": 254712345678
            }
          ]
        }
      }
    }
  }'
```

## Common Test Scenarios

### Scenario 1: Complete Subscription Flow

1. Register user
2. Get authentication token
3. View available plans
4. Initiate payment for a plan
5. Complete M-Pesa payment on phone
6. Check subscription status
7. Verify payment record

### Scenario 2: Payment Failure

1. Initiate payment
2. Cancel on phone
3. Check payment status (should be 'failed')
4. Verify subscription not activated

### Scenario 3: Multiple Subscriptions

1. Create active subscription
2. Attempt to create another subscription
3. Cancel first subscription
4. Create new subscription

## Error Responses

### 400 Bad Request

```json
{
  "phone_number": [
    "Phone number must start with 254"
  ]
}
```

### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found

```json
{
  "detail": "No active subscription found."
}
```

### 500 Internal Server Error

```json
{
  "error": "Failed to initiate M-Pesa payment: Connection timeout"
}
```

## Performance Testing

### Using Apache Bench

```bash
# Test authentication endpoint
ab -n 100 -c 10 -H "Content-Type: application/json" \
  -p login.json \
  http://localhost:8000/api/auth/token/
```

### Using Locust

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class AdminovaUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/auth/token/", json={
            "username": "testuser",
            "password": "password123"
        })
        self.token = response.json()["token"]
        self.headers = {"Authorization": f"Token {self.token}"}
    
    @task
    def view_plans(self):
        self.client.get("/api/plans/", headers=self.headers)
    
    @task
    def view_profile(self):
        self.client.get("/api/auth/users/me/", headers=self.headers)
```

Run:
```bash
locust -f locustfile.py
```

## Debugging Tips

1. **Check Django logs**:
```bash
python manage.py runserver --verbosity 3
```

2. **Enable SQL logging**:
Add to settings:
```python
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        },
    },
}
```

3. **Test M-Pesa service directly**:
```python
from apps.payments.mpesa_service import MpesaService

service = MpesaService()
token = service.get_access_token()
print(f"Access Token: {token}")
```

## Support

For API testing support, contact:
- Email: cavin.otieno012@gmail.com
- GitHub Issues: https://github.com/OumaCavin/adminova-django-dashboard/issues
