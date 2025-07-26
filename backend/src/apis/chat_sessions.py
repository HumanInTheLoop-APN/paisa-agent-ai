from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from ..auth.firebase_auth import get_current_user

router = APIRouter()


class ChatSessionCreateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ChatSessionUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ChatSessionResponse(BaseModel):
    id: str
    user_id: str
    title: Optional[str]
    description: Optional[str]
    created_at: str
    updated_at: str
    message_count: int
    is_active: bool

    class Config:
        from_attributes = True


@router.post("/", response_model=ChatSessionResponse)
async def create_chat_session(
    request: ChatSessionCreateRequest, current_user: dict = Depends(get_current_user)
):
    """Create a new chat session for the current user"""
    try:
        user_id = current_user["uid"]
        session = await chat_session_service.create_session(
            user_id=user_id, title=request.title, description=request.description
        )
        return ChatSessionResponse.from_orm(session)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create session: {str(e)}"
        )


@router.get("/", response_model=List[ChatSessionResponse])
async def get_user_sessions(
    limit: Optional[int] = Query(None, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    """Get all chat sessions for the current user"""
    try:
        user_id = current_user["uid"]
        sessions = await chat_session_service.get_user_sessions(user_id, limit)
        return [ChatSessionResponse.from_orm(session) for session in sessions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sessions: {str(e)}")


@router.get("/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str, current_user: dict = Depends(get_current_user)
):
    """Get a specific chat session for the current user"""
    try:
        user_id = current_user["uid"]
        session = await chat_session_service.get_session(session_id, user_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return ChatSessionResponse.from_orm(session)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session: {str(e)}")


@router.put("/{session_id}", response_model=ChatSessionResponse)
async def update_chat_session(
    session_id: str,
    request: ChatSessionUpdateRequest,
    current_user: dict = Depends(get_current_user),
):
    """Update a chat session for the current user"""
    try:
        user_id = current_user["uid"]
        session = await chat_session_service.update_session(
            session_id=session_id,
            user_id=user_id,
            title=request.title,
            description=request.description,
        )
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return ChatSessionResponse.from_orm(session)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update session: {str(e)}"
        )


@router.delete("/{session_id}")
async def delete_chat_session(
    session_id: str, current_user: dict = Depends(get_current_user)
):
    """Delete a chat session for the current user"""
    try:
        user_id = current_user["uid"]
        success = await chat_session_service.delete_session(session_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Session deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete session: {str(e)}"
        )


@router.post("/{session_id}/deactivate")
async def deactivate_chat_session(
    session_id: str, current_user: dict = Depends(get_current_user)
):
    """Deactivate a chat session for the current user"""
    try:
        user_id = current_user["uid"]
        success = await chat_session_service.deactivate_session(session_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"message": "Session deactivated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to deactivate session: {str(e)}"
        )


@router.get("/{session_id}/summary")
async def get_session_summary(
    session_id: str, current_user: dict = Depends(get_current_user)
):
    """Get a summary of a chat session"""
    try:
        user_id = current_user["uid"]
        summary = await chat_session_service.get_session_summary(session_id, user_id)
        if not summary:
            raise HTTPException(status_code=404, detail="Session not found")
        return summary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get session summary: {str(e)}"
        )
