# End-to-End Testing Guide for Adminova Django Dashboard

## Overview

This guide provides step-by-step instructions for comprehensive testing of the Adminova Django Dashboard, including M-Pesa payment integration and subscription activation flow.

## Prerequisites

- Completed installation (run `bash setup.sh` or `bash deploy_and_test.sh`)
- Ngrok installed for M-Pesa callback testing
- M-Pesa sandbox credentials (or production credentials)
- Postman, curl, or Python requests library

## Testing Environment Setup

### 1. Configure Database Connection

The application is configured to use Supabase PostgreSQL by default:

```env
DB_HOST=brxiwidkpkmyqkbzdhht.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=Airtel!23!23
DB_PORT=5432
```

Test the database connection:
```bash
python manage.py dbshell
```

### 2. Set Up Ngrok for M-Pesa Callbacks

M-Pesa requires a publicly accessible HTTPS URL for callbacks. Use ngrok for local testing:

1. **Install ngrok**:
```bash
# Download from https://ngrok.com/download
# Or install via snap on Linux:
sudo snap install ngrok
```

2. **Start ngrok**:
```bash
ngrok http 8000
```

3. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok-free.app`)

4. **Update .env** with the ngrok URL:
```env
MPESA_CALLBACK_URL=https://abc123.ngrok-free.app/api/payments/mpesa/callback/
```

5. **Restart Django server** to apply changes

### 3. Configure M-Pesa Credentials

Update `.env` with your M-Pesa credentials:

**For Sandbox Testing**:
```env
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your_sandbox_consumer_key
MPESA_CONSUMER_SECRET=your_sandbox_consumer_secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your_sandbox_passkey
```

**For Production**:
```env
MPESA_ENVIRONMENT=production
MPESA_CONSUMER_KEY=your_production_consumer_key
MPESA_CONSUMER_SECRET=your_production_consumer_secret
MPESA_SHORTCODE=your_production_shortcode
MPESA_PASSKEY=your_production_passkey
```

## Testing Flow

### Phase 1: Basic Application Testing

#### 1.1 Start the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations (if not done)
python manage.py migrate

# Start development server
python manage.py runserver
```

Access URLs:
- Application: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- API Docs: http://127.0.0.1:8000/api/docs/

#### 1.2 Test Admin Interface

1. Go to http://127.0.0.1:8000/admin/
2. Login with default credentials:
   - Username: `admin`
   - Password: `admin123`
3. Verify sections:
   - Users
   - Profiles
   - Subscription Plans
   - Subscriptions
   - M-Pesa Payments

#### 1.3 Test API Documentation

1. Go to http://127.0.0.1:8000/api/docs/
2. Explore available endpoints
3. Test authentication endpoint

### Phase 2: API Testing

#### 2.1 User Registration

```bash
curl -X POST http://127.0.0.1:8000/api/auth/users/ \
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

**Expected Response**: 201 Created with user data

#### 2.2 Get Authentication Token

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123!"
  }'
```

**Expected Response**:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

Save this token for subsequent requests.

#### 2.3 View Subscription Plans

```bash
curl http://127.0.0.1:8000/api/plans/
```

**Expected Response**: List of all available subscription plans

### Phase 3: M-Pesa Payment Testing

This is the critical testing phase that validates the complete payment and subscription activation flow.

#### 3.1 Verify Ngrok is Running

Check that ngrok is running and the callback URL is accessible:

```bash
# In another terminal
curl https://your-ngrok-url.ngrok-free.app/api/payments/mpesa/callback/
```

You should see a 405 Method Not Allowed (because GET is not allowed, but POST is).

#### 3.2 Initiate M-Pesa Payment

Replace `YOUR_TOKEN` with the token from step 2.2:

```bash
curl -X POST http://127.0.0.1:8000/api/payments/mpesa/initiate/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "254712345678",
    "plan_id": 1
  }'
```

**Expected Response**:
```json
{
  "message": "STK Push initiated successfully. Please check your phone.",
  "checkout_request_id": "ws_CO_12345678",
  "amount": "499.00"
}
```

#### 3.3 Complete Payment on Phone

1. **Check your M-Pesa registered phone**
2. **You should receive an STK Push prompt**
3. **Enter your M-Pesa PIN** to complete payment
4. **Wait for confirmation**

#### 3.4 Monitor Callback Processing

Watch the Django server console for callback logs:

```
INFO apps.payments Received M-Pesa callback: {...}
INFO apps.payments Payment ws_CO_12345678 completed. Receipt: QGH12345AB
INFO apps.payments Activated subscription 1
```

#### 3.5 Verify Payment Status

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/payments/mpesa/
```

**Expected Response**: Payment with status "completed"

#### 3.6 Verify Subscription Activation

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/plans/subscriptions/active/
```

**Expected Response**: Active subscription linked to the payment

### Phase 4: Subscription Management Testing

#### 4.1 View User Subscriptions

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/plans/subscriptions/
```

#### 4.2 Cancel Subscription

```bash
curl -X POST \
  -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/plans/subscriptions/1/cancel/
```

#### 4.3 Verify Cancellation

Check that subscription status is now "canceled":

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/plans/subscriptions/1/
```

### Phase 5: Error Handling Testing

#### 5.1 Test Invalid Phone Number

```bash
curl -X POST http://127.0.0.1:8000/api/payments/mpesa/initiate/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "0712345678",
    "plan_id": 1
  }'
```

**Expected Response**: 400 Bad Request with validation error

