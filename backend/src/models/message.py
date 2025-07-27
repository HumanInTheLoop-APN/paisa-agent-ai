from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class UsageMetadata(BaseModel):
    """Usage metadata for events and messages"""

    prompt_token_count: Optional[int] = Field(
        None, description="Number of tokens in prompt"
    )
    response_token_count: Optional[int] = Field(
        None, description="Number of tokens in response"
    )
    total_token_count: Optional[int] = Field(None, description="Total tokens used")
    model_name: Optional[str] = Field(None, description="Model used for generation")
    invocation_id: Optional[str] = Field(None, description="Unique invocation ID")
    processing_time: Optional[float] = Field(
        None, description="Processing time in seconds"
    )
    cost_estimate: Optional[float] = Field(None, description="Estimated cost in USD")


class MessageEvent(BaseModel):
    """Individual event within a message response"""

    event_id: str = Field(..., description="Unique event ID")
    timestamp: datetime = Field(..., description="Event timestamp")
    sequence_number: int = Field(..., description="Order of events in the response")

    # Author information
    author: str = Field(..., description="Author of the event (agent name)")

    # Content information
    content: Optional[str] = Field(None, description="Text content for text events")

    # Tool-related data
    tool_calls: Optional[List[Dict[str, Any]]] = Field(
        None, description="Tool calls in this event"
    )
    tool_results: Optional[List[Dict[str, Any]]] = Field(
        None, description="Tool results in this event"
    )

    # Event-specific metadata
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Event-specific metadata"
    )

    # Usage and performance metadata
    usage_metadata: Optional[UsageMetadata] = Field(
        None, description="Usage and performance data"
    )

    error_code: Optional[str] = Field(None, description="Error code if any")
    error_message: Optional[str] = Field(None, description="Error message if any")
    interrupted: Optional[bool] = Field(
        None, description="Whether the response was interrupted"
    )
    custom_metadata: Optional[Dict[str, Any]] = Field(
        None, description="Custom metadata from ADK"
    )
    long_running_tool_ids: Optional[List[str]] = Field(
        None, description="Long running tool IDs"
    )
    branch: Optional[str] = Field(None, description="Branch information")
    id: Optional[str] = Field(None, description="ADK event ID")


class MessageBase(BaseModel):
    session_id: str = Field(..., description="Chat session ID")
    user_id: str = Field(..., description="User ID for message ownership")
    role: MessageRole = Field(..., description="Message role (user/assistant/system)")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class MessageCreate(MessageBase):
    # For human messages (user role)
    human_content: Optional[str] = Field(None, description="Human message content")

    # For assistant messages (assistant role)
    events: Optional[List[MessageEvent]] = Field(
        default=None, description="Structured events (for assistant messages)"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class MessageUpdate(BaseModel):
    human_content: Optional[str] = None
    events: Optional[List[MessageEvent]] = None
    metadata: Optional[Dict[str, Any]] = None


class Message(MessageBase):
    id: str = Field(..., description="Unique message ID")
    created_at: datetime = Field(..., description="Message creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    parent_message_id: Optional[str] = Field(
        None, description="Parent message ID for threading"
    )

    # Human message content (for user role)
    human_content: Optional[str] = Field(None, description="Human message content")

    # Assistant message events (for assistant role)
    events: Optional[List[MessageEvent]] = Field(
        default_factory=list, description="Ordered list of response events"
    )

    # Aggregated metadata from events
    response_metadata: Optional[Dict[str, Any]] = Field(
        None, description="Response-level metadata"
    )

    # Aggregated usage metadata
    total_usage_metadata: Optional[UsageMetadata] = Field(
        None, description="Aggregated usage metadata from all events"
    )

    # Authors involved in the response
    authors: Optional[List[str]] = Field(
        default_factory=list, description="List of authors involved in the response"
    )

    # Processing status
    processing_complete: Optional[bool] = Field(
        default=False, description="Whether all events have been processed"
    )

    # Error information
    has_errors: bool = Field(
        default=False, description="Whether any events contain errors"
    )
    error_summary: Optional[Dict[str, Any]] = Field(
        None, description="Summary of errors if any"
    )

    class Config:
        from_attributes = True


# API Request/Response Models
class MessageCreateRequest(BaseModel):
    human_content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    parent_message_id: Optional[str] = None


class MessageUpdateRequest(BaseModel):
    human_content: Optional[str] = None
    events: Optional[List[MessageEvent]] = None
    metadata: Optional[Dict[str, Any]] = None


class MessageResponse(BaseModel):
    """Enhanced message response with structured events"""

    id: str
    session_id: str
    user_id: str
    role: MessageRole
    created_at: Union[str, datetime]
    updated_at: Union[str, datetime]
    parent_message_id: Optional[str]

    # Human message content
    human_content: Optional[str] = Field(None, description="Human message content")

    # Structured response data
    events: Optional[List[MessageEvent]] = Field(
        None, description="Ordered list of response events"
    )

    # Response metadata
    response_metadata: Optional[Dict[str, Any]] = Field(
        None, description="Response-level metadata"
    )

    # Aggregated usage metadata
    total_usage_metadata: Optional[UsageMetadata] = Field(
        None, description="Aggregated usage metadata"
    )

    # Authors involved
    authors: Optional[List[str]] = Field(
        default_factory=list, description="List of authors"
    )

    # Processing status
    processing_complete: Optional[bool] = Field(
        default=False, description="Processing complete status"
    )
    has_errors: Optional[bool] = Field(default=False, description="Has errors status")
    error_summary: Optional[Dict[str, Any]] = Field(None, description="Error summary")

    class Config:
        from_attributes = True


# Streaming Event Model
class StreamingEvent(BaseModel):
    """Individual event for streaming to UI"""

    message_id: str = Field(..., description="Parent message ID")
    event: MessageEvent = Field(..., description="The event being streamed")
    is_complete: bool = Field(False, description="Whether this is the final event")
    current_event_number: int = Field(..., description="Current event number")


# Chat Response Models
class ChatMessageRequest(BaseModel):
    human_content: str = Field(..., description="Human message content")
    metadata: Optional[Dict[str, Any]] = None


class ChatMessageResponse(BaseModel):
    success: bool
    user_message: MessageResponse
    assistant_message: Optional[MessageResponse] = None
    error: Optional[str] = None
    events: Optional[List[MessageEvent]] = None  # For streaming support
    total_usage_metadata: Optional[UsageMetadata] = Field(
        None, description="Total usage for the chat"
    )
