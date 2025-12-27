"""
Test login endpoint to verify demo account works.
"""

import requests
import sys

def test_demo_login():
    """Test demo account login."""
    print("=" * 60)
    print("Testing Demo Account Login")
    print("=" * 60)
    
    # API endpoint
    url = "http://localhost:8000/api/auth/login"
    
    # Demo credentials
    credentials = {
        "username": "demo@project.com",  # OAuth2 uses 'username' field
        "password": "Demo@123"
    }
    
    print(f"\n📡 Testing login endpoint: {url}")
    print(f"   Email: {credentials['username']}")
    print(f"   Password: {credentials['password']}")
    
    try:
        # Make login request
        response = requests.post(
            url,
            data=credentials,  # OAuth2PasswordRequestForm expects form data
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login SUCCESS!")
            print(f"   Token Type: {data.get('token_type')}")
            print(f"   Access Token: {data.get('access_token')[:50]}...")
            print("\n✅ Demo account is working correctly!")
        else:
            print("❌ Login FAILED!")
            print(f"   Error: {response.text}")
            print("\nTroubleshooting:")
            print("1. Make sure backend is running: python run.py")
            print("2. Run fix script: python fix_demo_account.py")
            print("3. Check database connection")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error!")
        print("   Backend server is not running.")
        print("   Start it with: python run.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_demo_login()

