# test_api.py
"""
Test script for Flask API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_encode():
    print("\n" + "="*60)
    print("Testing /encode endpoint")
    print("="*60)
    
    response = requests.post(f"{BASE_URL}/encode", 
                            json={'state': '0'})
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"Initial state: {data['initial_state']}")
        print(f"Encoded state: {data['encoded_state']}")
        print(f"Measurements: {data['measurements']}")
    else:
        print(f"❌ Failed: {response.status_code}")

def test_error():
    print("\n" + "="*60)
    print("Testing /error endpoint")
    print("="*60)
    
    response = requests.post(f"{BASE_URL}/error",
                            json={'state': '0', 'error_qubit': 1})
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"Error on qubit: {data['error_qubit']}")
        print(f"Measurements: {data['measurements']}")
    else:
        print(f"❌ Failed: {response.status_code}")

def test_correct():
    print("\n" + "="*60)
    print("Testing /correct endpoint")
    print("="*60)
    
    response = requests.post(f"{BASE_URL}/correct",
                            json={'state': '0', 'error_qubit': 1})
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"Expected state: {data['expected_state']}")
        print(f"Success rate: {data['success_rate']:.1f}%")
        print(f"Measurements: {data['measurements']}")
    else:
        print(f"❌ Failed: {response.status_code}")

def test_pipeline():
    print("\n" + "="*60)
    print("Testing /pipeline endpoint")
    print("="*60)
    
    response = requests.post(f"{BASE_URL}/pipeline",
                            json={'state': '0', 'error_qubit': 1, 'shots': 1000})
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"Pipeline: {data['pipeline']}")
        print(f"Success rate: {data['pipeline']['success_rate']:.1f}%")
    else:
        print(f"❌ Failed: {response.status_code}")

def test_statevector():
    print("\n" + "="*60)
    print("Testing /statevector endpoint")
    print("="*60)
    
    response = requests.post(f"{BASE_URL}/statevector",
                            json={'state': '0', 'error_qubit': 1})
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"Stages available: {list(data['stages'].keys())}")
    else:
        print(f"❌ Failed: {response.status_code}")

def test_health():
    print("\n" + "="*60)
    print("Testing /health endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"Status: {data['status']}")
        print(f"Service: {data['service']}")
    else:
        print(f"❌ Failed: {response.status_code}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("API TEST SUITE")
    print("="*60)
    print("Make sure the Flask server is running on localhost:5000")
    input("\nPress Enter to start tests...")
    
    try:
        test_health()
        test_encode()
        test_error()
        test_correct()
        test_pipeline()
        test_statevector()
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server")
        print("Make sure Flask server is running: python flask_backend.py\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
