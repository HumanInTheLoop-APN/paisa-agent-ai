from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from ..config.firebase_config import get_auth
from ..models import User, UserConsents, UserProfile
from ..repositories.user_repository import UserRepository

router = APIRouter()
security = HTTPBearer()


class UserRegistrationRequest(BaseModel):
    email: str
    password: str
    name: str
    country: str = "IN"
    risk_profile: str = "moderate"


class UserLoginRequest(BaseModel):
    identifier: str  # Can be email or phone number
    password: str


class GoogleSignInRequest(BaseModel):
    id_token: str


class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    risk_profile: Optional[str] = None


class UserConsentUpdateRequest(BaseModel):
    store_financial_snippets: Optional[bool] = None
    store_artifacts: Optional[bool] = None
    retention_days: Optional[int] = None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """Get current user from Firebase token"""
    try:
        token = credentials.credentials
        print(f"🔍 Received token in get_current_user: {token[:50]}...")

        # Get Firebase Auth client
        auth_client = get_auth()

        # Try to verify as ID token first (in case frontend sends ID token directly)
        try:
            decoded_token = auth_client.verify_id_token(token)
            uid = decoded_token["uid"]
            print(f"✅ Verified as ID token for UID: {uid}")
        except Exception as id_token_error:
            print(f"❌ ID token verification failed: {id_token_error}")
            # Custom tokens cannot be verified server-side directly
            # They are meant for Firebase client SDK
            # For now, we'll need a different approach
            raise HTTPException(
                status_code=401,
                detail="Invalid token format. Please send ID token instead of custom token.",
            )

        # Fetch user from Firestore database
        print(f"🔍 Fetching user {uid} from database...")
        user = await UserRepository().get_user(uid)
        if not user:
            print(f"❌ User {uid} not found in database")
            raise HTTPException(status_code=404, detail="User not found in database")

        print(f"✅ User {uid} found and returned")
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Unexpected error in get_current_user: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


GetCurrentUserDep = Annotated[User, Depends(get_current_user)]


def is_email(identifier: str) -> bool:
    """Check if identifier is an email address"""
    return "@" in identifier


def is_phone(identifier: str) -> bool:
    """Check if identifier is a phone number"""
    # Remove all non-digit characters
    digits_only = "".join(filter(str.isdigit, identifier))
    # Check if it's a valid phone number (7-15 digits)
    return 7 <= len(digits_only) <= 15


