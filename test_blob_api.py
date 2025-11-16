"""
Test script for Local Blob API endpoints
Tests file upload, download, list, and delete operations
"""

import requests
import json
import os
from io import BytesIO

BASE_URL = 'http://localhost:5000'

def test_upload_file():
    """Test file upload endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Upload File")
    print("="*60)
    
    # Create a test file
    test_content = """# Test Quantum Circuit
# This is a test file for the Blob API
q_0: ──H──■───
          │
q_1: ────⊕───
"""
    
    # Prepare file for upload
    files = {
        'file': ('test_circuit.txt', BytesIO(test_content.encode()), 'text/plain')
    }
    
    try:
        response = requests.post(f'{BASE_URL}/upload', files=files)
        print(f"Status Code: {response.status_code}")
        
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Message: {data.get('message')}")
        print(f"Filename: {data.get('filename')}")
        print(f"Size: {data.get('size_formatted')}")
        print(f"Download URL: {data.get('download_url')}")
        
        return data.get('filename')
    except Exception as e:
        print(f"Error: {e}")
        return None


def test_list_files():
    """Test list files endpoint"""
    print("\n" + "="*60)
    print("TEST 2: List Files")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/files')
        print(f"Status Code: {response.status_code}")
        
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"File Count: {data.get('count')}")
        print("\nFiles:")
        for file in data.get('files', []):
            print(f"  - {file['filename']} ({file['size_formatted']}) - {file['created']}")
    except Exception as e:
        print(f"Error: {e}")


def test_download_file(filename):
    """Test file download endpoint"""
    print("\n" + "="*60)
    print("TEST 3: Download File")
    print("="*60)
    
    if not filename:
        print("No filename provided, skipping test")
        return
    
    try:
        response = requests.get(f'{BASE_URL}/download/{filename}')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Content Length: {len(response.content)} bytes")
            print(f"Content Type: {response.headers.get('Content-Type')}")
            print("\nFile Content Preview:")
            print(response.content.decode()[:200])
        else:
            print(f"Error: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")


def test_delete_file(filename):
    """Test file deletion endpoint"""
    print("\n" + "="*60)
    print("TEST 4: Delete File")
    print("="*60)
    
    if not filename:
        print("No filename provided, skipping test")
        return
    
    try:
        response = requests.delete(f'{BASE_URL}/delete/{filename}')
        print(f"Status Code: {response.status_code}")
        
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Message: {data.get('message')}")
    except Exception as e:
        print(f"Error: {e}")


def test_visualize_circuit():
    """Test circuit visualization endpoint"""
    print("\n" + "="*60)
    print("TEST 5: Visualize Circuit")
    print("="*60)
    
    try:
        payload = {
            'state': '0',
            'error_qubit': 1
        }
        
        response = requests.post(
            f'{BASE_URL}/visualize_circuit',
            json=payload
        )
        print(f"Status Code: {response.status_code}")
        
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Circuit Depth: {data.get('depth')}")
        print(f"Gate Count: {data.get('gate_count')}")
        print(f"Operations: {data.get('operations')}")
        print("\nCircuit:")
        for line in data.get('circuit', [])[:10]:
            print(line)
    except Exception as e:
        print(f"Error: {e}")


def test_api_docs():
    """Test API documentation endpoint"""
    print("\n" + "="*60)
    print("TEST 6: API Documentation")
    print("="*60)
    
    try:
        response = requests.get(f'{BASE_URL}/api')
        print(f"Status Code: {response.status_code}")
        
        data = response.json()
        print(f"API Name: {data.get('name')}")
        print(f"Version: {data.get('version')}")
        print(f"\nEndpoint Categories:")
        for category in data.get('endpoints', {}).keys():
            count = len(data['endpoints'][category])
            print(f"  - {category}: {count} endpoints")
        
        print(f"\nConfiguration:")
        config = data.get('configuration', {})
        for key, value in config.items():
            print(f"  - {key}: {value}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    print("\n" + "="*60)
    print("BLOB API TEST SUITE")
    print("="*60)
    print("Testing Local Blob API and new endpoints...")
    print("Make sure Flask server is running on http://localhost:5000")
    
    # Test API documentation
    test_api_docs()
    
    # Test circuit visualization
    test_visualize_circuit()
    
    # Test file upload
    filename = test_upload_file()
    
    # Test file listing
    test_list_files()
    
    # Test file download
    test_download_file(filename)
    
    # Test file deletion
    test_delete_file(filename)
    
    # List files again to verify deletion
    test_list_files()
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
