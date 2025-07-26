from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from ..auth.firebase_auth import GetCurrentUserDep, get_current_user
from ..dependencies import MessageServiceDep
from ..models.message import (
    Message,
    MessageCreate,
    MessageRole,
    MessageType,
    MessageUpdate,
)
from ..services.message_service import MessageService
from ..services.runner_manager_service import RunnerManagerService

router = APIRouter()


class MessageCreateRequest(BaseModel):
    content: str
    message_type: MessageType = MessageType.TEXT
    metadata: Optional[Dict[str, Any]] = None
    parent_message_id: Optional[str] = None


class MessageUpdateRequest(BaseModel):
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MessageResponse(BaseModel):
    id: str
    session_id: str
    user_id: str
    role: MessageRole
    content: str
    message_type: MessageType
    metadata: Optional[Dict[str, Any]]
    created_at: str
    updated_at: str
    parent_message_id: Optional[str]
    tool_calls: Optional[Dict[str, Any]]
    tool_results: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True


class ChatMessageRequest(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None


class ChatMessageResponse(BaseModel):
    success: bool
    user_message: MessageResponse
    assistant_message: Optional[MessageResponse] = None
    response: Optional[str] = None
    error: Optional[str] = None


@router.post("/{session_id}/messages", response_model=MessageResponse)
async def create_message(
    session_id: str,
    request: MessageCreateRequest,
    current_user: GetCurrentUserDep,
    message_service: MessageServiceDep,
):
    """Create a new message in a chat session"""
    try:
        user_id = current_user.uid
        message = await message_service.create_message(
            session_id=session_id,
            user_id=user_id,
            role=MessageRole.USER,
            content=request.content,
            message_type=request.message_type,
            metadata=request.metadata,
            parent_message_id=request.parent_message_id,
        )
        return MessageResponse.from_orm(message)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create message: {str(e)}"
        )


@router.get("/{session_id}/messages", response_model=List[MessageResponse])
async def get_session_messages(
    session_id: str,
    current_user: GetCurrentUserDep,
    message_service: MessageServiceDep,
    limit: Optional[int] = Query(None, ge=1, le=100),
):
    """Get all messages for a specific chat session"""
    try:
        user_id = current_user.uid
        messages = await message_service.get_session_messages(
            session_id, user_id, limit
        )
        return [MessageResponse.from_orm(message) for message in messages]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get messages: {str(e)}")


@router.get("/{session_id}/messages/{message_id}", response_model=MessageResponse)
async def get_message(
    session_id: str,
    message_id: str,
    current_user: GetCurrentUserDep,
    message_service: MessageServiceDep,
):
    """Get a specific message from a chat session"""
    try:
        user_id = current_user.uid
        message = await message_service.get_message(message_id, user_id)
        if not message or message.session_id != session_id:
            raise HTTPException(status_code=404, detail="Message not found")
        return MessageResponse.from_orm(message)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get message: {str(e)}")


@router.put("/{session_id}/messages/{message_id}", response_model=MessageResponse)
async def update_message(
    session_id: str,
    message_id: str,
    request: MessageUpdateRequest,
    current_user: dict = Depends(get_current_user),
):
    """Update a message in a chat session"""
    try:
        user_id = current_user["uid"]
        message = await message_service.update_message(
            message_id=message_id,
            user_id=user_id,
            content=request.content,
            metadata=request.metadata,
        )
        if not message or message.session_id != session_id:
            raise HTTPException(status_code=404, detail="Message not found")
        return MessageResponse.from_orm(message)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update message: {str(e)}"
        )


@router.delete("/{session_id}/messages/{message_id}")
async def delete_message(
    session_id: str, message_id: str, current_user: dict = Depends(get_current_user)
):
    """Delete a message from a chat session"""
    try:
        user_id = current_user["uid"]
        message = await message_service.get_message(message_id, user_id)
        if not message or message.session_id != session_id:
            raise HTTPException(status_code=404, detail="Message not found")

        success = await message_service.delete_message(message_id, user_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete message")

        return {"message": "Message deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete message: {str(e)}"
        )


@router.post("/{session_id}/chat", response_model=ChatMessageResponse)
async def send_chat_message(
    session_id: str,
    request: ChatMessageRequest,
    current_user: dict = Depends(get_current_user),
):
    """Send a chat message and get AI response"""
    try:
        user_id = current_user["uid"]

        # Process message through agent system
        result = await runner_manager_service.process_user_message(
            user_id=user_id,
            session_id=session_id,
            message_content=request.content,
            backend_session_id=session_id,
        )

        # Get the created messages
        user_message = await message_service.get_message(
            result["user_message_id"], user_id
        )
        assistant_message = None
        if result.get("assistant_message_id"):
            assistant_message = await message_service.get_message(
                result["assistant_message_id"], user_id
            )

        return ChatMessageResponse(
            success=result["success"],
            user_message=MessageResponse.from_orm(user_message),
            assistant_message=(
                MessageResponse.from_orm(assistant_message)
                if assistant_message
                else None
            ),
            response=result.get("response"),
            error=result.get("error"),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process chat message: {str(e)}"
        )


@router.get("/{session_id}/messages/role/{role}", response_model=List[MessageResponse])
async def get_messages_by_role(
    session_id: str, role: MessageRole, current_user: dict = Depends(get_current_user)
):
    """Get messages by role for a specific session"""
    try:
        user_id = current_user["uid"]
        messages = await message_service.get_messages_by_role(session_id, user_id, role)
        return [MessageResponse.from_orm(message) for message in messages]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get messages by role: {str(e)}"
        )


@router.get(
    "/{session_id}/messages/{message_id}/thread", response_model=List[MessageResponse]
)
async def get_conversation_thread(
    session_id: str, message_id: str, current_user: dict = Depends(get_current_user)
):
    """Get a conversation thread starting from a specific message"""
    try:
        user_id = current_user["uid"]
        messages = await message_service.get_conversation_thread(message_id, user_id)
        # Filter to ensure all messages are from the same session
        session_messages = [msg for msg in messages if msg.session_id == session_id]
        return [MessageResponse.from_orm(message) for message in session_messages]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get conversation thread: {str(e)}"
        )


@router.get("/conversation", response_model=List[MessageResponse])
async def get_user_conversation(
    limit: Optional[int] = Query(None, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    """Get all messages for the current user across all sessions"""
    try:
        user_id = current_user["uid"]
        messages = await message_service.get_user_messages(user_id, limit)
        return [MessageResponse.from_orm(message) for message in messages]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get user conversation: {str(e)}"
        )
