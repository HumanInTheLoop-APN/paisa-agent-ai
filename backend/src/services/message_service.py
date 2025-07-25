from datetime import datetime
from typing import Any, Dict, List, Optional

from ..models import Message, MessageContent, MessageType
from ..repositories import MessageRepository


class MessageService:
    """Service class for message business logic"""

    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo

    async def create_message(
        self,
        session_id: str,
        user_id: str,
        role: str,
        content: str,
        message_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new message with business logic validation"""
        # Validate inputs
        if not session_id or not user_id or not role or not content:
            raise ValueError("Session ID, User ID, Role, and Content are required")

        # Validate role
        valid_roles = ["user", "assistant", "system"]
        if role not in valid_roles:
            raise ValueError(f"Role must be one of: {valid_roles}")

        # Validate message type
        try:
            message_type_enum = MessageType(message_type)
        except ValueError:
            raise ValueError(f"Invalid message type: {message_type}")

        # Create message content
        message_content = {
            "content": content,
            "type": message_type_enum.value,
            "metadata": metadata or {},
        }

        # Create message
        message_id = await self.message_repo.create_message(
            session_id=session_id, user_id=user_id, role=role, content=message_content
        )

        # Return created message
        return await self.message_repo.get(message_id)

    async def get_session_messages(
        self, session_id: str, user_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get messages for a session with access control"""
        if not session_id or not user_id:
            raise ValueError("Session ID and User ID are required")

        messages = await self.message_repo.get_session_messages(session_id, limit)

        # Filter messages by user access (in a real app, you'd check session ownership)
        # For now, we'll return all messages for the session
        return messages

    async def get_message(
        self, message_id: str, user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get a specific message with access control"""
        if not message_id or not user_id:
            raise ValueError("Message ID and User ID are required")

        message = await self.message_repo.get(message_id)

        # Check access control (in a real app, you'd check session ownership)
        if message and message.get("user_id") != user_id:
            raise PermissionError("Access denied to this message")

        return message

    async def update_message_processing_info(
        self, message_id: str, user_id: str, tokens_used: int, processing_time: float
    ) -> bool:
        """Update message with processing information"""
        # Verify access
        message = await self.get_message(message_id, user_id)
        if not message:
            return False

        return await self.message_repo.update_message_processing_info(
            message_id, tokens_used, processing_time
        )

    async def add_artifact_to_message(
        self, message_id: str, user_id: str, artifact_id: str
    ) -> bool:
        """Add an artifact reference to a message"""
        # Verify access
        message = await self.get_message(message_id, user_id)
        if not message:
            return False

        return await self.message_repo.add_artifact_to_message(message_id, artifact_id)

    async def get_conversation_context(
        self, session_id: str, user_id: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent messages for conversation context"""
        messages = await self.get_session_messages(session_id, user_id, limit)

        # Format for conversation context
        context = []
        for message in messages:
            context.append(
                {
                    "role": message.get("role"),
                    "content": message.get("content", {}).get("content", ""),
                    "timestamp": message.get("created_at"),
                }
            )

        return context

    async def get_session_message_count(self, session_id: str) -> int:
        """Get the number of messages in a session"""
        messages = await self.message_repo.get_session_messages(session_id)
        return len(messages)

    async def delete_session_messages(self, session_id: str, user_id: str) -> bool:
        """Delete all messages for a session (for cleanup)"""
        # Verify access (in a real app, you'd check session ownership)
        if not session_id or not user_id:
            return False

        return await self.message_repo.delete_session_messages(session_id)
