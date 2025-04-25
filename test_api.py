import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000/api/v1"

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("\n=== Testing Authentication Endpoints ===")
    
    # Test login with admin credentials
    print("\nTesting login endpoint...")
    login_data = {
        "email": "admin@realtex.ai",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print("Login failed, cannot proceed with other tests")
        return None

def test_admin_endpoints(access_token):
    """Test admin user management endpoints"""
    print("\n=== Testing Admin Endpoints ===")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Test creating a new user
    print("\nTesting create user endpoint...")
    user_data = {
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "is_admin": False
    }
    response = requests.post(f"{BASE_URL}/admin/users", json=user_data, headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test getting all users
    print("\nTesting get users endpoint...")
    response = requests.get(f"{BASE_URL}/admin/users", headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200 and len(response.json()) > 0:
        user_id = response.json()[1]['id']  # Get the second user (not admin)
        
        # Test getting a specific user
        print(f"\nTesting get user endpoint for user_id: {user_id}...")
        response = requests.get(f"{BASE_URL}/admin/users/{user_id}", headers=headers)
        print(f"Status code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test updating a user
        print(f"\nTesting update user endpoint for user_id: {user_id}...")
        update_data = {
            "first_name": "Updated",
            "last_name": "User"
        }
        response = requests.put(f"{BASE_URL}/admin/users/{user_id}", json=update_data, headers=headers)
        print(f"Status code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test resending invitation
        print(f"\nTesting resend invitation endpoint for user_id: {user_id}...")
        response = requests.post(f"{BASE_URL}/admin/users/{user_id}/resend-invitation", headers=headers)
        print(f"Status code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_prediction_endpoints(access_token):
    """Test real estate prediction endpoints"""
    print("\n=== Testing Prediction Endpoints ===")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Test price prediction
    print("\nTesting price prediction endpoint...")
    price_data = {
        "location": "London, UK",
        "size_sqft": 1200,
        "num_bedrooms": 3,
        "num_bathrooms": 2,
        "property_type": "Apartment"
    }
    response = requests.post(f"{BASE_URL}/predictions/price", json=price_data, headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test rent prediction
    print("\nTesting rent prediction endpoint...")
    response = requests.post(f"{BASE_URL}/predictions/rent", json=price_data, headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test capital growth prediction
    print("\nTesting capital growth prediction endpoint...")
    growth_data = {
        "location": "London, UK",
        "property_type": "Apartment"
    }
    response = requests.post(f"{BASE_URL}/predictions/capital-growth", json=growth_data, headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test area score
    print("\nTesting area score endpoint...")
    response = requests.get(f"{BASE_URL}/predictions/area-score?area=Central London&country=UK", headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def main():
    """Main test function"""
    print("Starting API tests...")
    
    # Test authentication endpoints
    access_token = test_auth_endpoints()
    
    if access_token:
        # Test admin endpoints
        test_admin_endpoints(access_token)
        
        # Test prediction endpoints
        test_prediction_endpoints(access_token)
    
    print("\nAPI tests completed.")

if __name__ == "__main__":
    main()
