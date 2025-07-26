#!/usr/bin/env python3
"""
Comprehensive Firebase authentication test script
"""

import json
import os
import sys
from datetime import datetime

import firebase_admin
import requests
from firebase_admin import auth, credentials


def test_firebase_setup():
    """Test Firebase Admin SDK setup"""
    try:
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate("keys/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        print("✅ Firebase Admin SDK initialized successfully")

        # Get project info from service account
        with open("keys/serviceAccountKey.json", "r") as f:
            service_account = json.load(f)
            project_id = service_account.get("project_id")
            print(f"✅ Project ID: {project_id}")

        return True, project_id
    except Exception as e:
        print(f"❌ Firebase setup failed: {e}")
        return False, None


def test_token_verification(token):
    """Test token verification with detailed error reporting"""
    try:
        print(f"🔍 Testing token verification...")
        print(f"📝 Token preview: {token[:50]}...")
        print(f"📏 Token length: {len(token)}")
        print(f"🔍 Token format check: {'eyJ' in token[:10]}")

        # Try to verify the token
        decoded_token = auth.verify_id_token(token)

        print("✅ Token verification successful!")
        print(f"📋 Decoded token info:")
        print(f"   - UID: {decoded_token.get('uid')}")
        print(f"   - Email: {decoded_token.get('email')}")
        print(f"   - Name: {decoded_token.get('name')}")
        print(f"   - Issuer: {decoded_token.get('iss')}")
        print(f"   - Audience: {decoded_token.get('aud')}")
        print(f"   - Issued at: {datetime.fromtimestamp(decoded_token.get('iat', 0))}")
        print(f"   - Expires at: {datetime.fromtimestamp(decoded_token.get('exp', 0))}")

        return True, decoded_token
    except auth.InvalidIdTokenError as e:
        print(f"❌ Invalid ID token error: {e}")
        return False, str(e)
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        return False, str(e)


def test_backend_endpoint(token, base_url="http://localhost:8000"):
    """Test the backend Firebase auth endpoint"""
    try:
        print(f"🌐 Testing backend endpoint: {base_url}/auth/firebase-auth")

        response = requests.post(
            f"{base_url}/auth/firebase-auth",
            json={"id_token": token},
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        print(f"📊 Response status: {response.status_code}")
        print(f"📋 Response headers: {dict(response.headers)}")

        if response.status_code == 200:
            print("✅ Backend endpoint test successful!")
            print(f"📋 Response data: {response.json()}")
            return True, response.json()
        else:
            print(f"❌ Backend endpoint test failed!")
            print(f"📋 Error response: {response.text}")
            return False, response.text

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False, str(e)
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        return False, str(e)


def main():
    """Main test function"""
    print("🚀 Firebase Authentication Debug Test")
    print("=" * 50)

    # Test Firebase setup
    setup_success, project_id = test_firebase_setup()
    if not setup_success:
        print("❌ Cannot proceed without Firebase setup")
        sys.exit(1)

    print("\n" + "=" * 50)

    # If a token is provided as command line argument, test it
    if len(sys.argv) > 1:
        token = sys.argv[1]
        print(f"🔑 Testing provided token...")

        # Test token verification
        token_success, token_result = test_token_verification(token)

        if token_success:
            print("\n" + "=" * 50)
            # Test backend endpoint
            backend_success, backend_result = test_backend_endpoint(token)

            if backend_success:
                print(
                    "\n🎉 All tests passed! Firebase authentication is working correctly."
                )
            else:
                print(
                    "\n❌ Backend endpoint test failed. Check backend logs for details."
                )
        else:
            print(f"\n❌ Token verification failed: {token_result}")
    else:
        print("ℹ️  No token provided. Run with: python test_firebase_auth.py <token>")
        print(
            "ℹ️  You can get a token from the browser console after FirebaseUI sign-in"
        )
        print("\n📋 To get a token:")
        print("1. Open your frontend app in the browser")
        print("2. Open browser developer tools (F12)")
        print("3. Go to Console tab")
        print("4. Sign in with FirebaseUI")
        print("5. Look for logs starting with '🔑 Got ID token:'")
        print("6. Copy the token and run this script with it")


if __name__ == "__main__":
    main()
