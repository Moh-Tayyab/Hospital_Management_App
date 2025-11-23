import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def print_response(response):
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def verify_api():
    print("1. Registering Patient...")
    patient_data = {
        "username": "testpatient",
        "password": "testpassword123",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "Patient"
    }
    try:
        resp = requests.post(f"{BASE_URL}/register/patient/", json=patient_data)
        print_response(resp)
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    print("\n2. Logging in...")
    login_data = {
        "username": "testpatient",
        "password": "testpassword123"
    }
    resp = requests.post(f"{BASE_URL}/login/", json=login_data)
    print_response(resp)
    
    if resp.status_code == 200:
        token = resp.json().get('access')
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n3. Listing Doctors...")
        resp = requests.get(f"{BASE_URL}/doctors/", headers=headers)
        print_response(resp)

        print("\n4. Checking Profile...")
        resp = requests.get(f"{BASE_URL}/profile/", headers=headers)
        print_response(resp)

if __name__ == "__main__":
    verify_api()
