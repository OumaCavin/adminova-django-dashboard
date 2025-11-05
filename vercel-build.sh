#!/usr/bin/env bash

# Vercel build script for Django Adminova Dashboard
# This script runs Django migrations and collects static files

echo "🚀 Starting Django build process..."

# Set environment to production
export DJANGO_SETTINGS_MODULE=adminova.settings.production

# Run database migrations
echo "📊 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create static directory if it doesn't exist
mkdir -p .vercel/output/static

echo "✅ Build completed successfully!"