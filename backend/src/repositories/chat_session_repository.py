from datetime import datetime
from typing import Any, Dict, List, Optional

from ..models import ChatSession
from .base_repository import BaseRepository


class ChatSessionRepository(BaseRepository[ChatSession]):
    """Repository for chat session operations"""

    def __init__(self):
        super().__init__("chat_sessions")

    async def create_session(
        self, user_id: str, title: str = "", settings: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new chat session for a user"""
        session_data = {
            "user_id": user_id,
            "title": title,
            "is_active": True,
            "settings": settings or {},
            "metadata": {},
        }
        return await self.create(session_data)

    async def get_user_sessions(
        self, user_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all chat sessions for a user"""
        filters = [("user_id", "==", user_id)]
        return await self.list(filters=filters, order_by="updated_at", limit=limit)

    async def get_active_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get the most recent active session for a user"""
        filters = [("user_id", "==", user_id), ("is_active", "==", True)]
        sessions = await self.list(filters=filters, order_by="updated_at", limit=1)
        return sessions[0] if sessions else None

    async def deactivate_session(self, session_id: str) -> bool:
        """Deactivate a chat session"""
        return await self.update(session_id, {"is_active": False})

    async def update_session_title(self, session_id: str, title: str) -> bool:
        """Update the title of a chat session"""
        return await self.update(session_id, {"title": title})

    async def update_session_settings(
        self, session_id: str, settings: Dict[str, Any]
    ) -> bool:
        """Update the settings of a chat session"""
        return await self.update(session_id, {"settings": settings})

    async def add_session_metadata(
        self, session_id: str, metadata: Dict[str, Any]
    ) -> bool:
        """Add metadata to a chat session"""
        # Get current metadata and merge
        current_session = await self.get(session_id)
        if current_session:
            current_metadata = current_session.get("metadata", {})
            current_metadata.update(metadata)
            return await self.update(session_id, {"metadata": current_metadata})
        return False
