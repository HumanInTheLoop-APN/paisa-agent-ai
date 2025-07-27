from typing import Any, Dict, List, Optional

from ..models.message import Message, MessageCreate, MessageRole, MessageUpdate
from .base_repository import BaseRepository


class MessageRepository(
    BaseRepository[
        Message,
        MessageCreate,
        MessageUpdate,
    ]
):
    """Repository for message operations"""

    def __init__(self, db=None):
        super().__init__("messages", db=db)

    def _get_key(self, item: Message) -> str:
        """Get the unique key for a message"""
        return item.id

    def _reconstruct_item(self, data: Dict[str, Any]) -> Message:
        """Reconstruct a Message from stored data"""
        return Message(**data)

    def _validate_update_item(self, item: MessageUpdate) -> bool:
        """Validate a message before storage"""
        return True  # MessageUpdate doesn't require id

    def _validate_create_item(self, item: MessageCreate) -> bool:
        """Validate a message before storage"""
        return (
            hasattr(item, "session_id")
            and item.session_id is not None
            and hasattr(item, "user_id")
            and item.user_id is not None
            and hasattr(item, "role")
            and item.role is not None
            and (
                (item.role == MessageRole.USER and item.human_content is not None)
                or (item.role == MessageRole.ASSISTANT and item.events is not None)
                or item.role == MessageRole.SYSTEM
            )
        )

    async def create_message(self, message_data: MessageCreate) -> Message:
        """Create a new message"""
        return await self.create(message_data)

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
        self,
        message_id: str,
        human_content: Optional[str] = None,
        events: Optional[List[Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[Message]:
        """Update a message"""
        message = await self.get_by_id(message_id)
        if not message:
            return None

        # Apply updates
        if human_content is not None:
            message.human_content = human_content
        if events is not None:
            message.events = events
        if metadata is not None:
            message.metadata = metadata

        return await self.update(message)

    async def delete_message(self, message_id: str) -> bool:
        """Delete a message"""
        message = await self.get_by_id(message_id)
        if not message:
            return False

        return await self.delete(message_id)

    async def delete_session_messages(self, session_id: str, user_id: str) -> bool:
        """Delete all messages for a session (ensures ownership)"""
        # First verify session ownership
        from .chat_session_repository import ChatSessionRepository

        session_repo = ChatSessionRepository()
        session = await session_repo.get_session_by_user(session_id, user_id)
        if not session:
            return False

        messages = await self.get_by_field("session_id", session_id)

        # Delete all messages in the session
        for message in messages:
            await self.delete(message.id)

        return True

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
        """Get messages for a session by role"""
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
        return await self.get_session_messages(message.session_id, user_id)

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
