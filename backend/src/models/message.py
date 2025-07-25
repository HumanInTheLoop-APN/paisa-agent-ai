from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    CHART = "chart"
    JSON = "json"


class MessageContent(BaseModel):
    content: Any = Field(description="Message text content")
    type: MessageType = Field(description="Message type (text, image, chart, etc.)")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional message metadata"
    )


class Message(BaseModel):
    id: str = Field(description="Unique message identifier")
    session_id: str = Field(description="Chat session ID")
    user_id: str = Field(description="Firebase user ID")
    role: str = Field(description="Message role (user, assistant, system)")
    content: MessageContent = Field(description="Message content")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Message creation timestamp"
    )
    tokens_used: Optional[int] = Field(
        default=None, description="Number of tokens used"
    )
    processing_time: Optional[float] = Field(
        default=None, description="Processing time in seconds"
    )
    artifacts: List[str] = Field(
        default_factory=list,
        description="List of artifact IDs generated from this message",
    )
