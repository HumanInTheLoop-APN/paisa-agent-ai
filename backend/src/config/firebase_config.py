"""
Firebase configuration and initialization module
"""

import logging
import os
from typing import Optional

import firebase_admin
from firebase_admin import auth, credentials, firestore
from google.cloud.firestore_v1.client import Client

logger = logging.getLogger(__name__)

# Global Firebase app reference
_firebase_app: Optional[firebase_admin.App] = None


def initialize_firebase() -> firebase_admin.App:
    """Initialize Firebase Admin SDK"""
    global _firebase_app

    if _firebase_app is not None:
        logger.info("Firebase already initialized")
        return _firebase_app

    FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH")
    if not FIREBASE_CRED_PATH:
        raise ValueError("FIREBASE_CRED_PATH environment variable is not set")

    if not os.path.exists(FIREBASE_CRED_PATH):
        raise FileNotFoundError(
            f"Firebase credentials file not found: {FIREBASE_CRED_PATH}"
        )

    try:
        # Explicitly use service account credentials to avoid default credentials
        cred = credentials.Certificate(FIREBASE_CRED_PATH)
        _firebase_app = firebase_admin.initialize_app(cred)
        logger.info(f"Firebase initialized with credentials from: {FIREBASE_CRED_PATH}")

        # Verify the project ID
        with open(FIREBASE_CRED_PATH, "r") as f:
            import json

            service_account = json.load(f)
            project_id = service_account.get("project_id")
            logger.info(f"Firebase project ID: {project_id}")

        return _firebase_app

    except Exception as e:
        logger.error(f"Firebase initialization failed: {e}")
        raise


def get_firebase_app() -> firebase_admin.App:
    """Get the Firebase app instance"""
    if _firebase_app is None:
        raise RuntimeError(
            "Firebase app not initialized. Call initialize_firebase() first."
        )
    return _firebase_app


def get_auth() -> auth.Client:
    """Get Firebase Auth client"""
    if _firebase_app is None:
        raise RuntimeError(
            "Firebase app not initialized. Call initialize_firebase() first."
        )
    return auth.Client(app=_firebase_app)


def get_firestore() -> Client:
    """Get Firestore client"""
    if _firebase_app is None:
        raise RuntimeError(
            "Firebase app not initialized. Call initialize_firebase() first."
        )
    return firestore.client(app=_firebase_app)


def cleanup_firebase():
    """Clean up Firebase resources"""
    global _firebase_app

    if _firebase_app is not None:
        try:
            firebase_admin.delete_app(_firebase_app)
            _firebase_app = None
            logger.info("Firebase app deleted successfully")
        except Exception as e:
            logger.warning(f"Error cleaning up Firebase: {e}")


def is_initialized() -> bool:
    """Check if Firebase is initialized"""
    return _firebase_app is not None
