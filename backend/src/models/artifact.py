from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ArtifactType(str, Enum):
    # AI Generated Artifacts
    CHART = "chart"
    REPORT = "report"
    ANALYSIS = "analysis"
    RECOMMENDATION = "recommendation"
    VISUALIZATION = "visualization"
    DATA_EXPORT = "data_export"

    # User Uploaded Artifacts
    PDF = "pdf"
    CSV = "csv"
    IMAGE = "image"
    DOCUMENT = "document"
    SPREADSHEET = "spreadsheet"
    OTHER = "other"


class ArtifactSource(str, Enum):
    USER_UPLOAD = "user_upload"
    AI_GENERATED = "ai_generated"


class ArtifactStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CONSENT_REQUIRED = "consent_required"
    CONSENT_DENIED = "consent_denied"


class ArtifactBase(BaseModel):
    session_id: str = Field(..., description="Chat session ID")
    user_id: str = Field(..., description="User ID for artifact ownership")
    message_id: str = Field(..., description="Message ID that generated this artifact")
    artifact_type: ArtifactType = Field(..., description="Type of artifact")
    source: ArtifactSource = Field(
        ..., description="Source of artifact (user upload or AI generated)"
    )
    title: str = Field(..., description="Artifact title")
    description: Optional[str] = Field(None, description="Artifact description")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )
    consent_required: bool = Field(
        default=False, description="Whether user consent is required for storage"
    )
    consent_granted: Optional[bool] = Field(
        default=None, description="Whether user has granted consent for this artifact"
    )


class ArtifactCreate(ArtifactBase):
    pass


class ArtifactUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ArtifactStatus] = None
    content: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    consent_granted: Optional[bool] = None


class Artifact(ArtifactBase):
    id: str = Field(..., description="Unique artifact ID")
    created_at: datetime = Field(..., description="Artifact creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    status: ArtifactStatus = Field(
        default=ArtifactStatus.PENDING, description="Processing status"
    )
    content: Optional[Dict[str, Any]] = Field(None, description="Artifact content/data")
    file_path: Optional[str] = Field(None, description="File path if stored on disk")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    mime_type: Optional[str] = Field(None, description="MIME type of the artifact")
    original_filename: Optional[str] = Field(
        None, description="Original filename for uploads"
    )
    storage_uri: Optional[str] = Field(
        None, description="Cloud storage URI if stored remotely"
    )
    retention_expires_at: Optional[datetime] = Field(
        None, description="When this artifact should be automatically deleted"
    )

    class Config:
        from_attributes = True
