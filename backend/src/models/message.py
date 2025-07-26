from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageType(str, Enum):
    TEXT = "text"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    ERROR = "error"


class MessageBase(BaseModel):
    session_id: str = Field(..., description="Chat session ID")
    user_id: str = Field(..., description="User ID for message ownership")
    role: MessageRole = Field(..., description="Message role (user/assistant/system)")
    content: str = Field(..., description="Message content")
    message_type: MessageType = Field(
        default=MessageType.TEXT, description="Message type"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Message(MessageBase):
    id: str = Field(..., description="Unique message ID")
    created_at: datetime = Field(..., description="Message creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    parent_message_id: Optional[str] = Field(
        None, description="Parent message ID for threading"
    )
    tool_calls: Optional[Dict[str, Any]] = Field(
        None, description="Tool call information"
    )
    tool_results: Optional[Dict[str, Any]] = Field(
        None, description="Tool result information"
    )

    class Config:
        from_attributes = True
