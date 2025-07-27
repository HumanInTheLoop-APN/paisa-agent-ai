from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    name: str = Field(default="", description="User's full name")
    email: str = Field(default="", description="User's email address")
    country: str = Field(default="IN", description="User's country code")
    risk_profile: str = Field(
        default="moderate", description="User's risk tolerance level"
    )


class UserConsents(BaseModel):
    store_financial_snippets: bool = Field(
        default=False, description="Consent to store financial data snippets"
    )
    store_artifacts: bool = Field(
        default=False, description="Consent to store generated artifacts"
    )
    retention_days: int = Field(default=30, description="Data retention period in days")
    granted_at: datetime = Field(
        default_factory=datetime.now, description="When consent was granted"
    )


class User(BaseModel):
    uid: str = Field(description="Firebase user ID")
    profile: UserProfile = Field(
        default_factory=UserProfile, description="User profile information"
    )
    consents: UserConsents = Field(
        default_factory=UserConsents, description="User consent preferences"
    )


class UserCreate(BaseModel):
    uid: str = Field(description="Firebase user ID")
    profile: UserProfile = Field(
        default_factory=UserProfile, description="User profile information"
    )
    consents: UserConsents = Field(
        default_factory=UserConsents, description="User consent preferences"
    )


class UserUpdate(BaseModel):
    profile: UserProfile = Field(
        default_factory=UserProfile, description="User profile information"
    )
    consents: UserConsents = Field(
        default_factory=UserConsents, description="User consent preferences"
    )
