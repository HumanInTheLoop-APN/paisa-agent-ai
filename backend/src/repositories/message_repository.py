from typing import Any, Dict, List, Optional

from ..models.message import Message, MessageCreate, MessageRole, MessageUpdate
from .base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """Repository for message operations"""

    def __init__(self):
        super().__init__("messages")
        self._item_type = Message

    def _get_key(self, item: Message) -> str:
        """Get the unique key for a message"""
        return item.id

    def _validate_item(self, item: Message) -> bool:
        """Validate a message before storage"""
        return (
            hasattr(item, "session_id")
            and item.session_id is not None
            and hasattr(item, "user_id")
            and item.user_id is not None
            and hasattr(item, "role")
            and item.role is not None
            and hasattr(item, "content")
            and item.content is not None
            and hasattr(item, "id")
            and item.id is not None
        )

    def _reconstruct_item(self, data: Dict[str, Any]) -> Message:
        """Reconstruct a Message from stored data"""
        return Message(**data)

    async def create_message(self, message_data: MessageCreate) -> Message:
        """Create a new message"""
        message = Message(
            id=None,  # Will be set by base repository
            session_id=message_data.session_id,
            user_id=message_data.user_id,
            role=message_data.role,
            content=message_data.content,
            message_type=message_data.message_type,
            metadata=message_data.metadata,
            created_at=None,  # Will be set by base repository
            updated_at=None,  # Will be set by base repository
            parent_message_id=None,
            tool_calls=None,
            tool_results=None,
        )
        return await self.create(message)

    async def get_session_messages(
        self, session_id: str, user_id: str, limit: Optional[int] = None
    ) -> List[Message]:
        """Get all messages for a specific session (ensures ownership)"""
        # First verify session ownership
        from .chat_session_repository import ChatSessionRepository

        session_repo = ChatSessionRepository()
        session = await session_repo.get_session_by_user(session_id, user_id)
        if not session:
            return []

        messages = await self.get_by_field("session_id", session_id)

        # Sort by created_at ascending (chronological order)
        messages.sort(key=lambda x: x.created_at)

        if limit:
            messages = messages[-limit:]  # Get the most recent messages

        return messages

    async def get_message_by_user(
        self, message_id: str, user_id: str
    ) -> Optional[Message]:
        """Get a specific message for a user (ensures ownership)"""
        message = await self.get_by_id(message_id)
        if message and message.user_id == user_id:
            return message
        return None

    async def update_message(
        self, message_id: str, user_id: str, update_data: MessageUpdate
    ) -> Optional[Message]:
        """Update a message (ensures ownership)"""
        message = await self.get_message_by_user(message_id, user_id)
        if not message:
            return None

        # Apply updates
        if update_data.content is not None:
            message.content = update_data.content
        if update_data.metadata is not None:
            message.metadata = update_data.metadata

        return await self.update(message)

    async def delete_message(self, message_id: str, user_id: str) -> bool:
        """Delete a message (ensures ownership)"""
        message = await self.get_message_by_user(message_id, user_id)
        if not message:
            return False

        return await self.delete(message_id)

    async def get_user_messages(
        self, user_id: str, limit: Optional[int] = None
    ) -> List[Message]:
        """Get all messages for a user across all sessions"""
        messages = await self.get_by_field("user_id", user_id)

        # Sort by created_at descending (most recent first)
        messages.sort(key=lambda x: x.created_at, reverse=True)

        if limit:
            messages = messages[:limit]

        return messages

    async def get_messages_by_role(
        self, session_id: str, user_id: str, role: MessageRole
    ) -> List[Message]:
        """Get messages by role for a specific session"""
        messages = await self.get_session_messages(session_id, user_id)
        return [msg for msg in messages if msg.role == role]

    async def get_conversation_thread(
        self, message_id: str, user_id: str
    ) -> List[Message]:
        """Get a conversation thread starting from a specific message"""
        message = await self.get_message_by_user(message_id, user_id)
        if not message:
            return []

        # Get all messages in the same session
        session_messages = await self.get_session_messages(message.session_id, user_id)

        # Find the thread (messages with the same parent or the message itself)
        thread_messages = []
        current_message = message

        # Go backwards to find the root of the thread
        while current_message:
            thread_messages.insert(0, current_message)
            if current_message.parent_message_id:
                current_message = next(
                    (
                        msg
                        for msg in session_messages
                        if msg.id == current_message.parent_message_id
                    ),
                    None,
                )
            else:
                break

        return thread_messages
