# test_flask_api.py
"""
Test script for the Flask API
Demonstrates all available endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health check endpoint."""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_encode():
    """Test encoding endpoint."""
    print("\n" + "="*60)
    print("TEST 2: Encode Qubit")
    print("="*60)
    
    payload = {"state": "0"}
    response = requests.post(f"{BASE_URL}/encode", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Initial State: {result.get('initial_state')}")
    print(f"Encoded State: {result.get('encoded_state')}")
    print(f"Measurements: {result.get('measurements')}")

def test_error():
    """Test error introduction endpoint."""
    print("\n" + "="*60)
    print("TEST 3: Introduce Error")
    print("="*60)
    
    payload = {"state": "0", "error_qubit": 1}
    response = requests.post(f"{BASE_URL}/error", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Initial State: {result.get('initial_state')}")
    print(f"Error Qubit: {result.get('error_qubit')}")
    print(f"Measurements: {result.get('measurements')}")

def test_correct():
    """Test correction endpoint."""
    print("\n" + "="*60)
    print("TEST 4: Error Correction")
    print("="*60)
    
    payload = {"state": "0", "error_qubit": 1}
    response = requests.post(f"{BASE_URL}/correct", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Initial State: {result.get('initial_state')}")
    print(f"Error Qubit: {result.get('error_qubit')}")
    print(f"Expected State: {result.get('expected_state')}")
    print(f"Success Rate: {result.get('success_rate')}%")
    print(f"Measurements: {result.get('measurements')}")

def test_pipeline():
    """Test full pipeline endpoint."""
    print("\n" + "="*60)
    print("TEST 5: Full Pipeline")
    print("="*60)
    
    payload = {"state": "1", "error_qubit": 2, "shots": 1000}
    response = requests.post(f"{BASE_URL}/pipeline", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    pipeline = result.get('pipeline', {})
    print(f"Initial State: {pipeline.get('initial_state')}")
    print(f"Error Qubit: {pipeline.get('error_qubit')}")
    print(f"Expected State: {pipeline.get('expected_state')}")
    print(f"Success Rate: {pipeline.get('success_rate')}%")
    print(f"Corrected: {pipeline.get('corrected')}")
    print(f"Measurements: {result.get('measurements')}")

def test_statevector():
    """Test statevector analysis endpoint."""
    print("\n" + "="*60)
    print("TEST 6: Statevector Analysis")
    print("="*60)
    
    payload = {"state": "0", "error_qubit": 1}
    response = requests.post(f"{BASE_URL}/statevector", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    stages = result.get('stages', {})
    
    print("\nInitial State:")
    print(f"  Probabilities: {stages.get('initial', {}).get('probabilities')}")
    
    print("\nEncoded State:")
    print(f"  Probabilities: {stages.get('encoded', {}).get('probabilities')}")
    
    print("\nWith Error:")
    print(f"  Probabilities: {stages.get('with_error', {}).get('probabilities')}")
    
    print("\nCorrected State:")
    print(f"  Probabilities: {stages.get('corrected', {}).get('probabilities')}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("FLASK API TEST SUITE")
    print("3-Qubit Bit-Flip Error Correction")
    print("="*60)
    
    try:
        test_health()
        test_encode()
        test_error()
        test_correct()
        test_pipeline()
        test_statevector()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to Flask server!")
        print("Make sure the server is running on http://localhost:5000\n")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
