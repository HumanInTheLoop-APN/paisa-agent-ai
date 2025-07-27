from typing import List, Optional

from fastapi import HTTPException

from ..models.chat_session import (
    ChatSession,
    ChatSessionCreate,
    ChatSessionUpdate,
)
from ..repositories import ChatSessionRepository, MessageRepository


class ChatSessionService:
    """Service for chat session operations"""

    def __init__(
        self,
        chat_session_repository: ChatSessionRepository,
        message_repository: MessageRepository,
    ):
        self.repository = chat_session_repository
        self.message_repository = message_repository

    async def create_session(
        self,
        user_id: str,
    ) -> ChatSession:
        """Create a new chat session for a user"""
        try:
            session_data = ChatSessionCreate(user_id=user_id)
            return await self.repository.create_session(session_data)
        except Exception as e:
            print(f"Error creating chat session: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_user_sessions(
        self, user_id: str, limit: Optional[int] = None
    ) -> List[ChatSession]:
        """Get all sessions for a specific user"""
        return await self.repository.get_user_sessions(user_id, limit)

    async def get_session(self, session_id: str, user_id: str) -> Optional[ChatSession]:
        """Get a specific session for a user (ensures ownership)"""
        return await self.repository.get_session_by_user(session_id, user_id)

    async def update_session(
        self,
        session_id: str,
        user_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[ChatSession]:
        """Update a session (ensures ownership)"""
        update_data = ChatSessionUpdate(title=title, description=description)
        return await self.repository.update_session(session_id, user_id, update_data)

    async def delete_session(self, session_id: str, user_id: str) -> bool:
        """Delete a session (ensures ownership)"""
        return await self.repository.delete_session(session_id, user_id)

    async def deactivate_session(self, session_id: str, user_id: str) -> bool:
        """Deactivate a session (ensures ownership)"""
        return await self.repository.deactivate_session(session_id, user_id)

    async def increment_message_count(self, session_id: str) -> bool:
        """Increment the message count for a session"""
        return await self.repository.increment_message_count(session_id)

    async def get_active_sessions(self, user_id: str) -> List[ChatSession]:
        """Get all active sessions for a user"""
        sessions = await self.get_user_sessions(user_id)
        return [session for session in sessions if session.is_active]

    async def get_session_summary(
        self, session_id: str, user_id: str
    ) -> Optional[dict]:
        """Get a summary of a session including message count and last activity"""
        session = await self.get_session(session_id, user_id)
        if not session:
            return None

        return {
            "id": session.id,
            "title": session.title,
            "description": session.description,
            "message_count": session.message_count,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
            "is_active": session.is_active,
        }
