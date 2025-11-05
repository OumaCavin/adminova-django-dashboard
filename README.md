# Adminova Django Dashboard

![Adminova](https://img.shields.io/badge/Adminova-Django-green)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Django](https://img.shields.io/badge/Django-5.0%2B-darkgreen)

**Adminova** is a comprehensive Django admin dashboard application with subscription management and M-Pesa payment integration, built specifically for the Kenyan market.

Created by [Cavin Otieno](https://github.com/OumaCavin)

## Features

- **Custom User Management**: Extended user model with profiles and authentication
- **Subscription System**: Multiple subscription tiers with monthly and annual billing
- **M-Pesa Integration**: Full STK Push implementation with callback handling
- **RESTful API**: Complete API with Django REST Framework and OpenAPI documentation
- **Dual Database Support**: PostgreSQL (Supabase) and MySQL compatibility
- **Admin Interface**: Comprehensive Django admin customization
- **Security**: Token authentication, CSRF protection, and secure payment handling
- **Kenyan Localization**: KSh currency, Kenya timezone, and localized content

## Technology Stack

- **Backend**: Django 5.0+, Python 3.12+
- **API**: Django REST Framework, drf-spectacular
- **Database**: PostgreSQL (Supabase), MySQL
- **Payments**: Safaricom Daraja API (M-Pesa)
- **Authentication**: Token-based authentication
- **Static Files**: WhiteNoise
- **Server**: Gunicorn

## Quick Start

### Prerequisites

- Python 3.12 or higher
- PostgreSQL or MySQL
- M-Pesa API credentials (sandbox or production)
- Virtual environment tool (venv, virtualenv, or conda)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/OumaCavin/adminova-django-dashboard.git
cd adminova-django-dashboard
```

2. **Create and activate virtual environment**
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using virtualenv
virtualenv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements/local.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the application.

## Configuration

### Environment Variables

Key environment variables to configure in `.env`:

```env
# Django
SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=adminova.settings.local

# Database (PostgreSQL/Supabase)
DB_HOST=brxiwidkpkmyqkbzdhht.supabase.co
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_PORT=5432

# M-Pesa Configuration
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your-passkey
MPESA_CALLBACK_URL=https://your-domain.com/api/payments/mpesa/callback/
```

### M-Pesa Setup

1. **Sandbox Testing**
   - Register at [Daraja Portal](https://developer.safaricom.co.ke/)
   - Create a test app and get sandbox credentials
   - Use ngrok for local callback testing: `ngrok http 8000`

2. **Production**
   - Submit go-live request with required documentation
   - Get production credentials and shortcode
   - Configure IP whitelisting with Safaricom

## API Documentation

API documentation is available at:
- Swagger UI: http://127.0.0.1:8000/api/docs/
- ReDoc: http://127.0.0.1:8000/api/redoc/
- OpenAPI Schema: http://127.0.0.1:8000/api/schema/

### Key Endpoints

- `POST /api/auth/token/` - Get authentication token
- `GET /api/plans/` - List subscription plans
- `POST /api/payments/mpesa/initiate/` - Initiate M-Pesa payment
- `GET /api/auth/users/me/` - Get current user details

## Database Management

### PostgreSQL (Supabase)

The default database is PostgreSQL hosted on Supabase. Connection details:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'Airtel!23!23',
        'HOST': 'brxiwidkpkmyqkbzdhht.supabase.co',
        'PORT': '5432',
    }
}
```

### MySQL Support

To use MySQL, update your `.env`:
```env
DB_ENGINE=django.db.backends.mysql
MYSQL_DB_NAME=your_database
MYSQL_DB_USER=your_user
MYSQL_DB_PASSWORD=your_password
MYSQL_DB_HOST=localhost
MYSQL_DB_PORT=3306
```

## Deployment

### Docker Deployment

Build and run with Docker:
```bash
docker build -t adminova .
docker run -p 8000:8000 adminova
```

### Production Checklist

- [ ] Set `DEBUG=False` in settings
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure production database
- [ ] Set up SSL/HTTPS
- [ ] Configure static file serving (WhiteNoise or CDN)
- [ ] Set up M-Pesa production credentials
- [ ] Configure email backend
- [ ] Set up logging and monitoring
- [ ] Configure CORS settings

## Project Structure

```
adminova-django-dashboard/
├── adminova/              # Main project configuration
│   ├── settings/          # Split settings (base, local, production)
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── apps/                  # Django applications
│   ├── core/              # Core utilities and base models
│   ├── users/             # User management
│   ├── subscriptions/     # Subscription plans and management
│   ├── payments/          # M-Pesa payment integration
│   └── dashboard/         # Dashboard views
├── requirements/          # Python dependencies
├── static/                # Static files
├── media/                 # User-uploaded media
├── templates/             # HTML templates
└── manage.py              # Django management script
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

**Cavin Otieno**
- Email: cavin.otieno012@gmail.com
- LinkedIn: [Cavin Otieno](https://www.linkedin.com/in/cavin-otieno-9a841260/)
- GitHub: [@OumaCavin](https://github.com/OumaCavin)

## Acknowledgments

Built with Django, Django REST Framework, and the Safaricom Daraja API.

## Support

For support, email cavin.otieno012@gmail.com or open an issue on GitHub.
