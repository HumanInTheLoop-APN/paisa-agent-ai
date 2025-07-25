from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ChatSessionSettings(BaseModel):
    model: str = Field(default="gpt-4", description="AI model to use for responses")
    temperature: float = Field(
        default=0.7, description="Response creativity level (0.0-1.0)"
    )
    max_tokens: int = Field(default=1000, description="Maximum tokens in response")
    language: str = Field(default="en", description="Preferred language for responses")


class ChatSession(BaseModel):
    id: str = Field(description="Unique session identifier")
    user_id: str = Field(description="Firebase user ID")
    title: str = Field(default="", description="Session title")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Session creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last activity timestamp"
    )
    is_active: bool = Field(
        default=True, description="Whether session is currently active"
    )
    settings: ChatSessionSettings = Field(
        default_factory=ChatSessionSettings, description="Session-specific settings"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional session metadata"
    )
