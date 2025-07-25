from datetime import datetime
from typing import Any, Dict, List, Optional

from ..models import ChatSession, ChatSessionSettings
from ..repositories import ChatSessionRepository


class ChatSessionService:
    """Service class for chat session business logic"""

    def __init__(self, session_repo: ChatSessionRepository):
        self.session_repo = session_repo

    async def create_session(
        self, user_id: str, title: str = "", settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new chat session with business logic validation"""
        # Validate user_id
        if not user_id or not user_id.strip():
            raise ValueError("User ID is required")

        # Set default title if not provided
        if not title:
            title = f"Chat Session {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        # Validate and set default settings
        if settings is None:
            settings = ChatSessionSettings().dict()

        # Create session
        session_id = await self.session_repo.create_session(user_id, title, settings)

        # Return created session
        return await self.session_repo.get(session_id)

    async def get_user_sessions(
        self, user_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all sessions for a user with business logic"""
        if not user_id or not user_id.strip():
            raise ValueError("User ID is required")

        sessions = await self.session_repo.get_user_sessions(user_id, limit)

        # Add computed fields
        for session in sessions:
            session["message_count"] = 0  # TODO: Get from message service
            session["last_activity"] = session.get("updated_at")

        return sessions

    async def get_session(
        self, session_id: str, user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get a specific session with access control"""
        if not session_id or not user_id:
            raise ValueError("Session ID and User ID are required")

        session = await self.session_repo.get(session_id)

        # Check access control
        if session and session.get("user_id") != user_id:
            raise PermissionError("Access denied to this session")

        return session

    async def update_session_title(
        self, session_id: str, user_id: str, title: str
    ) -> bool:
        """Update session title with validation"""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        # Verify access
        session = await self.get_session(session_id, user_id)
        if not session:
            return False

        return await self.session_repo.update_session_title(session_id, title.strip())

    async def update_session_settings(
        self, session_id: str, user_id: str, settings: Dict[str, Any]
    ) -> bool:
        """Update session settings with validation"""
        # Validate settings
        if not isinstance(settings, dict):
            raise ValueError("Settings must be a dictionary")

        # Verify access
        session = await self.get_session(session_id, user_id)
        if not session:
            return False

        return await self.session_repo.update_session_settings(session_id, settings)

    async def deactivate_session(self, session_id: str, user_id: str) -> bool:
        """Deactivate a session with access control"""
        # Verify access
        session = await self.get_session(session_id, user_id)
        if not session:
            return False

        return await self.session_repo.deactivate_session(session_id)

    async def get_or_create_active_session(self, user_id: str) -> Dict[str, Any]:
        """Get the active session for a user or create a new one"""
        # Try to get existing active session
        active_session = await self.session_repo.get_active_session(user_id)

        if active_session:
            return active_session

        # Create new session if none exists
        return await self.create_session(user_id)

    async def add_session_metadata(
        self, session_id: str, user_id: str, metadata: Dict[str, Any]
    ) -> bool:
        """Add metadata to session with validation"""
        if not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary")

        # Verify access
        session = await self.get_session(session_id, user_id)
        if not session:
            return False

        return await self.session_repo.add_session_metadata(session_id, metadata)
