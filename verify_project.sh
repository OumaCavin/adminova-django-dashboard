#!/bin/bash
# Quick verification script to check project completeness
# Created by Cavin Otieno

echo "=========================================="
echo "Adminova Django Dashboard"
echo "Project Verification Script"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

CHECKS_PASSED=0
CHECKS_FAILED=0

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗${NC} $2 (Missing: $1)"
        ((CHECKS_FAILED++))
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗${NC} $2 (Missing: $1)"
        ((CHECKS_FAILED++))
    fi
}

echo "Checking Project Structure..."
echo ""

# Core files
check_file "manage.py" "Django management script"
check_file "requirements/base.txt" "Base requirements"
check_file "requirements/local.txt" "Local requirements"
check_file "requirements/production.txt" "Production requirements"
check_file ".env.example" "Environment template"
check_file ".gitignore" "Git ignore file"
check_file "README.md" "Project README"
check_file "Dockerfile" "Docker configuration"
check_file "docker-compose.yml" "Docker Compose configuration"

echo ""
echo "Checking Django Configuration..."
echo ""

# Django configuration
check_dir "adminova" "Main project directory"
check_file "adminova/settings/base.py" "Base settings"
check_file "adminova/settings/local.py" "Local settings"
check_file "adminova/settings/production.py" "Production settings"
check_file "adminova/urls.py" "URL configuration"
check_file "adminova/wsgi.py" "WSGI configuration"

echo ""
echo "Checking Django Apps..."
echo ""

# Django apps
check_dir "apps/core" "Core app"
check_dir "apps/users" "Users app"
check_dir "apps/subscriptions" "Subscriptions app"
check_dir "apps/payments" "Payments app"
check_dir "apps/dashboard" "Dashboard app"

# Key models
check_file "apps/users/models.py" "User models"
check_file "apps/subscriptions/models.py" "Subscription models"
check_file "apps/payments/models.py" "Payment models"

# M-Pesa integration
check_file "apps/payments/mpesa_service.py" "M-Pesa service"

echo ""
echo "Checking API Components..."
echo ""

# API files
check_file "apps/users/serializers.py" "User serializers"
check_file "apps/subscriptions/serializers.py" "Subscription serializers"
check_file "apps/payments/serializers.py" "Payment serializers"

check_file "apps/users/views.py" "User API views"
check_file "apps/subscriptions/views.py" "Subscription API views"
check_file "apps/payments/views.py" "Payment API views"

echo ""
echo "Checking Documentation..."
echo ""

# Documentation
check_file "docs/DEPLOYMENT.md" "Deployment guide"
check_file "docs/MPESA_INTEGRATION.md" "M-Pesa integration guide"
check_file "docs/API_TESTING.md" "API testing guide"
check_file "docs/END_TO_END_TESTING.md" "E2E testing guide"
check_file "CONTRIBUTING.md" "Contributing guidelines"
check_file "PROJECT_SUMMARY.md" "Project summary"

echo ""
echo "Checking Scripts..."
echo ""

# Scripts
check_file "setup.sh" "Setup script"
check_file "deploy_and_test.sh" "Deployment script"
check_file "tests/automated_tests.py" "Automated tests"

echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo ""
echo -e "Checks Passed: ${GREEN}$CHECKS_PASSED${NC}"
echo -e "Checks Failed: ${RED}$CHECKS_FAILED${NC}"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Project is complete.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review .env.example and create .env"
    echo "  2. Run: bash deploy_and_test.sh"
    echo "  3. Follow docs/END_TO_END_TESTING.md"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please review missing components.${NC}"
    exit 1
fi
