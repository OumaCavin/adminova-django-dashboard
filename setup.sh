#!/bin/bash
# Quick setup script for Adminova Django Dashboard
# Created by Cavin Otieno

set -e

echo "============================================"
echo "Adminova Django Dashboard - Quick Setup"
echo "Created by Cavin Otieno"
echo "============================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements/local.txt
echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created. Please update it with your configuration."
    echo "  - Database credentials"
    echo "  - M-Pesa API credentials"
    echo "  - Secret key"
else
    echo "✓ .env file already exists"
fi

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo "✓ Database migrations completed"

# Create superuser prompt
echo ""
read -p "Do you want to create a superuser? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Initialize sample data
echo ""
read -p "Do you want to load sample subscription plans? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py init_sample_data
    echo "✓ Sample data loaded"
fi

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected"

# Done
echo ""
echo "============================================"
echo "✓ Setup completed successfully!"
echo "============================================"
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then visit:"
echo "  - Application: http://127.0.0.1:8000/"
echo "  - Admin: http://127.0.0.1:8000/admin/"
echo "  - API Docs: http://127.0.0.1:8000/api/docs/"
echo ""
echo "For M-Pesa testing with ngrok:"
echo "  1. Run: ngrok http 8000"
echo "  2. Update MPESA_CALLBACK_URL in .env"
echo "  3. Restart the server"
echo ""
echo "Happy coding!"
echo ""
