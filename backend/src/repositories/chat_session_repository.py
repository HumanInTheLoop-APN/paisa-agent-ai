from typing import Any, Dict, List, Optional

from ..models.chat_session import (
    ChatSession,
    ChatSessionCreate,
    ChatSessionUpdate,
)
from .base_repository import BaseRepository


class ChatSessionRepository(BaseRepository[ChatSession]):
    """Repository for chat session operations"""

    def __init__(self, db=None):
        super().__init__("chat_sessions", db=db)
        self._item_type = ChatSession

    def _get_key(self, item: ChatSession) -> str:
        """Get the unique key for a chat session"""
        return item.id

    def _validate_item(self, item: ChatSession) -> bool:
        """Validate a chat session before storage"""
        return (
            hasattr(item, "user_id")
            and item.user_id is not None
            and hasattr(item, "id")
            and item.id is not None
        )

    def _reconstruct_item(self, data: Dict[str, Any]) -> ChatSession:
        """Reconstruct a ChatSession from stored data"""
        return ChatSession(**data)

    async def create_session(self, session_data: ChatSessionCreate) -> ChatSession:
        """Create a new chat session"""
        session = ChatSession(
            id=None,  # Will be set by base repository
            user_id=session_data.user_id,
            title=session_data.title,
            description=session_data.description,
            created_at=None,  # Will be set by base repository
            updated_at=None,  # Will be set by base repository
            message_count=0,
            is_active=True,
        )
        return await self.create(session)

    async def get_user_sessions(
        self, user_id: str, limit: Optional[int] = None
    ) -> List[ChatSession]:
        """Get all sessions for a specific user"""
        sessions = await self.get_by_field("user_id", user_id)

        # Sort by updated_at descending (most recent first)
        sessions.sort(key=lambda x: x.updated_at, reverse=True)

        if limit:
            sessions = sessions[:limit]

        return sessions

    async def get_session_by_user(
        self, session_id: str, user_id: str
    ) -> Optional[ChatSession]:
        """Get a specific session for a user (ensures ownership)"""
        session = await self.get_by_id(session_id)
        if session and session.user_id == user_id:
            return session
        return None

    async def update_session(
        self, session_id: str, user_id: str, update_data: ChatSessionUpdate
    ) -> Optional[ChatSession]:
        """Update a session (ensures ownership)"""
        session = await self.get_session_by_user(session_id, user_id)
        if not session:
            return None

        # Apply updates
        if update_data.title is not None:
            session.title = update_data.title
        if update_data.description is not None:
            session.description = update_data.description

        return await self.update(session)

    async def delete_session(self, session_id: str, user_id: str) -> bool:
        """Delete a session (ensures ownership)"""
        session = await self.get_session_by_user(session_id, user_id)
        if not session:
            return False

        return await self.delete(session_id)

    async def increment_message_count(self, session_id: str) -> bool:
        """Increment the message count for a session"""
        session = await self.get_by_id(session_id)
        if not session:
            return False

        session.message_count += 1
        await self.update(session)
        return True

    async def deactivate_session(self, session_id: str, user_id: str) -> bool:
        """Deactivate a session (ensures ownership)"""
        session = await self.get_session_by_user(session_id, user_id)
        if not session:
            return False

        session.is_active = False
        await self.update(session)
        return True
