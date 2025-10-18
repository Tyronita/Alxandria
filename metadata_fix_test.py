#!/usr/bin/env python3
"""
Metadata Fix Test - Quick verification of Kaggle notebook push with empty dataset
Tests the specific scenario from review request to verify metadata fix resolves 400 Bad Request error
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuration - Using EXACT parameters from review request
BASE_URL = "https://notebook-forge-1.preview.emergentagent.com/api"
SESSION_ID = "metadata-fix-test"
TOPIC = "machine learning research"  # Simple topic for quick test
DATASET_NAME = ""  # Empty as requested

def log_test(test_name, status, details=""):
    """Log test results with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"[{timestamp}] {status_symbol} {test_name}")
    if details:
        print(f"    {details}")
    print()

def test_research_step_1():
    """Test Step 1 only as requested"""
    try:
        payload = {
            "session_id": SESSION_ID,
            "topic": TOPIC,
            "step": 1
        }
        
        print(f"    Executing Research Step 1... (may take 10-30 seconds)")
        response = requests.post(f"{BASE_URL}/research/step", 
                               json=payload, 
                               timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ["step", "content", "citations"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                log_test("Research Step 1", "FAIL", 
                        f"Missing fields: {missing_fields}")
                return False
            
            # Check content is not empty
            if not data["content"] or len(data["content"].strip()) < 50:
                log_test("Research Step 1", "FAIL", 
                        f"Content too short or empty: {len(data.get('content', ''))}")
                return False
            
            log_test("Research Step 1", "PASS", 
                    f"Content length: {len(data['content'])}, Citations: {len(data.get('citations', []))}")
            return True
            
        else:
            log_test("Research Step 1", "FAIL", 
                    f"Status: {response.status_code}, Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        log_test("Research Step 1", "FAIL", f"Exception: {str(e)}")
        return False

def test_kaggle_push_empty_dataset():
    """Test Kaggle push with empty dataset_name as requested"""
    try:
        payload = {
            "session_id": SESSION_ID,
            "topic": TOPIC,
            "dataset_name": DATASET_NAME  # Empty string as requested
        }
        
        print(f"    Pushing to Kaggle with empty dataset_name... (may take 5-10 seconds)")
        response = requests.post(f"{BASE_URL}/ship/push-to-kaggle", 
                               json=payload, 
                               timeout=30)
        
        print(f"    Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ["status", "kaggle_link", "kernel_slug", "username"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                log_test("Kaggle Push (Empty Dataset)", "FAIL", 
                        f"Missing fields: {missing_fields}")
                return False, None
            
            # Get the exact kaggle_link as requested
            kaggle_link = data.get("kaggle_link", "")
            
            # Print the exact kaggle_link as requested in review
            print(f"    🔗 EXACT KAGGLE LINK RETURNED: {kaggle_link}")
            
            # Check status is success
            if data.get("status") != "success":
                log_test("Kaggle Push (Empty Dataset)", "FAIL", 
                        f"Status not success: {data.get('status')}")
                return False, kaggle_link
            
            # Check Kaggle link format
            expected_format = "https://www.kaggle.com/code/evanoleary/"
            if not kaggle_link.startswith(expected_format):
                log_test("Kaggle Push (Empty Dataset)", "FAIL", 
                        f"Invalid Kaggle link format: {kaggle_link}")
                return False, kaggle_link
            
            log_test("Kaggle Push (Empty Dataset)", "PASS", 
                    f"API returned success with link: {kaggle_link}")
            
            return True, kaggle_link
            
        elif response.status_code == 400:
            # Check for 400 Bad Request errors as requested
            error_text = response.text
            log_test("Kaggle Push (Empty Dataset)", "FAIL", 
                    f"400 BAD REQUEST ERROR: {error_text}")
            print(f"    🚨 400 ERROR DETAILS: {error_text}")
            return False, None
            
        else:
            log_test("Kaggle Push (Empty Dataset)", "FAIL", 
                    f"Status: {response.status_code}, Response: {response.text[:300]}")
            return False, None
            
    except Exception as e:
        log_test("Kaggle Push (Empty Dataset)", "FAIL", f"Exception: {str(e)}")
        return False, None

def verify_kaggle_link(kaggle_link):
    """Verify if the Kaggle link actually works (returns 200, not 404)"""
    if not kaggle_link:
        log_test("Kaggle Link Verification", "FAIL", "No link to verify")
        return False
    
    try:
        print(f"    Checking if Kaggle link works: {kaggle_link}")
        response = requests.get(kaggle_link, timeout=15)
        
        print(f"    Link Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            log_test("Kaggle Link Verification", "PASS", 
                    f"Link works! Status: {response.status_code}")
            return True
        elif response.status_code == 404:
            log_test("Kaggle Link Verification", "FAIL", 
                    f"Link returns 404 - notebook doesn't exist on Kaggle")
            return False
        else:
            log_test("Kaggle Link Verification", "WARN", 
                    f"Unexpected status: {response.status_code}")
            return False
            
    except Exception as e:
        log_test("Kaggle Link Verification", "FAIL", f"Exception: {str(e)}")
        return False

def check_backend_logs():
    """Check backend logs for any 400 errors from Kaggle API"""
    try:
        print("    Checking backend logs for Kaggle API errors...")
        import subprocess
        
        # Check supervisor backend logs
        result = subprocess.run(
            ['tail', '-n', '50', '/var/log/supervisor/backend.err.log'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            log_content = result.stdout
            if "400 Client Error" in log_content or "Bad Request" in log_content:
                print(f"    🚨 FOUND 400 ERRORS IN BACKEND LOGS:")
                # Extract relevant error lines
                error_lines = [line.strip() for line in log_content.split('\n') 
                             if '400' in line or 'Bad Request' in line or 'Error' in line]
                for line in error_lines[-3:]:  # Show last 3 error lines
                    print(f"        {line}")
                return True
            else:
                print(f"    ✅ No 400 errors found in recent backend logs")
                return False
        else:
            print(f"    ⚠️  Could not read backend logs")
            return False
            
    except Exception as e:
        print(f"    ⚠️  Error checking logs: {str(e)}")
        return False

def run_metadata_fix_test():
    """Run the specific metadata fix test as requested in review"""
    print("=" * 70)
    print("METADATA FIX TEST - KAGGLE NOTEBOOK PUSH VERIFICATION")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    print(f"Session ID: {SESSION_ID}")
    print(f"Topic: {TOPIC}")
    print(f"Dataset Name: '{DATASET_NAME}' (empty as requested)")
    print("=" * 70)
    print()
    
    results = {}
    
    # Step 1: Complete ONE research step as requested
    print("🔬 STEP 1: Complete Research Step 1")
    results["research_step1"] = test_research_step_1()
    
    # Step 2: Push to Kaggle with empty dataset_name
    print("🚀 STEP 2: Push to Kaggle with empty dataset_name")
    kaggle_success, kaggle_link = test_kaggle_push_empty_dataset()
    results["kaggle_push"] = kaggle_success
    
    # Step 3: Verify the Kaggle link works
    print("🔍 STEP 3: Verify Kaggle link accessibility")
    results["link_verification"] = verify_kaggle_link(kaggle_link)
    
    # Step 4: Check for 400 errors in backend logs
    print("📋 STEP 4: Check backend logs for 400 errors")
    has_400_errors = check_backend_logs()
    
    # Summary
    print("=" * 70)
    print("METADATA FIX TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper():<25} {status}")
    
    print(f"\nOVERALL: {passed}/{total} tests passed")
    
    # Critical findings
    print("\n🎯 CRITICAL FINDINGS:")
    if kaggle_link:
        print(f"   📎 Exact Kaggle Link: {kaggle_link}")
    
    if results.get("link_verification", False):
        print(f"   ✅ Link Status: Working (200 OK)")
    else:
        print(f"   ❌ Link Status: Not working (404 or error)")
    
    if has_400_errors:
        print(f"   🚨 Backend Logs: 400 Bad Request errors found")
    else:
        print(f"   ✅ Backend Logs: No 400 errors detected")
    
    # Final verdict
    if results.get("kaggle_push", False) and results.get("link_verification", False):
        print("\n🎉 METADATA FIX SUCCESSFUL!")
        print("   ✅ API returns success AND notebook exists on Kaggle")
        return True
    elif results.get("kaggle_push", False) and not results.get("link_verification", False):
        print("\n⚠️  METADATA FIX PARTIALLY WORKING")
        print("   ✅ API returns success BUT notebook doesn't exist on Kaggle")
        print("   🔧 Issue persists - notebooks not actually being created")
        return False
    else:
        print("\n❌ METADATA FIX NOT WORKING")
        print("   ❌ API call fails or returns errors")
        return False

if __name__ == "__main__":
    success = run_metadata_fix_test()
    sys.exit(0 if success else 1)