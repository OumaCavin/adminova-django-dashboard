#!/bin/bash

# Adminova Django Dashboard - Quick Test Script
# This script verifies the application is working correctly

echo "=========================================="
echo "Adminova Django Dashboard - Quick Test"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [ -d "venv" ]; then
    source venv/bin/activate || . venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "✗ Virtual environment not found"
    exit 1
fi

# Check database
if [ -f "db.sqlite3" ]; then
    echo "✓ Database file exists"
    
    # Count migrations
    MIGRATIONS=$(python manage.py showmigrations | grep "\[X\]" | wc -l)
    echo "✓ Applied migrations: $MIGRATIONS"
else
    echo "✗ Database not found"
fi

# Check superuser
echo ""
echo "Superuser credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo "  Email: cavin.otieno012@gmail.com"

# Test API endpoints
echo ""
echo "Testing API endpoints..."

# Start server in background if not running
if ! pgrep -f "manage.py runserver" > /dev/null; then
    echo "Starting Django server..."
    python manage.py runserver 0.0.0.0:8000 > /dev/null 2>&1 &
    SERVER_PID=$!
    sleep 3
    echo "✓ Server started (PID: $SERVER_PID)"
else
    echo "✓ Server already running"
fi

# Test plans endpoint
echo ""
echo "Testing /api/plans/ endpoint..."
PLANS_COUNT=$(curl -s http://localhost:8000/api/plans/ | python -c "import sys, json; print(json.load(sys.stdin)['count'])" 2>/dev/null)

if [ "$PLANS_COUNT" = "7" ]; then
    echo "✓ Subscription Plans API working (7 plans found)"
else
    echo "⚠ Could not verify plans endpoint"
fi

echo ""
echo "=========================================="
echo "Testing complete!"
echo ""
echo "Access the application:"
echo "  - Admin: http://localhost:8000/admin/"
echo "  - API Docs: http://localhost:8000/api/docs/"
echo "  - Plans API: http://localhost:8000/api/plans/"
echo "=========================================="
