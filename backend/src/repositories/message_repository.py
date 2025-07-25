from datetime import datetime
from typing import Any, Dict, List, Optional

from ..models import Message
from .base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """Repository for message operations"""

    def __init__(self):
        super().__init__("messages")

    async def create_message(
        self,
        session_id: str,
        user_id: str,
        role: str,
        content: Dict[str, Any],
        tokens_used: Optional[int] = None,
        processing_time: Optional[float] = None,
    ) -> str:
        """Create a new message in a chat session"""
        message_data = {
            "session_id": session_id,
            "user_id": user_id,
            "role": role,
            "content": content,
            "tokens_used": tokens_used,
            "processing_time": processing_time,
            "artifacts": [],
        }
        return await self.create(message_data)

    async def get_session_messages(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all messages for a chat session"""
        filters = [("session_id", "==", session_id)]
        return await self.list(filters=filters, order_by="created_at", limit=limit)

    async def get_session_messages_after(
        self, session_id: str, after_message_id: str
    ) -> List[Dict[str, Any]]:
        """Get messages in a session after a specific message ID"""
        # Get the timestamp of the after_message_id
        after_message = await self.get(after_message_id)
        if not after_message:
            return []

        after_timestamp = after_message.get("created_at")
        if not after_timestamp:
            return []

        filters = [
            ("session_id", "==", session_id),
            ("created_at", ">", after_timestamp),
        ]
        return await self.list(filters=filters, order_by="created_at")

    async def add_artifact_to_message(self, message_id: str, artifact_id: str) -> bool:
        """Add an artifact reference to a message"""
        message = await self.get(message_id)
        if message:
            artifacts = message.get("artifacts", [])
            if artifact_id not in artifacts:
                artifacts.append(artifact_id)
                return await self.update(message_id, {"artifacts": artifacts})
        return False

    async def update_message_processing_info(
        self, message_id: str, tokens_used: int, processing_time: float
    ) -> bool:
        """Update message with processing information"""
        return await self.update(
            message_id, {"tokens_used": tokens_used, "processing_time": processing_time}
        )

    async def get_user_messages(
        self, user_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all messages for a user across all sessions"""
        filters = [("user_id", "==", user_id)]
        return await self.list(filters=filters, order_by="created_at", limit=limit)

    async def delete_session_messages(self, session_id: str) -> bool:
        """Delete all messages for a session (for cleanup)"""
        try:
            messages = await self.get_session_messages(session_id)
            for message in messages:
                await self.delete(message["id"])
            return True
        except Exception:
            return False
