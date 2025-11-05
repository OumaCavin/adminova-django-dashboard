#!/usr/bin/env python
"""
Automated test suite for Adminova Django Dashboard
Tests all critical functionality including M-Pesa integration
Created by Cavin Otieno
"""

import requests
import json
import time
from typing import Dict, Optional

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Test data
TEST_USER = {
    "email": "autotest@example.com",
    "username": "autotest",
    "password": "TestPass123!",
    "password_confirm": "TestPass123!",
    "first_name": "Auto",
    "last_name": "Test"
}

TEST_PHONE = "254712345678"


class AdminovaTestSuite:
    """Automated test suite for Adminova"""
    
    def __init__(self):
        self.token: Optional[str] = None
        self.plan_id: Optional[int] = None
        self.payment_id: Optional[int] = None
        self.results = []
    
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✓ PASSED" if passed else "✗ FAILED"
        result = f"{status}: {test_name}"
        if message:
            result += f" - {message}"
        print(result)
        self.results.append({"test": test_name, "passed": passed, "message": message})
    
    def test_server_running(self) -> bool:
        """Test if server is accessible"""
        try:
            response = requests.get(BASE_URL, timeout=5)
            self.log_test("Server Running", response.status_code in [200, 301, 302, 404])
            return True
        except requests.exceptions.RequestException as e:
            self.log_test("Server Running", False, str(e))
            return False
    
    def test_api_docs(self) -> bool:
        """Test API documentation accessibility"""
        try:
            response = requests.get(f"{API_BASE}/docs/", timeout=5)
            passed = response.status_code == 200
            self.log_test("API Documentation", passed)
            return passed
        except Exception as e:
            self.log_test("API Documentation", False, str(e))
            return False
    
    def test_user_registration(self) -> bool:
        """Test user registration"""
        try:
            response = requests.post(
                f"{API_BASE}/auth/users/",
                json=TEST_USER,
                timeout=10
            )
            passed = response.status_code in [200, 201]
            self.log_test("User Registration", passed, response.text[:100])
            return passed
        except Exception as e:
            self.log_test("User Registration", False, str(e))
            return False
    
    def test_authentication(self) -> bool:
        """Test user authentication and token generation"""
        try:
            response = requests.post(
                f"{API_BASE}/auth/token/",
                json={
                    "username": TEST_USER["username"],
                    "password": TEST_USER["password"]
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                passed = self.token is not None
                self.log_test("Authentication", passed, f"Token: {self.token[:20]}...")
                return passed
            else:
                self.log_test("Authentication", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Authentication", False, str(e))
            return False
    
    def test_list_plans(self) -> bool:
        """Test listing subscription plans"""
        try:
            response = requests.get(f"{API_BASE}/plans/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                plans = data.get("results", [])
                if plans:
                    self.plan_id = plans[0]["id"]
                passed = len(plans) > 0
                self.log_test("List Plans", passed, f"Found {len(plans)} plans")
                return passed
            else:
                self.log_test("List Plans", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("List Plans", False, str(e))
            return False
    
    def test_mpesa_initiation(self) -> bool:
        """Test M-Pesa payment initiation"""
        if not self.token or not self.plan_id:
            self.log_test("M-Pesa Initiation", False, "Missing token or plan_id")
            return False
        
        try:
            headers = {"Authorization": f"Token {self.token}"}
            response = requests.post(
                f"{API_BASE}/payments/mpesa/initiate/",
                json={
                    "phone_number": TEST_PHONE,
                    "plan_id": self.plan_id
                },
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                checkout_id = data.get("checkout_request_id")
                passed = checkout_id is not None
                self.log_test("M-Pesa Initiation", passed, f"Checkout: {checkout_id}")
                return passed
            else:
                self.log_test("M-Pesa Initiation", False, f"Status: {response.status_code}, Response: {response.text[:200]}")
                return False
        except Exception as e:
            self.log_test("M-Pesa Initiation", False, str(e))
            return False
    
    def test_payment_list(self) -> bool:
        """Test listing user payments"""
        if not self.token:
            self.log_test("Payment List", False, "Missing token")
            return False
        
        try:
            headers = {"Authorization": f"Token {self.token}"}
            response = requests.get(
                f"{API_BASE}/payments/mpesa/",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                payments = data.get("results", [])
                self.log_test("Payment List", True, f"Found {len(payments)} payments")
                return True
            else:
                self.log_test("Payment List", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Payment List", False, str(e))
            return False
    
    def test_subscription_status(self) -> bool:
        """Test getting active subscription"""
        if not self.token:
            self.log_test("Subscription Status", False, "Missing token")
            return False
        
        try:
            headers = {"Authorization": f"Token {self.token}"}
            response = requests.get(
                f"{API_BASE}/plans/subscriptions/active/",
                headers=headers,
                timeout=10
            )
            
            # 404 is acceptable if no active subscription
            passed = response.status_code in [200, 404]
            status = "Active subscription found" if response.status_code == 200 else "No active subscription"
            self.log_test("Subscription Status", passed, status)
            return passed
        except Exception as e:
            self.log_test("Subscription Status", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("="*60)
        print("Adminova Django Dashboard - Automated Test Suite")
        print("Created by Cavin Otieno")
        print("="*60)
        print()
        
        # Run tests
        tests = [
            self.test_server_running,
            self.test_api_docs,
            self.test_user_registration,
            self.test_authentication,
            self.test_list_plans,
            self.test_mpesa_initiation,
            self.test_payment_list,
            self.test_subscription_status,
        ]
        
        for test in tests:
            test()
            time.sleep(0.5)  # Small delay between tests
        
        # Summary
        print()
        print("="*60)
        print("Test Summary")
        print("="*60)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        failed = total - passed
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print()
            print("Failed Tests:")
            for result in self.results:
                if not result["passed"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        print("="*60)
        
        return failed == 0


if __name__ == "__main__":
    suite = AdminovaTestSuite()
    success = suite.run_all_tests()
    exit(0 if success else 1)
