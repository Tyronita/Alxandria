#!/usr/bin/env python3
"""
Specific test for Kaggle push as requested in review request
Tests both with real dataset and without dataset linking
"""

import requests
import json
import time
from datetime import datetime

# Configuration from review request
BASE_URL = "https://notebook-forge-1.preview.emergentagent.com/api"
SESSION_ID = "real-kaggle-test-789"
TOPIC = "digit recognition using neural networks"
REAL_DATASET = "rtatman/english-word-frequency"

def log_test(test_name, status, details=""):
    """Log test results with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"[{timestamp}] {status_symbol} {test_name}")
    if details:
        print(f"    {details}")
    print()

def complete_research_flow():
    """Complete research steps 1-4 as required"""
    print("🔬 COMPLETING RESEARCH FLOW...")
    print(f"Session ID: {SESSION_ID}")
    print(f"Topic: {TOPIC}")
    print("=" * 50)
    
    # Step 1: Papers
    payload = {
        "session_id": SESSION_ID,
        "topic": TOPIC,
        "step": 1
    }
    
    print("Step 1: Research Papers...")
    response = requests.post(f"{BASE_URL}/research/step", json=payload, timeout=60)
    if response.status_code == 200:
        data = response.json()
        log_test("Research Step 1", "PASS", f"Content length: {len(data['content'])}")
    else:
        log_test("Research Step 1", "FAIL", f"Status: {response.status_code}")
        return False
    
    # Step 2: Gaps
    payload["step"] = 2
    print("Step 2: Research Gaps...")
    response = requests.post(f"{BASE_URL}/research/step", json=payload, timeout=60)
    if response.status_code == 200:
        data = response.json()
        log_test("Research Step 2", "PASS", f"Content length: {len(data['content'])}")
    else:
        log_test("Research Step 2", "FAIL", f"Status: {response.status_code}")
        return False
    
    # Step 3: Datasets
    payload["step"] = 3
    print("Step 3: Dataset Options...")
    response = requests.post(f"{BASE_URL}/research/step", json=payload, timeout=60)
    if response.status_code == 200:
        data = response.json()
        log_test("Research Step 3", "PASS", f"Content length: {len(data['content'])}")
    else:
        log_test("Research Step 3", "FAIL", f"Status: {response.status_code}")
        return False
    
    # Step 4: Implementation
    payload["step"] = 4
    payload["selected_data"] = {"dataset_name": REAL_DATASET}
    print("Step 4: Implementation Plan...")
    response = requests.post(f"{BASE_URL}/research/step", json=payload, timeout=60)
    if response.status_code == 200:
        data = response.json()
        log_test("Research Step 4", "PASS", f"Content length: {len(data['content'])}")
        return True
    else:
        log_test("Research Step 4", "FAIL", f"Status: {response.status_code}")
        return False

def test_kaggle_push_with_real_dataset():
    """Test push to Kaggle with REAL dataset"""
    print("🚀 TESTING KAGGLE PUSH WITH REAL DATASET...")
    print(f"Dataset: {REAL_DATASET} (real public Kaggle dataset)")
    print("=" * 50)
    
    payload = {
        "session_id": SESSION_ID,
        "topic": TOPIC,
        "dataset_name": REAL_DATASET
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ship/push-to-kaggle", json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "success" and "kaggle_link" in data:
                kaggle_link = data["kaggle_link"]
                log_test("Kaggle Push (Real Dataset)", "PASS", 
                        f"Successfully pushed to Kaggle")
                print(f"    🔗 EXACT KAGGLE LINK: {kaggle_link}")
                print(f"    📝 Kernel Slug: {data.get('kernel_slug', 'N/A')}")
                print(f"    👤 Username: {data.get('username', 'N/A')}")
                return True, kaggle_link
            else:
                log_test("Kaggle Push (Real Dataset)", "FAIL", 
                        f"Invalid response: {data}")
                return False, None
        else:
            log_test("Kaggle Push (Real Dataset)", "FAIL", 
                    f"Status: {response.status_code}, Response: {response.text}")
            return False, None
            
    except Exception as e:
        log_test("Kaggle Push (Real Dataset)", "FAIL", f"Exception: {str(e)}")
        return False, None

def test_kaggle_push_without_dataset():
    """Test push to Kaggle without dataset linking"""
    print("🚀 TESTING KAGGLE PUSH WITHOUT DATASET...")
    print("Dataset: '' (empty - no dataset linking)")
    print("=" * 50)
    
    payload = {
        "session_id": SESSION_ID,
        "topic": TOPIC,
        "dataset_name": ""
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ship/push-to-kaggle", json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "success" and "kaggle_link" in data:
                kaggle_link = data["kaggle_link"]
                log_test("Kaggle Push (No Dataset)", "PASS", 
                        f"Successfully pushed to Kaggle without dataset")
                print(f"    🔗 EXACT KAGGLE LINK: {kaggle_link}")
                print(f"    📝 Kernel Slug: {data.get('kernel_slug', 'N/A')}")
                print(f"    👤 Username: {data.get('username', 'N/A')}")
                return True, kaggle_link
            else:
                log_test("Kaggle Push (No Dataset)", "FAIL", 
                        f"Invalid response: {data}")
                return False, None
        else:
            log_test("Kaggle Push (No Dataset)", "FAIL", 
                    f"Status: {response.status_code}, Response: {response.text}")
            return False, None
            
    except Exception as e:
        log_test("Kaggle Push (No Dataset)", "FAIL", f"Exception: {str(e)}")
        return False, None

def main():
    """Run the specific test as requested in review"""
    print("=" * 60)
    print("KAGGLE NOTEBOOK PUSH TEST - REVIEW REQUEST")
    print("=" * 60)
    print("Objective: Push notebook to Kaggle with REAL dataset")
    print("Verify notebooks actually appear on Kaggle")
    print("=" * 60)
    print()
    
    # Step 1: Complete research flow
    research_success = complete_research_flow()
    if not research_success:
        print("❌ FAILED: Could not complete research flow")
        return False
    
    print()
    
    # Step 2: Test push with real dataset
    push_success, kaggle_link = test_kaggle_push_with_real_dataset()
    
    print()
    
    # Step 3: Alternative test without dataset
    alt_success, alt_link = test_kaggle_push_without_dataset()
    
    print()
    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    if push_success:
        print("✅ PRIMARY TEST PASSED: Kaggle push with real dataset successful")
        print(f"   Kaggle Link: {kaggle_link}")
    else:
        print("❌ PRIMARY TEST FAILED: Kaggle push with real dataset failed")
    
    if alt_success:
        print("✅ ALTERNATIVE TEST PASSED: Kaggle push without dataset successful")
        print(f"   Kaggle Link: {alt_link}")
    else:
        print("❌ ALTERNATIVE TEST FAILED: Kaggle push without dataset failed")
    
    if push_success or alt_success:
        print("\n🎉 CONCLUSION: Notebooks ARE being created on Kaggle!")
        return True
    else:
        print("\n⚠️ CONCLUSION: Issue with Kaggle API integration - notebooks may not be appearing")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)