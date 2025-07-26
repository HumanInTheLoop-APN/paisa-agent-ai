from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatSessionBase(BaseModel):
    user_id: str = Field(..., description="User ID for session ownership")
    title: Optional[str] = Field(None, description="Session title")
    description: Optional[str] = Field(None, description="Session description")


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ChatSession(ChatSessionBase):
    id: str = Field(..., description="Unique session ID")
    created_at: datetime = Field(..., description="Session creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    message_count: int = Field(default=0, description="Number of messages in session")
    is_active: bool = Field(default=True, description="Session active status")

    class Config:
        from_attributes = True