@router.post("/register")
async def register_user(request: UserRegistrationRequest):
    """Register a new user with Firebase Auth

    DEPRECATED: This endpoint is no longer needed with FirebaseUI.
    FirebaseUI handles user registration directly.
    Consider removing this endpoint after FirebaseUI migration is complete.
    """
    try:
        # Create user in Firebase Auth
        user_record = get_auth().create_user(
            email=request.email, password=request.password, display_name=request.name
        )

        # Create user profile in Firestore
        user = User(
            uid=user_record.uid,
            profile=UserProfile(
                name=request.name,
                email=request.email,
                country=request.country,
                risk_profile=request.risk_profile,
            ),
            consents=UserConsents(),
        )

        # Save user to Firestore database
        success = await UserRepository().create_user(user)
        if not success:
            # Clean up Firebase Auth user if Firestore save fails
            get_auth().delete_user(user_record.uid)
            raise HTTPException(status_code=500, detail="Failed to save user profile")

        return {
            "message": "User registered successfully",
            "user_id": user_record.uid,
            "email": user_record.email,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login")
async def login_user(request: UserLoginRequest):
    """Login user with email/phone and return Firebase token

    DEPRECATED: This endpoint is no longer needed with FirebaseUI.
    FirebaseUI handles user login directly.
    Consider removing this endpoint after FirebaseUI migration is complete.
    """
    try:
        # Determine if identifier is email or phone
        if is_email(request.identifier):
            # Login with email
            user_record = get_auth().get_user_by_email(request.identifier)
        elif is_phone(request.identifier):
            # Login with phone number
            # Format phone number to E.164 format if needed
            phone = request.identifier
            if not phone.startswith("+"):
                # Assume it's a local number, add country code (you might want to make this configurable)
                phone = f"+91{phone}"  # Default to India (+91)

            user_record = get_auth().get_user_by_phone_number(phone)
        else:
            raise HTTPException(status_code=400, detail="Invalid identifier format")

        # TODO: Verify password (Firebase Admin SDK doesn't support password verification)
        # This would typically be done on the client side with Firebase Auth SDK

        # Generate custom token for the user
        custom_token = get_auth().create_custom_token(user_record.uid)

        return {
            "message": "Login successful",
            "user_id": user_record.uid,
            "custom_token": custom_token.decode("utf-8"),
            "email": user_record.email,
            "phone": user_record.phone_number,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.post("/firebase-auth")
async def firebase_auth(request: GoogleSignInRequest):
    """Handle all FirebaseUI authentication (Google, Email, Phone)"""
    try:
        print(
            f"🔥 Firebase auth request received with ID token: {request.id_token[:50]}..."
        )
        print(f"📏 Token length: {len(request.id_token)}")
        print(f"🔍 Token format check: {'eyJ' in request.id_token[:10]}")

        # Verify the ID token (works for all Firebase auth methods)
        print("🔍 Verifying ID token...")
        try:
            decoded_token = get_auth().verify_id_token(request.id_token)
            uid = decoded_token["uid"]
            print(f"✅ ID token verified successfully for UID: {uid}")
            print(
                f"📋 Decoded token info: name={decoded_token.get('name')}, email={decoded_token.get('email')}"
            )
        except Exception as e:
            print(f"❌ Invalid ID token error: {e}")
            print(
                f"🔍 Token details: length={len(request.id_token)}, starts_with_eyJ={'eyJ' in request.id_token[:10]}"
            )
            raise HTTPException(status_code=401, detail=f"Invalid ID token: {str(e)}")

        # Check if user exists in our database
        print(f"🔍 Checking if user {uid} exists in database...")
        user = await UserRepository().get_user(uid)
        print(f"👤 User found in database: {user is not None}")

        if not user:
            print("📝 Creating new user profile...")
            # Create new user profile if they don't exist
            user_profile = UserProfile(
                name=decoded_token.get("name", "Unknown"),
                email=decoded_token.get("email", ""),
                country="IN",  # Default country
                risk_profile="moderate",  # Default risk profile
            )

            user = User(
                uid=uid,
                profile=user_profile,
                consents=UserConsents(),
            )

            # Save to database
            print("💾 Saving user to database...")
            success = await UserRepository().create_user(user)
            if not success:
                print("❌ Failed to save user to database")
                raise HTTPException(
                    status_code=500, detail="Failed to create user profile"
                )
            print("✅ User saved to database successfully")

        # Generate custom token
        print("🎫 Generating custom token...")
        custom_token = get_auth().create_custom_token(uid)
        print("✅ Custom token generated successfully")

        return {
            "message": "Authentication successful",
            "user_id": uid,
            "custom_token": custom_token.decode("utf-8"),
            "email": user.profile.email,
            "is_new_user": user is None,
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Unexpected error in firebase_auth: {type(e).__name__}: {str(e)}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")


@router.get("/profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile"""
    return {
        "user_id": current_user.uid,
        "profile": current_user.profile,
        "consents": current_user.consents,
    }


@router.put("/profile")
async def update_user_profile(
    request: UserProfileUpdateRequest, current_user: User = Depends(get_current_user)
):
    """Update current user's profile"""
    try:
        # Update Firebase Auth user record
        get_auth().update_user(
            current_user.uid, display_name=request.name or current_user.profile.name
        )

        # Update user profile in Firestore database
        updates = {}
        if request.name is not None:
            updates["profile.name"] = request.name
        if request.country is not None:
            updates["profile.country"] = request.country
        if request.risk_profile is not None:
            updates["profile.risk_profile"] = request.risk_profile

        if updates:
            success = await UserRepository().update_user(current_user.uid, updates)
            if not success:
                raise HTTPException(
                    status_code=500, detail="Failed to update profile in database"
                )

        return {"message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile update failed: {str(e)}")


@router.put("/consents")
async def update_user_consents(
    request: UserConsentUpdateRequest, current_user: User = Depends(get_current_user)
):
    """Update current user's consent preferences"""
    try:
        # Update user consents in Firestore database
        updates = {}
        if request.store_financial_snippets is not None:
            updates["consents.store_financial_snippets"] = (
                request.store_financial_snippets
            )
        if request.store_artifacts is not None:
            updates["consents.store_artifacts"] = request.store_artifacts
        if request.retention_days is not None:
            updates["consents.retention_days"] = request.retention_days

        if updates:
            success = await UserRepository().update_user(current_user.uid, updates)
            if not success:
                raise HTTPException(
                    status_code=500, detail="Failed to update consents in database"
                )

        return {"message": "Consents updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Consent update failed: {str(e)}")


@router.post("/logout")
async def logout_user(current_user: User = Depends(get_current_user)):
    """Logout user (client-side token invalidation)"""
    # Firebase tokens are stateless, so logout is handled client-side
    # This endpoint can be used for server-side cleanup if needed
    return {"message": "Logout successful"}
