# Backend

This directory contains the main backend application for the Talk to Your Money project.

## Structure

- `src/` — All backend code and modules
  - `auth/` — Authentication and user management modules
  - `agents/` — AI agents and related backend logic
  - `apis/` — API endpoints and integrations
  - `models/` — Pydantic data models for all entities
  - `utils/` — Utility functions and database connections
  - (add more backend components as needed)

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Firebase Configuration

1. Download your Firebase service account key from Firebase Console
2. Place it in `backend/keys/serviceAccountKey.json`
3. Or set the `FIREBASE_CRED_PATH` environment variable to point to your key file

### 3. Environment Variables

Create a `.env` file in the backend directory:

```env
# Firebase Configuration
FIREBASE_CRED_PATH=backend/keys/serviceAccountKey.json

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

### 4. Run the Server

```bash
# Using the run script
python run.py

# Or using uvicorn directly
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Authentication (`/auth`)

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/profile` - Get user profile
- `PUT /auth/profile` - Update user profile
- `PUT /auth/consents` - Update user consents
- `POST /auth/logout` - Logout user

### Health Check

- `GET /` - Root endpoint
- `GET /health` - Health check with Firebase status

## Data Models

All data models are defined in `src/models/` using Pydantic:

- `User`, `UserProfile`, `UserConsents`
- `ChatSession`, `ChatSessionSettings`
- `Message`, `MessageContent`
- `Artifact`
- `Schedule`
- `DataAccessLog`

## Database

Firestore database operations are handled by `src/utils/database.py` with a `FirestoreDB` class providing CRUD operations for all models.

## Notes

- This is the production backend.
- Use FastAPI, Firebase Admin SDK, Google Python ADK and Pydantic as core technologies.
- All backend code should reside in `backend/src/`.
- Firebase credentials are required for authentication features to work.
- Using uv for project management.
