import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..models import Message, MessageCreate, MessageEvent, MessageRole
from ..repositories.message_repository import MessageRepository


class MessageService:
    """Service class for message business logic"""

    def __init__(self, message_repository: MessageRepository):
        self.message_repo = message_repository

    async def create_message(
        self,
        session_id: str,
        user_id: str,
        role: str,
        human_content: Optional[str] = None,
        events: Optional[List[MessageEvent]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """Create a new message with business logic validation"""
        # Validate inputs
        if not session_id or not user_id or not role:
            raise ValueError("Session ID, User ID, and Role are required")

        # Validate role
        valid_roles = ["user", "assistant", "system"]
        if role not in valid_roles:
            raise ValueError(f"Role must be one of: {valid_roles}")

        # Validate content based on role
        if role == "user" and not human_content:
            raise ValueError("Human content is required for user messages")

        if role == "assistant" and not events:
            raise ValueError("Events are required for assistant messages")

        # Create message
        message = await self.message_repo.create_message(
            MessageCreate(
                session_id=session_id,
                user_id=user_id,
                role=MessageRole(role),
                human_content=human_content,
                events=events,
                metadata=metadata,
            )
        )

        # Return created message
        result = await self.message_repo.get_by_id(message.id)
        if not result:
            raise ValueError("Failed to retrieve created message")
        return result

    async def create_user_message(
        self,
        session_id: str,
        user_id: str,
        human_content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """Create a user message"""
        return await self.create_message(
            session_id=session_id,
            user_id=user_id,
            role="user",
            human_content=human_content,
            metadata=metadata,
        )

    async def create_assistant_message(
        self,
        session_id: str,
        user_id: str,
        events: List[MessageEvent],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Message:
        """Create an assistant message with events"""
        return await self.create_message(
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            events=events,
            metadata=metadata,
        )

    async def get_session_messages(
        self, session_id: str, user_id: str, limit: Optional[int] = None
    ) -> List[Message]:
        """Get messages for a session with access control"""
        if not session_id or not user_id:
            raise ValueError("Session ID and User ID are required")

        messages = await self.message_repo.get_session_messages(
            session_id, user_id, limit
        )

        # Filter messages by user access (in a real app, you'd check session ownership)
        # For now, we'll return all messages for the session
        return messages

    async def get_message(self, message_id: str, user_id: str) -> Optional[Message]:
        """Get a specific message with access control"""
        if not message_id or not user_id:
            raise ValueError("Message ID and User ID are required")

        message = await self.message_repo.get_by_id(message_id)

        # Check access control (in a real app, you'd check session ownership)
        if message and message.user_id != user_id:
            raise PermissionError("Access denied to this message")

        return message

    async def update_message(
        self,
        message_id: str,
        user_id: str,
        human_content: Optional[str] = None,
        events: Optional[List[MessageEvent]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[Message]:
        """Update a message"""
        # Verify access
        message = await self.get_message(message_id, user_id)
        if not message:
            return None

        # Update the message
        updated_message = await self.message_repo.update_message(
            message_id=message_id,
            human_content=human_content,
            events=events,
            metadata=metadata,
        )

        return updated_message

    async def add_event_to_message(
        self, message_id: str, user_id: str, event: MessageEvent
    ) -> bool:
        """Add an event to an assistant message"""
        # Verify access
        message = await self.get_message(message_id, user_id)
        if not message:
            return False

        if message.role != MessageRole.ASSISTANT:
            raise ValueError("Can only add events to assistant messages")

        # Get current events and add new one
        current_events = message.events.copy()
        current_events.append(event)

        # Update the message
        updated = await self.message_repo.update_message(
            message_id=message_id,
            events=current_events,
        )

        return updated is not None

    async def get_conversation_context(
        self, session_id: str, user_id: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent messages for conversation context"""
        messages = await self.get_session_messages(session_id, user_id, limit)

        # Format for conversation context
        context = []
        for message in messages:
            if message.role == MessageRole.USER:
                context.append(
                    {
                        "role": message.role,
                        "content": message.human_content or "",
                        "timestamp": message.created_at,
                    }
                )
            elif message.role == MessageRole.ASSISTANT:
                # Concatenate text content from events
                text_content = ""
                for event in message.events:
                    if event.content:
                        text_content += event.content + " "

                context.append(
                    {
                        "role": message.role,
                        "content": text_content.strip(),
                        "timestamp": message.created_at,
                    }
                )

        return context

    async def get_session_message_count(self, session_id: str, user_id: str) -> int:
        """Get the number of messages in a session"""
        messages = await self.message_repo.get_session_messages(session_id, user_id)
        return len(messages)

    async def delete_message(self, message_id: str, user_id: str) -> bool:
        """Delete a specific message"""
        # Verify access
        message = await self.get_message(message_id, user_id)
        if not message:
            return False

        return await self.message_repo.delete_message(message_id)

    async def delete_session_messages(self, session_id: str, user_id: str) -> bool:
        """Delete all messages for a session (for cleanup)"""
        # Verify access (in a real app, you'd check session ownership)
        if not session_id or not user_id:
            return False

        return await self.message_repo.delete_session_messages(session_id, user_id)
