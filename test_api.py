#!/usr/bin/env python3

import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://localhost:5000'

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.user_token = None
        self.admin_token = None
        self.test_city_id = None
        self.results = []
    
    def log(self, test_name, status, message):
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'time': datetime.now().isoformat()
        }
        self.results.append(result)
        print(f"[{status:7}] {test_name}: {message}")
    
    def test_register(self):
        try:
            response = self.session.post(
                f"{BASE_URL}/auth/register",
                json={
                    "phone": "13800138001",
                    "password": "testpass123",
                    "nickname": "Test User"
                }
            )
            if response.status_code == 201:
                data = response.json()
                if data.get('code') == 'created':
                    self.user_token = data['data'].get('token')
                    self.log("Register", "PASS", "User registered successfully")
                    return True
            self.log("Register", "FAIL", f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log("Register", "ERROR", str(e))
            return False
    
    def test_login(self):
        try:
            response = self.session.post(
                f"{BASE_URL}/auth/login",
                json={
                    "phone": "13800138001",
                    "password": "testpass123"
                }
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 'success':
                    self.user_token = data['data'].get('token')
                    self.log("Login", "PASS", "Login successful")
                    return True
            self.log("Login", "FAIL", f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log("Login", "ERROR", str(e))
            return False
    
    def test_get_user_info(self):
        try:
            headers = {'Authorization': f'Bearer {self.user_token}'}
            response = self.session.get(
                f"{BASE_URL}/auth/me",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 'success':
                    self.log("Get User Info", "PASS", "User info retrieved")
                    return True
            self.log("Get User Info", "FAIL", f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log("Get User Info", "ERROR", str(e))
            return False
    
    def test_update_user_tag(self):
        try:
            headers = {'Authorization': f'Bearer {self.user_token}'}
            response = self.session.put(
                f"{BASE_URL}/users/me/tags",
                json={"tag": "asthma"},
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 'updated':
                    self.log("Update User Tag", "PASS", "Tag updated")
                    return True
            self.log("Update User Tag", "FAIL", f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log("Update User Tag", "ERROR", str(e))
            return False
    
    def test_list_cities(self):
        try:
            headers = {'Authorization': f'Bearer {self.user_token}'}
            response = self.session.get(
                f"{BASE_URL}/data/cities?page=1&page_size=10",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 'success':
                    items = data['data'].get('items', [])
                    if items:
                        self.test_city_id = items[0]['id']
                    self.log("List Cities", "PASS", f"Found {len(items)} cities")
                    return True
            self.log("List Cities", "FAIL", f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log("List Cities", "ERROR", str(e))
            return False
    
    def test_get_city_detail(self):
        if not self.test_city_id:
            self.log("Get City Detail", "SKIP", "No test city available")
            return True
        
        try:
            headers = {'Authorization': f'Bearer {self.user_token}'}
            response = self.session.get(
                f"{BASE_URL}/data/cities/{self.test_city_id}",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 'success':
                    self.log("Get City Detail", "PASS", "City detail retrieved")
                    return True
            self.log("Get City Detail", "FAIL", f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log("Get City Detail", "ERROR", str(e))
            return False
    
    def test_query_air_quality(self):
        if not self.test_city_id:
            self.log("Query Air Quality", "SKIP", "No test city available")
            return True
        
        try:
            headers = {'Authorization': f'Bearer {self.user_token}'}
            response = self.session.get(
                f"{BASE_URL}/data/query?city_id={self.test_city_id}&page=1&page_size=5",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 'success':
                    items = data['data'].get('items', [])
                    self.log("Query Air Quality", "PASS", f"Found {len(items)} records")
                    return True
            self.log("Query Air Quality", "FAIL", f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log("Query Air Quality", "ERROR", str(e))
            return False
    
    def test_get_latest_data(self):
        if not self.test_city_id:
            self.log("Get Latest Data", "SKIP", "No test city available")
            return True
        
        try:
            headers = {'Authorization': f'Bearer {self.user_token}'}
            response = self.session.get(
                f"{BASE_URL}/data/detail?city_id={self.test_city_id}",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 'success':
                    self.log("Get Latest Data", "PASS", "Latest data retrieved")
                    return True
            self.log("Get Latest Data", "FAIL", f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log("Get Latest Data", "ERROR", str(e))
            return False
    
    def test_get_monthly_stats(self):
        if not self.test_city_id:
            self.log("Get Monthly Stats", "SKIP", "No test city available")
            return True
        
        try:
            headers = {'Authorization': f'Bearer {self.user_token}'}
            response = self.session.get(
                f"{BASE_URL}/data/monthly-stats?city_id={self.test_city_id}&months=6",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 'success':
                    stats = data['data'].get('monthly_stats', [])
                    self.log("Get Monthly Stats", "PASS", f"Found {len(stats)} months")
                    return True
            self.log("Get Monthly Stats", "FAIL", f"Status: {response.status_code}")
            return False
        except Exception as e:
            self.log("Get Monthly Stats", "ERROR", str(e))
            return False
    
    def test_admin_create_city(self):
        self.log("Admin Create City", "SKIP", "Requires admin token")
        return True
    
    def test_admin_sync(self):
        self.log("Admin Trigger Sync", "SKIP", "Requires admin token")
        return True
    
    def run_all_tests(self):
        print("\n" + "="*60)
        print("Air Quality Monitoring System API Tests")
        print("="*60 + "\n")
        
        print("[Authentication Tests]")
        self.test_register()
        self.test_login()
        self.test_get_user_info()
        
        print("\n[User Management Tests]")
        self.test_update_user_tag()
        
        print("\n[Data Query Tests]")
        self.test_list_cities()
        self.test_get_city_detail()
        self.test_query_air_quality()
        self.test_get_latest_data()
        self.test_get_monthly_stats()
        
        print("\n[Admin Functionality Tests]")
        self.test_admin_create_city()
        self.test_admin_sync()
        
        print("\n" + "="*60)
        print("Test Results Summary")
        print("="*60)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        skipped = sum(1 for r in self.results if r['status'] == 'SKIP')
        errors = sum(1 for r in self.results if r['status'] == 'ERROR')
        
        print(f"Total: {total}")
        print(f"Passed: {passed} ✓")
        print(f"Failed: {failed} ✗")
        print(f"Skipped: {skipped} ○")
        print(f"Errors: {errors} ⚠")
        print(f"Success Rate: {(passed/total*100):.1f}%")

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()
