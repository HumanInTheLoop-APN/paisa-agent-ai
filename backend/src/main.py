import os

import firebase_admin
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials

# Load environment variables from .env if present
load_dotenv()

# Initialize Firebase Admin SDK
FIREBASE_CRED_PATH = os.getenv(
    "FIREBASE_CRED_PATH", "backend/keys/serviceAccountKey.json"
)

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(FIREBASE_CRED_PATH)
        firebase_admin.initialize_app(cred)
        print(f"Firebase initialized with credentials from: {FIREBASE_CRED_PATH}")
    except Exception as e:
        print(f"Warning: Firebase initialization failed: {e}")
        print("Some features may not work without proper Firebase credentials")

app = FastAPI(title="Talk to Your Money Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers after Firebase initialization
from src.auth import firebase_auth

app.include_router(firebase_auth.router, prefix="/auth", tags=["Authentication"])


@app.get("/")
def read_root():
    return {"message": "Talk to Your Money Backend is up and running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "firebase_initialized": bool(firebase_admin._apps)}
