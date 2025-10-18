#!/usr/bin/env python3
"""
Manual Kaggle CLI test to understand the exact issue
"""

import os
import json
import tempfile
import subprocess
import time

# Set up environment
os.environ['KAGGLE_USERNAME'] = 'evanoleary'
os.environ['KAGGLE_KEY'] = '69a5b9afcdff4a5c56fa399c31d467c1'

def run_kaggle_command(command):
    """Run kaggle command with proper environment"""
    env = os.environ.copy()
    env['PATH'] = f"/root/.venv/bin:{env.get('PATH', '')}"
    
    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=30)
    
    print(f"Return code: {result.returncode}")
    print(f"STDOUT: {result.stdout}")
    print(f"STDERR: {result.stderr}")
    
    return result

def test_manual_kernel_creation():
    """Test manual kernel creation with minimal setup"""
    
    # Create a simple notebook
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# Test Notebook\n", "This is a test notebook created via API."]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["print('Hello from Alexandria!')"]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # Create unique slug
    timestamp = str(int(time.time()))[-6:]
    kernel_slug = f"alexandria-test-{timestamp}"
    
    print(f"Creating kernel with slug: {kernel_slug}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write notebook
        notebook_path = os.path.join(temp_dir, "notebook.ipynb")
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f, indent=2)
        
        # Test 1: Try with minimal metadata (no id)
        print("\n=== TEST 1: Minimal metadata (no id) ===")
        metadata1 = {
            "title": f"Alexandria Test {timestamp}",
            "code_file": "notebook.ipynb",
            "language": "python",
            "kernel_type": "notebook",
            "is_private": False,
            "enable_gpu": False,
            "enable_internet": False
        }
        
        metadata_path = os.path.join(temp_dir, "kernel-metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata1, f, indent=2)
        
        result1 = run_kaggle_command(['kaggle', 'kernels', 'push', '-p', temp_dir])
        
        # Test 2: Try with id field
        print("\n=== TEST 2: With id field ===")
        metadata2 = {
            "id": f"evanoleary/{kernel_slug}",
            "title": f"Alexandria Test {timestamp}",
            "code_file": "notebook.ipynb",
            "language": "python",
            "kernel_type": "notebook",
            "is_private": False,
            "enable_gpu": False,
            "enable_internet": False
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata2, f, indent=2)
        
        result2 = run_kaggle_command(['kaggle', 'kernels', 'push', '-p', temp_dir])
        
        # Test 3: Try with slug field
        print("\n=== TEST 3: With slug field ===")
        metadata3 = {
            "slug": kernel_slug,
            "title": f"Alexandria Test {timestamp}",
            "code_file": "notebook.ipynb",
            "language": "python",
            "kernel_type": "notebook",
            "is_private": False,
            "enable_gpu": False,
            "enable_internet": False
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata3, f, indent=2)
        
        result3 = run_kaggle_command(['kaggle', 'kernels', 'push', '-p', temp_dir])
        
        # Test 4: Try kaggle kernels init first
        print("\n=== TEST 4: Using kaggle kernels init ===")
        init_result = run_kaggle_command(['kaggle', 'kernels', 'init', '-p', temp_dir])
        
        if init_result.returncode == 0:
            # Read the generated metadata
            with open(metadata_path, 'r') as f:
                generated_metadata = json.load(f)
            print(f"Generated metadata: {json.dumps(generated_metadata, indent=2)}")
            
            # Try to push with generated metadata
            result4 = run_kaggle_command(['kaggle', 'kernels', 'push', '-p', temp_dir])
        else:
            print("Init failed, skipping push test")

if __name__ == "__main__":
    test_manual_kernel_creation()