#!/usr/bin/env python3
"""
CRITICAL TEST: Verify Kaggle push works with 'language' field removed
Testing specific parameters from review request
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuration from review request
BASE_URL = "https://notebook-forge-1.preview.emergentagent.com/api"
SESSION_ID = "language-fix-test-999"
TOPIC = "image classification"
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
    """Test research step 1 ONLY as requested"""
    try:
        payload = {
            "session_id": SESSION_ID,
            "topic": TOPIC,
            "step": 1
        }
        
        print(f"    Executing research step 1 for topic '{TOPIC}'... (may take 10-30 seconds)")
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

def test_kaggle_push_language_fix():
    """Test Kaggle push with empty dataset_name to verify language field fix"""
    try:
        payload = {
            "session_id": SESSION_ID,
            "topic": TOPIC,
            "dataset_name": DATASET_NAME  # Empty string
        }
        
        print(f"    Testing Kaggle push with empty dataset_name... (may take 5-10 seconds)")
        response = requests.post(f"{BASE_URL}/ship/push-to-kaggle", 
                               json=payload, 
                               timeout=30)
        
        print(f"    Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ["status", "kaggle_link"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                log_test("Kaggle Push (Language Fix)", "FAIL", 
                        f"Missing fields: {missing_fields}")
                return False, None
            
            # Check status is success
            if data.get("status") != "success":
                log_test("Kaggle Push (Language Fix)", "FAIL", 
                        f"Status not success: {data.get('status')}")
                return False, None
            
            # Get the exact kaggle_link
            kaggle_link = data.get("kaggle_link", "")
            
            # Check if it's a valid Kaggle link
            if not kaggle_link.startswith("https://www.kaggle.com/"):
                log_test("Kaggle Push (Language Fix)", "FAIL", 
                        f"Invalid Kaggle link format: {kaggle_link}")
                return False, kaggle_link
            
            log_test("Kaggle Push (Language Fix)", "PASS", 
                    f"Successfully returned valid Kaggle link")
            
            return True, kaggle_link
            
        else:
            log_test("Kaggle Push (Language Fix)", "FAIL", 
                    f"Status: {response.status_code}, Response: {response.text[:300]}")
            return False, None
            
    except Exception as e:
        log_test("Kaggle Push (Language Fix)", "FAIL", f"Exception: {str(e)}")
        return False, None

def check_backend_logs():
    """Check backend logs for Kaggle API messages"""
    try:
        print("    Checking backend logs for Kaggle API messages...")
        
        # Check supervisor backend logs
        import subprocess
        result = subprocess.run(
            ["tail", "-n", "50", "/var/log/supervisor/backend.out.log"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            log_content = result.stdout
            
            # Look for Kaggle-related messages
            kaggle_messages = []
            for line in log_content.split('\n'):
                if any(keyword in line.lower() for keyword in ['kaggle', 'push', 'kernel', 'error', 'success']):
                    kaggle_messages.append(line.strip())
            
            if kaggle_messages:
                print("    📋 BACKEND LOG MESSAGES (Kaggle-related):")
                for msg in kaggle_messages[-10:]:  # Last 10 relevant messages
                    print(f"        {msg}")
            else:
                print("    📋 No Kaggle-related messages found in recent logs")
                
            return kaggle_messages
        else:
            print("    ⚠️  Could not read backend logs")
            return []
            
    except Exception as e:
        print(f"    ⚠️  Error checking logs: {str(e)}")
        return []

def test_kaggle_link_accessibility(kaggle_link):
    """Test if the returned Kaggle link is accessible"""
    if not kaggle_link:
        return False
        
    try:
        print(f"    Testing accessibility of: {kaggle_link}")
        
        # Make a HEAD request to check if the link exists
        response = requests.head(kaggle_link, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            log_test("Kaggle Link Accessibility", "PASS", 
                    f"Link is accessible (Status: {response.status_code})")
            return True
        elif response.status_code == 404:
            log_test("Kaggle Link Accessibility", "FAIL", 
                    f"Link returns 404 - notebook not found on Kaggle")
            return False
        else:
            log_test("Kaggle Link Accessibility", "WARN", 
                    f"Link returns status {response.status_code}")
            return False
            
    except Exception as e:
        log_test("Kaggle Link Accessibility", "FAIL", f"Exception: {str(e)}")
        return False

def run_language_fix_test():
    """Run the specific language fix test as requested"""
    print("=" * 70)
    print("CRITICAL TEST: Verify Kaggle push works with 'language' field removed")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    print(f"Session ID: {SESSION_ID}")
    print(f"Topic: {TOPIC}")
    print(f"Dataset Name: '{DATASET_NAME}' (empty)")
    print("=" * 70)
    print()
    
    # Step 1: Complete research step 1 ONLY
    step1_success = test_research_step_1()
    if not step1_success:
        print("❌ Research Step 1 failed - cannot proceed with Kaggle push test")
        return False
    
    # Step 2: Push to Kaggle with empty dataset_name
    kaggle_success, kaggle_link = test_kaggle_push_language_fix()
    
    # Step 3: Check backend logs
    log_messages = check_backend_logs()
    
    # Step 4: Test Kaggle link accessibility (if we got a link)
    link_accessible = False
    if kaggle_link:
        link_accessible = test_kaggle_link_accessibility(kaggle_link)
    
    # Summary
    print("=" * 70)
    print("LANGUAGE FIX TEST RESULTS")
    print("=" * 70)
    
    print(f"Research Step 1:           {'✅ PASS' if step1_success else '❌ FAIL'}")
    print(f"Kaggle Push (No Language): {'✅ PASS' if kaggle_success else '❌ FAIL'}")
    print(f"Kaggle Link Accessible:    {'✅ PASS' if link_accessible else '❌ FAIL'}")
    
    if kaggle_link:
        print(f"\n🔗 EXACT KAGGLE LINK RETURNED: {kaggle_link}")
    
    if log_messages:
        print(f"\n📋 BACKEND LOG ANALYSIS:")
        error_found = any('error' in msg.lower() or '400' in msg or 'failed' in msg.lower() 
                         for msg in log_messages)
        success_found = any('success' in msg.lower() or 'pushed' in msg.lower() 
                           for msg in log_messages)
        
        if error_found:
            print("    ❌ Error messages found in logs")
        elif success_found:
            print("    ✅ Success messages found in logs")
        else:
            print("    ⚠️  No clear error or success indicators in logs")
    
    # Final assessment
    overall_success = step1_success and kaggle_success
    
    print(f"\n🎯 OVERALL RESULT: {'✅ LANGUAGE FIX SUCCESSFUL' if overall_success else '❌ LANGUAGE FIX FAILED'}")
    
    if overall_success:
        print("✅ Removing 'language' field appears to have fixed the 400 error")
        print("✅ Kaggle push now returns valid response with kaggle_link")
    else:
        print("❌ Issues still exist with Kaggle push functionality")
    
    return overall_success

if __name__ == "__main__":
    success = run_language_fix_test()
    sys.exit(0 if success else 1)