#!/usr/bin/env python3
"""
Dataset Loading Code Verification Test for Alexandria App
Tests that the generated notebook contains ACTUAL executable dataset loading code (not commented)

Review Request Requirements:
1. Complete research step 1 with session_id "dataset-code-fix-test"
2. Topic: "image classification"
3. Push to Kaggle with dataset_name: "mloey1/ahcd1" (a real small Kaggle dataset)
4. Download the generated notebook and verify the "Load Dataset" cell contains ACTUAL executable code
"""

import requests
import json
import time
import sys
import re
from datetime import datetime

# Configuration - Using EXACT parameters from review request
BASE_URL = "https://notebook-forge-1.preview.emergentagent.com/api"
SESSION_ID = "dataset-code-fix-test"
TOPIC = "image classification"
DATASET_NAME = "mloey1/ahcd1"  # Real small Kaggle dataset

def log_test(test_name, status, details=""):
    """Log test results with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"[{timestamp}] {status_symbol} {test_name}")
    if details:
        print(f"    {details}")
    print()

def test_research_step_1():
    """Test POST /api/research/step endpoint for step 1 only"""
    try:
        payload = {
            "session_id": SESSION_ID,
            "topic": TOPIC,
            "step": 1
        }
        
        print(f"    Completing research step 1 for '{TOPIC}'... (may take 10-30 seconds)")
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
            
            # Check citations format
            citations = data.get("citations", [])
            if not isinstance(citations, list):
                log_test("Research Step 1", "FAIL", 
                        f"Citations should be a list, got: {type(citations)}")
                return False
            
            log_test("Research Step 1", "PASS", 
                    f"Content length: {len(data['content'])}, Citations: {len(citations)}")
            return True
            
        else:
            log_test("Research Step 1", "FAIL", 
                    f"Status: {response.status_code}, Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        log_test("Research Step 1", "FAIL", f"Exception: {str(e)}")
        return False

def test_push_to_kaggle():
    """Test POST /api/ship/push-to-kaggle endpoint with real dataset"""
    try:
        payload = {
            "session_id": SESSION_ID,
            "topic": TOPIC,
            "dataset_name": DATASET_NAME
        }
        
        print(f"    Pushing to Kaggle with dataset '{DATASET_NAME}'... (may take 5-10 seconds)")
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
                return False, None
            
            # Check status is success
            if data.get("status") != "success":
                log_test("Push to Kaggle", "FAIL", 
                        f"Status not success: {data.get('status')}")
                return False, None
            
            # Check Kaggle link format
            kaggle_link = data.get("kaggle_link", "")
            expected_format = "https://www.kaggle.com/code/evanoleary/"
            if not kaggle_link.startswith(expected_format):
                log_test("Push to Kaggle", "FAIL", 
                        f"Invalid Kaggle link format: {kaggle_link}")
                return False, None
            
            log_test("Push to Kaggle", "PASS", 
                    f"Link: {kaggle_link}")
            
            return True, kaggle_link
            
        else:
            log_test("Push to Kaggle", "FAIL", 
                    f"Status: {response.status_code}, Response: {response.text[:300]}")
            return False, None
            
    except Exception as e:
        log_test("Push to Kaggle", "FAIL", f"Exception: {str(e)}")
        return False, None

def verify_dataset_loading_code():
    """CRITICAL TEST: Download notebook and verify dataset loading cell contains ACTUAL executable code"""
    try:
        payload = {
            "session_id": SESSION_ID,
            "topic": TOPIC,
            "dataset_name": DATASET_NAME
        }
        
        print(f"    Downloading notebook to verify dataset loading code...")
        response = requests.post(f"{BASE_URL}/ship/notebook", 
                               json=payload, 
                               timeout=30)
        
        if response.status_code == 200:
            # Parse notebook JSON
            try:
                notebook_data = response.json()
            except:
                log_test("Dataset Loading Code Verification", "FAIL", 
                        "Response is not valid JSON")
                return False
            
            # Check notebook structure
            if "cells" not in notebook_data:
                log_test("Dataset Loading Code Verification", "FAIL", 
                        "Notebook missing 'cells' field")
                return False
            
            cells = notebook_data["cells"]
            if not isinstance(cells, list) or len(cells) == 0:
                log_test("Dataset Loading Code Verification", "FAIL", 
                        "Notebook has no cells")
                return False
            
            # Find the "Load Dataset" cell
            dataset_cell_found = False
            dataset_cell_content = ""
            
            for i, cell in enumerate(cells):
                # Check if this is a markdown cell with "Load Dataset" title
                if (cell.get("cell_type") == "markdown" and 
                    "source" in cell and 
                    any("load dataset" in line.lower() for line in cell["source"])):
                    
                    # The next cell should be the code cell with dataset loading
                    if i + 1 < len(cells):
                        next_cell = cells[i + 1]
                        if next_cell.get("cell_type") == "code" and "source" in next_cell:
                            dataset_cell_found = True
                            dataset_cell_content = "".join(next_cell["source"])
                            break
            
            if not dataset_cell_found:
                log_test("Dataset Loading Code Verification", "FAIL", 
                        "No 'Load Dataset' code cell found")
                return False
            
            print(f"    Found dataset loading cell with {len(dataset_cell_content)} characters")
            
            # CRITICAL VERIFICATION: Check for ACTUAL executable code (not comments)
            verification_results = {}
            
            # 1. Check for !kaggle datasets download command (NOT in comments)
            kaggle_download_pattern = r'^[^#]*!kaggle\s+datasets\s+download'
            kaggle_download_found = bool(re.search(kaggle_download_pattern, dataset_cell_content, re.MULTILINE))
            verification_results["kaggle_download"] = kaggle_download_found
            
            # 2. Check for zipfile extraction code (NOT in comments)
            zipfile_patterns = [
                r'^[^#]*with\s+zipfile\.ZipFile',
                r'^[^#]*zipfile\.ZipFile.*\.extractall',
                r'^[^#]*zip_ref\.extractall'
            ]
            zipfile_extraction_found = any(
                re.search(pattern, dataset_cell_content, re.MULTILINE) 
                for pattern in zipfile_patterns
            )
            verification_results["zipfile_extraction"] = zipfile_extraction_found
            
            # 3. Check for automatic CSV loading code (NOT in comments)
            csv_loading_patterns = [
                r'^[^#]*pd\.read_csv',
                r'^[^#]*pandas\.read_csv',
                r'^[^#]*csv_files.*=.*glob',
                r'^[^#]*df\s*=\s*pd\.read_csv'
            ]
            csv_loading_found = any(
                re.search(pattern, dataset_cell_content, re.MULTILINE) 
                for pattern in csv_loading_patterns
            )
            verification_results["csv_loading"] = csv_loading_found
            
            # 4. Check that the dataset name is correctly used
            dataset_name_used = DATASET_NAME in dataset_cell_content
            verification_results["dataset_name_used"] = dataset_name_used
            
            # 5. Check for file listing code
            file_listing_patterns = [
                r'^[^#]*\.glob\(',
                r'^[^#]*os\.listdir',
                r'^[^#]*list\(.*\.glob',
                r'^[^#]*files\s*=.*glob'
            ]
            file_listing_found = any(
                re.search(pattern, dataset_cell_content, re.MULTILINE) 
                for pattern in file_listing_patterns
            )
            verification_results["file_listing"] = file_listing_found
            
            # Report detailed results
            print(f"    📋 DATASET LOADING CODE VERIFICATION RESULTS:")
            print(f"    ✅ Kaggle download command: {'FOUND' if verification_results['kaggle_download'] else '❌ MISSING'}")
            print(f"    ✅ Zipfile extraction code: {'FOUND' if verification_results['zipfile_extraction'] else '❌ MISSING'}")
            print(f"    ✅ CSV loading code: {'FOUND' if verification_results['csv_loading'] else '❌ MISSING'}")
            print(f"    ✅ Dataset name used: {'FOUND' if verification_results['dataset_name_used'] else '❌ MISSING'}")
            print(f"    ✅ File listing code: {'FOUND' if verification_results['file_listing'] else '❌ MISSING'}")
            
            # Check for commented out code (this should NOT be the case)
            commented_kaggle = bool(re.search(r'#.*!kaggle\s+datasets\s+download', dataset_cell_content))
            commented_zipfile = bool(re.search(r'#.*zipfile', dataset_cell_content))
            commented_csv = bool(re.search(r'#.*pd\.read_csv', dataset_cell_content))
            
            if commented_kaggle or commented_zipfile or commented_csv:
                log_test("Dataset Loading Code Verification", "FAIL", 
                        f"❌ CRITICAL: Found commented out code! Kaggle: {commented_kaggle}, Zipfile: {commented_zipfile}, CSV: {commented_csv}")
                return False
            
            # All critical components must be present as ACTUAL code
            critical_components = [
                verification_results["kaggle_download"],
                verification_results["zipfile_extraction"], 
                verification_results["csv_loading"]
            ]
            
            if all(critical_components):
                log_test("Dataset Loading Code Verification", "PASS", 
                        f"✅ ALL CRITICAL COMPONENTS FOUND AS ACTUAL EXECUTABLE CODE (not comments)")
                
                # Print a sample of the actual code for verification
                print(f"    📝 SAMPLE OF ACTUAL DATASET LOADING CODE:")
                lines = dataset_cell_content.split('\n')
                for i, line in enumerate(lines[:20]):  # Show first 20 lines
                    if line.strip() and not line.strip().startswith('#'):
                        print(f"    {i+1:2d}: {line}")
                if len(lines) > 20:
                    print(f"    ... and {len(lines) - 20} more lines")
                
                return True
            else:
                missing_components = []
                if not verification_results["kaggle_download"]:
                    missing_components.append("Kaggle download command")
                if not verification_results["zipfile_extraction"]:
                    missing_components.append("Zipfile extraction")
                if not verification_results["csv_loading"]:
                    missing_components.append("CSV loading")
                
                log_test("Dataset Loading Code Verification", "FAIL", 
                        f"❌ MISSING CRITICAL COMPONENTS: {', '.join(missing_components)}")
                return False
            
        else:
            log_test("Dataset Loading Code Verification", "FAIL", 
                    f"Status: {response.status_code}, Response: {response.text[:300]}")
            return False
            
    except Exception as e:
        log_test("Dataset Loading Code Verification", "FAIL", f"Exception: {str(e)}")
        return False

def run_dataset_code_verification_test():
    """Run the complete dataset code verification test as per review request"""
    print("=" * 80)
    print("ALEXANDRIA DATASET LOADING CODE VERIFICATION TEST")
    print("=" * 80)
    print(f"🎯 VERIFYING DATASET LOADING CODE IS ACTUAL (NOT COMMENTED)")
    print(f"Base URL: {BASE_URL}")
    print(f"Session ID: {SESSION_ID}")
    print(f"Topic: {TOPIC}")
    print(f"Dataset: {DATASET_NAME}")
    print("=" * 80)
    print()
    
    results = {}
    
    # Step 1: Complete research step 1
    print("🔬 STEP 1: Complete research step 1...")
    results["research_step_1"] = test_research_step_1()
    
    if not results["research_step_1"]:
        print("❌ Research step 1 failed - cannot proceed")
        return False
    
    # Step 2: Push to Kaggle with real dataset
    print("🚀 STEP 2: Push to Kaggle with dataset...")
    kaggle_success, kaggle_link = test_push_to_kaggle()
    results["kaggle_push"] = kaggle_success
    
    if not kaggle_success:
        print("❌ Kaggle push failed - cannot proceed")
        return False
    
    print(f"✅ Kaggle link generated: {kaggle_link}")
    
    # Step 3: CRITICAL - Verify dataset loading code
    print("🔍 STEP 3: CRITICAL - Verify dataset loading code...")
    results["dataset_code_verification"] = verify_dataset_loading_code()
    
    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper():<30} {status}")
    
    print(f"\nOVERALL: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Dataset loading code is ACTUAL executable code (not commented)!")
        print(f"✅ Notebook contains working code for dataset: {DATASET_NAME}")
        return True
    else:
        print("⚠️  SOME TESTS FAILED - Check logs above")
        if not results.get("dataset_code_verification", False):
            print("❌ CRITICAL: Dataset loading code verification failed!")
            print("❌ The notebook may contain commented code instead of executable code!")
        return False

if __name__ == "__main__":
    success = run_dataset_code_verification_test()
    sys.exit(0 if success else 1)