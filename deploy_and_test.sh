#!/bin/bash
# Comprehensive deployment and testing script for Adminova
# Created by Cavin Otieno

set -e

echo "=========================================="
echo "Adminova Django Dashboard"
echo "Deployment and Testing Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if running in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    print_error "Virtual environment not activated!"
    echo "Please run: source venv/bin/activate"
    exit 1
fi

print_success "Virtual environment active"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    print_warning "Please update .env with your configuration"
    exit 1
fi

print_success ".env file found"

# Run database migrations
echo ""
echo "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
print_success "Database migrations completed"

# Create superuser if it doesn't exist
echo ""
echo "Checking for superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@adminova.com', 'admin123')
    print('Superuser created: admin / admin123')
else:
    print('Superuser already exists')
EOF

# Load sample data
echo ""
echo "Loading sample subscription plans..."
python manage.py init_sample_data
print_success "Sample data loaded"

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
print_success "Static files collected"

# Run tests
echo ""
echo "Running application tests..."
if command -v pytest &> /dev/null; then
    pytest -v
    print_success "Tests passed"
else
    print_warning "pytest not installed, skipping tests"
fi

# Start server
echo ""
echo "=========================================="
print_success "Deployment completed successfully!"
echo "=========================================="
echo ""
echo "Application is ready to run!"
echo ""
echo "To start the development server:"
echo "  python manage.py runserver"
echo ""
echo "Then access:"
echo "  - Application: http://127.0.0.1:8000/"
echo "  - Admin: http://127.0.0.1:8000/admin/"
echo "  - API Docs: http://127.0.0.1:8000/api/docs/"
echo ""
echo "Default superuser credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "For M-Pesa testing:"
echo "  1. Start ngrok: ngrok http 8000"
echo "  2. Update MPESA_CALLBACK_URL in .env with ngrok URL"
echo "  3. Restart the server"
echo ""
