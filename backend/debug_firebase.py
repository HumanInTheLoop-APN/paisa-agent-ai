#!/usr/bin/env python3
"""
Debug script to test Firebase token verification
"""

import os
import sys

import firebase_admin
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
            import json

            service_account = json.load(f)
            project_id = service_account.get("project_id")
            print(f"✅ Project ID: {project_id}")

        return True
    except Exception as e:
        print(f"❌ Firebase setup failed: {e}")
        return False


def test_token_verification(token):
    """Test token verification"""
    try:
        print(f"🔍 Testing token verification...")
        print(f"📝 Token preview: {token[:50]}...")

        # Try to verify the token
        decoded_token = auth.verify_id_token(token)

        print("✅ Token verification successful!")
        print(f"📋 Decoded token info:")
        print(f"   - UID: {decoded_token.get('uid')}")
        print(f"   - Email: {decoded_token.get('email')}")
        print(f"   - Name: {decoded_token.get('name')}")
        print(f"   - Issuer: {decoded_token.get('iss')}")
        print(f"   - Audience: {decoded_token.get('aud')}")
        print(f"   - Issued at: {decoded_token.get('iat')}")
        print(f"   - Expires at: {decoded_token.get('exp')}")

        return True
    except auth.InvalidIdTokenError as e:
        print(f"❌ Invalid ID token error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    # Test Firebase setup
    if not test_firebase_setup():
        sys.exit(1)

    # If a token is provided as command line argument, test it
    if len(sys.argv) > 1:
        token = sys.argv[1]
        test_token_verification(token)
    else:
        print("ℹ️  No token provided. Run with: python debug_firebase.py <token>")
        print(
            "ℹ️  You can get a token from the browser console after FirebaseUI sign-in"
        )
