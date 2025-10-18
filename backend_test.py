#!/usr/bin/env python3
"""
Backend API Testing for Alexandria App - Kaggle Notebook Push Functionality
Tests the new /api/ship/push-to-kaggle endpoint and existing research endpoints
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://notebook-forge-1.preview.emergentagent.com/api"
SESSION_ID = "test-session-" + str(int(time.time()))
TOPIC = "medical image classification"
DATASET_NAME = "medical-images"

def log_test(test_name, status, details=""):
    """Log test results with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"[{timestamp}] {status_symbol} {test_name}")
    if details:
        print(f"    {details}")
    print()

def test_root_endpoint():
    """Test GET /api/ endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "message" in data and "Alexandria" in data["message"]:
                log_test("Root Endpoint", "PASS", f"Response: {data}")
                return True
            else:
                log_test("Root Endpoint", "FAIL", f"Unexpected response format: {data}")
                return False
        else:
            log_test("Root Endpoint", "FAIL", f"Status: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        log_test("Root Endpoint", "FAIL", f"Exception: {str(e)}")
        return False

def test_research_step(step_num, expected_content_keywords=None):
    """Test POST /api/research/step endpoint for specific step"""
    try:
        payload = {
            "session_id": SESSION_ID,
            "topic": TOPIC,
            "step": step_num
        }
        
        if step_num == 3:
            payload["selected_data"] = None
        elif step_num == 4:
            payload["selected_data"] = {"dataset_name": DATASET_NAME}
            
        print(f"    Sending request to step {step_num}... (may take 10-30 seconds)")
        response = requests.post(f"{BASE_URL}/research/step", 
                               json=payload, 
                               timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ["step", "content", "citations"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                log_test(f"Research Step {step_num}", "FAIL", 
                        f"Missing fields: {missing_fields}")
                return False
            
            # Check content is not empty
            if not data["content"] or len(data["content"].strip()) < 50:
                log_test(f"Research Step {step_num}", "FAIL", 
                        f"Content too short or empty: {len(data.get('content', ''))}")
                return False
            
            # Check for expected keywords if provided
            if expected_content_keywords:
                content_lower = data["content"].lower()
                missing_keywords = [kw for kw in expected_content_keywords 
                                  if kw.lower() not in content_lower]
                if missing_keywords:
                    log_test(f"Research Step {step_num}", "WARN", 
                            f"Missing expected keywords: {missing_keywords}")
            
            # Check citations format
            citations = data.get("citations", [])
            if not isinstance(citations, list):
                log_test(f"Research Step {step_num}", "FAIL", 
                        f"Citations should be a list, got: {type(citations)}")
                return False
            
            log_test(f"Research Step {step_num}", "PASS", 
                    f"Content length: {len(data['content'])}, Citations: {len(citations)}")
            return True
            
        else:
            log_test(f"Research Step {step_num}", "FAIL", 
                    f"Status: {response.status_code}, Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        log_test(f"Research Step {step_num}", "FAIL", f"Exception: {str(e)}")
        return False

def test_push_to_kaggle():
    """Test POST /api/ship/push-to-kaggle endpoint"""
    try:
        payload = {
            "session_id": SESSION_ID,
            "topic": TOPIC,
            "dataset_name": DATASET_NAME
        }
        
        print(f"    Pushing to Kaggle... (may take 5-10 seconds)")
        response = requests.post(f"{BASE_URL}/ship/push-to-kaggle", 
                               json=payload, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ["status", "kaggle_link", "kernel_slug", "username"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                log_test("Push to Kaggle", "FAIL", 
                        f"Missing fields: {missing_fields}")
                return False
            
            # Check status is success
            if data.get("status") != "success":
                log_test("Push to Kaggle", "FAIL", 
                        f"Status not success: {data.get('status')}")
                return False
            
            # Check Kaggle link format
            kaggle_link = data.get("kaggle_link", "")
            expected_format = "https://www.kaggle.com/code/evanoleary/"
            if not kaggle_link.startswith(expected_format):
                log_test("Push to Kaggle", "FAIL", 
                        f"Invalid Kaggle link format: {kaggle_link}")
                return False
            
            # Check username
            if data.get("username") != "evanoleary":
                log_test("Push to Kaggle", "FAIL", 
                        f"Wrong username: {data.get('username')}")
                return False
            
            # Check kernel slug format
            kernel_slug = data.get("kernel_slug", "")
            if not kernel_slug.startswith("alexandria-"):
                log_test("Push to Kaggle", "WARN", 
                        f"Kernel slug doesn't start with 'alexandria-': {kernel_slug}")
            
            log_test("Push to Kaggle", "PASS", 
                    f"Link: {kaggle_link}, Slug: {kernel_slug}")
            return True
            
        else:
            log_test("Push to Kaggle", "FAIL", 
                    f"Status: {response.status_code}, Response: {response.text[:300]}")
            return False
            
    except Exception as e:
        log_test("Push to Kaggle", "FAIL", f"Exception: {str(e)}")
        return False

def run_all_tests():
    """Run all backend tests in sequence"""
    print("=" * 60)
    print("ALEXANDRIA BACKEND API TESTING")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    print(f"Session ID: {SESSION_ID}")
    print(f"Topic: {TOPIC}")
    print(f"Dataset: {DATASET_NAME}")
    print("=" * 60)
    print()
    
    results = {}
    
    # Test 1: Root endpoint
    results["root"] = test_root_endpoint()
    
    # Test 2: Research Step 1 (Papers)
    results["step1"] = test_research_step(1, ["paper", "research", "analysis"])
    
    # Test 3: Research Step 2 (Gaps)  
    results["step2"] = test_research_step(2, ["gap", "opportunity", "limitation"])
    
    # Test 4: Research Step 3 (Datasets)
    results["step3"] = test_research_step(3, ["dataset", "kaggle", "source"])
    
    # Test 5: Push to Kaggle (main feature)
    results["kaggle_push"] = test_push_to_kaggle()
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper():<15} {status}")
    
    print(f"\nOVERALL: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print("⚠️  SOME TESTS FAILED - Check logs above")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)