from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Artifact(BaseModel):
    id: str = Field(description="Unique artifact identifier")
    user_id: str = Field(description="Firebase user ID")
    session_id: str = Field(description="Chat session ID")
    message_id: str = Field(description="Source message ID")
    type: str = Field(description="Artifact type (chart, report, analysis, etc.)")
    title: str = Field(description="Artifact title")
    content: str = Field(description="Artifact content (JSON, HTML, etc.)")
    file_path: Optional[str] = Field(
        default=None, description="Path to stored file if applicable"
    )
    mime_type: str = Field(description="MIME type of the artifact")
    size_bytes: Optional[int] = Field(default=None, description="Size in bytes")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional artifact metadata"
    )