#### 5.2 Test User Cancellation

Initiate a payment but cancel on your phone. The callback should mark the payment as "failed".

#### 5.3 Test Insufficient Balance

Use a test phone number configured for insufficient balance in the M-Pesa sandbox.

### Phase 6: Admin Interface Testing

#### 6.1 View Payments in Admin

1. Go to http://127.0.0.1:8000/admin/payments/mpesapayment/
2. Verify payment records are visible
3. Check that metadata is stored correctly

#### 6.2 View Subscriptions in Admin

1. Go to http://127.0.0.1:8000/admin/subscriptions/subscription/
2. Verify subscription is linked to user and payment
3. Check subscription dates and status

#### 6.3 Manage Subscription Plans

1. Go to http://127.0.0.1:8000/admin/subscriptions/plan/
2. Create a new plan
3. Update pricing or features
4. Mark plans as active/inactive

## Testing Checklist

### Essential Tests

- [ ] Database connection successful
- [ ] Application starts without errors
- [ ] Admin interface accessible
- [ ] API documentation accessible
- [ ] User registration works
- [ ] Authentication token generation works
- [ ] Subscription plans are listed

### M-Pesa Integration Tests

- [ ] Ngrok URL is accessible
- [ ] STK Push initiates successfully
- [ ] Phone receives M-Pesa prompt
- [ ] Payment completion updates database
- [ ] Callback is processed correctly
- [ ] Subscription is activated automatically
- [ ] Payment status is "completed"
- [ ] M-Pesa receipt number is stored

### Edge Cases

- [ ] Invalid phone number validation
- [ ] User payment cancellation handled
- [ ] Insufficient balance handled
- [ ] Duplicate callback idempotency
- [ ] Network timeout handling
- [ ] Invalid plan ID validation

### Security Tests

- [ ] Unauthenticated requests rejected
- [ ] CSRF protection active
- [ ] Token authentication required
- [ ] Admin requires authentication
- [ ] Sensitive data not exposed in logs

## Troubleshooting

### Issue: Database Connection Fails

**Symptoms**: `django.db.utils.OperationalError: could not connect to server`

**Solutions**:
1. Verify Supabase credentials in `.env`
2. Check network connectivity
3. Verify Supabase project is active
4. Try connecting with `psql` directly

### Issue: No STK Push Received

**Symptoms**: API call succeeds but no phone prompt

**Solutions**:
1. Verify phone number format (254XXXXXXXXX)
2. Check M-Pesa credentials are correct
3. Ensure phone has active M-Pesa
4. Check Daraja API sandbox status
5. Verify shortcode and passkey

### Issue: Callback Not Received

**Symptoms**: Payment completed but not reflected in database

**Solutions**:
1. Check ngrok is running and accessible
2. Verify callback URL in `.env` is correct
3. Check Django server logs for callback
4. Test callback URL manually with curl
5. Verify no firewall blocking ngrok

### Issue: Migrations Fail

**Symptoms**: `django.db.migrations.exceptions.InconsistentMigrationHistory`

**Solutions**:
1. Delete migration files (keep __init__.py)
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. If persistent, reset database

## Performance Testing

### Load Testing with Locust

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class AdminovaUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        response = self.client.post("/api/auth/token/", json={
            "username": "testuser",
            "password": "SecurePass123!"
        })
        self.token = response.json()["token"]
        self.headers = {"Authorization": f"Token {self.token}"}
    
    @task(3)
    def view_plans(self):
        self.client.get("/api/plans/", headers=self.headers)
    
    @task(2)
    def view_profile(self):
        self.client.get("/api/auth/users/me/", headers=self.headers)
    
    @task(1)
    def view_subscription(self):
        self.client.get("/api/plans/subscriptions/active/", headers=self.headers)
```

Run:
```bash
locust -f locustfile.py
```

### API Response Time Testing

```bash
# Test plan listing endpoint
time curl http://127.0.0.1:8000/api/plans/

# Test with authentication
time curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/auth/users/me/
```

## Production Deployment Testing

Before deploying to production:

1. **Update settings to production**:
   ```env
   DEBUG=False
   DJANGO_SETTINGS_MODULE=adminova.settings.production
   MPESA_ENVIRONMENT=production
   ```

2. **Test with production M-Pesa credentials**

3. **Verify SSL/HTTPS is configured**

4. **Test all endpoints on production URL**

5. **Monitor logs for errors**

6. **Perform smoke tests after deployment**

## Continuous Monitoring

After deployment:

1. **Monitor payment success rate**
2. **Track callback processing time**
3. **Watch for M-Pesa API errors**
4. **Monitor database connections**
5. **Check server resource usage**
6. **Review user registration/login patterns**

## Support

For testing support:
- Email: cavin.otieno012@gmail.com
- GitHub: https://github.com/OumaCavin/adminova-django-dashboard
- Check logs: `tail -f /var/log/django/adminova.log`

## Testing Status

| Test Category | Status | Notes |
|--------------|--------|-------|
| Basic Functionality | ⏳ Pending | Run setup and basic tests |
| API Endpoints | ⏳ Pending | Test all documented endpoints |
| M-Pesa Integration | ⏳ Pending | Critical: Test STK Push end-to-end |
| Subscription Flow | ⏳ Pending | Verify activation after payment |
| Error Handling | ⏳ Pending | Test edge cases |
| Security | ⏳ Pending | Verify authentication |
| Performance | ⏳ Pending | Load testing |

---

**Created by Cavin Otieno**
Last Updated: November 2025
