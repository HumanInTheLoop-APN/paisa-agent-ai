from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..auth.firebase_auth import GetCurrentUserDep
from ..dependencies import MessageServiceDep, RunnerManagerServiceDep
from ..models.message import MessageResponse, MessageRole

router = APIRouter()


class MessageCreateRequest(BaseModel):
    human_content: str
    metadata: Optional[Dict[str, Any]] = None


class MessageUpdateRequest(BaseModel):
    human_content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


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
            human_content=request.human_content,
            metadata=request.metadata,
        )
        return MessageResponse.model_validate(message)
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
        return [MessageResponse.model_validate(message) for message in messages]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get messages: {str(e)}")


@router.get(
    "/{session_id}/messages/{message_id}",
    response_model=MessageResponse,
)
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
        return MessageResponse.model_validate(message)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get message: {str(e)}")


@router.put("/{session_id}/messages/{message_id}", response_model=MessageResponse)
async def update_message(
    session_id: str,
    message_id: str,
    request: MessageUpdateRequest,
    current_user: GetCurrentUserDep,
    message_service: MessageServiceDep,
):
    """Update a message in a chat session"""
    try:
        user_id = current_user.uid
        message = await message_service.update_message(
            message_id=message_id,
            user_id=user_id,
            human_content=request.human_content,
            metadata=request.metadata,
        )
        if not message or message.session_id != session_id:
            raise HTTPException(status_code=404, detail="Message not found")
        return MessageResponse.model_validate(message)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update message: {str(e)}"
        )


@router.delete("/{session_id}/messages/{message_id}")
async def delete_message(
    session_id: str,
    message_id: str,
    current_user: GetCurrentUserDep,
    message_service: MessageServiceDep,
):
    """Delete a message from a chat session"""
    try:
        user_id = current_user.uid
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


@router.post("/{session_id}/chat")
async def send_chat_message(
    session_id: str,
    request: ChatMessageRequest,
    current_user: GetCurrentUserDep,
    runner_manager_service: RunnerManagerServiceDep,
    message_service: MessageServiceDep,
):
    """Send a chat message and get AI response"""
    try:
        user_id = current_user.uid

        async def event_stream():
            # Process message through agent system
            async for event in runner_manager_service.process_user_message(
                user_id=user_id,
                session_id=session_id,
                message_content=request.content,
                backend_session_id=session_id,
            ):
                yield event

        return StreamingResponse(event_stream(), media_type="application/json")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process chat message: {str(e)}"
        )


@router.get("/{session_id}/conversation", response_model=List[MessageResponse])
async def get_user_conversation(
    session_id: str,
    current_user: GetCurrentUserDep,
    message_service: MessageServiceDep,
    limit: Optional[int] = Query(None, ge=1, le=100),
):
    """Get all messages for the current user across all sessions"""
    try:
        user_id = current_user.uid
        messages = await message_service.get_session_messages(
            session_id=session_id, user_id=user_id, limit=limit
        )
        return [MessageResponse.model_validate(message) for message in messages]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get user conversation: {str(e)}"
        )
