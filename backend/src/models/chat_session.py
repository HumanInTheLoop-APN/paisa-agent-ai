from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatSessionBase(BaseModel):
    user_id: str = Field(..., description="User ID for session ownership")


class ChatSessionCreate(ChatSessionBase):
    title: str = Field(default="Untitled", description="Session title")
    description: str = Field(
        default="No description", description="Session description"
    )


class ChatSessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ChatSession(ChatSessionBase):
    id: str = Field(..., description="Unique session ID")
    title: str = Field(..., description="Session title")
    description: str = Field(..., description="Session description")
    created_at: datetime = Field(..., description="Session creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    message_count: int = Field(default=0, description="Number of messages in session")
    is_active: bool = Field(default=True, description="Session active status")

    class Config:
        from_attributes = True
