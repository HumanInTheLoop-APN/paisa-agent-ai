from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ArtifactType(str, Enum):
    CHART = "chart"
    REPORT = "report"
    ANALYSIS = "analysis"
    RECOMMENDATION = "recommendation"
    VISUALIZATION = "visualization"
    DATA_EXPORT = "data_export"


class ArtifactStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ArtifactBase(BaseModel):
    session_id: str = Field(..., description="Chat session ID")
    user_id: str = Field(..., description="User ID for artifact ownership")
    message_id: str = Field(..., description="Message ID that generated this artifact")
    artifact_type: ArtifactType = Field(..., description="Type of artifact")
    title: str = Field(..., description="Artifact title")
    description: Optional[str] = Field(None, description="Artifact description")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class ArtifactCreate(ArtifactBase):
    pass


class ArtifactUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ArtifactStatus] = None
    content: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


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

    class Config:
        from_attributes = True
