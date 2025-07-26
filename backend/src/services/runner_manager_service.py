import uuid
from typing import Any, Dict, Optional

from google.adk.artifacts.in_memory_artifact_service import (
    InMemoryArtifactService,
)
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from ..agents.root_agent import root_agent
from ..models.message import MessageRole, MessageType
from .artifact_service import ArtifactService
from .message_service import MessageService


class RunnerManagerService:
    """Service for managing agent runners and sessions"""

    def __init__(self):
        # Create database session service
        self.app_name = "MoneyTalk"
        self.session_service = DatabaseSessionService(
            db_url="sqlite://agent_sessions.db"
        )
        self.artifact_service = InMemoryArtifactService()
        self.message_service = MessageService()
        self.artifact_service_backend = ArtifactService()

        # Singleton runner instance
        self._runner: Optional[Runner] = None

    @property
    def runner(self) -> Runner:
        """Get or create the singleton runner instance"""
        if self._runner is None:

            # Create singleton runner
            self._runner = Runner(
                app_name="MoneyTalk",
                agent=root_agent,
                session_service=self.session_service,
            )

        return self._runner

    async def process_user_message(
        self,
        user_id: str,
        session_id: Optional[str],
        message_content: str,
        backend_session_id: str,
    ) -> Dict[str, Any]:
        """Process a user message through the agent system"""
        try:
            # Generate session_id if None
            if session_id is None:
                session_id = str(uuid.uuid4())

            # Check if session exists
            existing_sessions = self.session_service.list_sessions(
                app_name=self.app_name, user_id=user_id
            )

            existing_session_ids = [session.id for session in existing_sessions]

            if session_id not in existing_session_ids:
                # Create a new session
                await self.session_service.create_session(
                    app_name=self.app_name,
                    user_id=user_id,
                    session_id=session_id,
                )

            # Create content for the agent
            content = types.Content(
                role="user", parts=[types.Part(text=message_content)]
            )

            # Save user message to backend
            user_message = await self.message_service.create_message(
                session_id=backend_session_id,
                user_id=user_id,
                role=MessageRole.USER,
                content=message_content,
                message_type=MessageType.TEXT,
            )

            # Process with agent
            print(f"Processing message for user {user_id} in session {session_id}")
            response = self.runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content,
            )

            # Extract agent response
            agent_response = ""
            async for event in response:
                print(f"Event received: {event}")
                # Extract text content from agent response
                if hasattr(event, "content") and event.content:
                    for part in event.content.parts or []:
                        if hasattr(part, "text") and part.text:
                            agent_response += part.text

            # Save agent response to backend
            assistant_message = await self.message_service.create_message(
                session_id=backend_session_id,
                user_id=user_id,
                role=MessageRole.ASSISTANT,
                content=agent_response,
                message_type=MessageType.TEXT,
                metadata={
                    "adk_session_id": session_id,
                    "processing_complete": True,
                },
            )

            return {
                "success": True,
                "user_message_id": user_message["id"],
                "assistant_message_id": assistant_message["id"],
                "response": agent_response,
                "adk_session_id": session_id,
            }

        except Exception as e:
            print(f"Error processing message: {e}")
            # Save error message
            error_message = await self.message_service.create_message(
                session_id=backend_session_id,
                user_id=user_id,
                role=MessageRole.ASSISTANT,
                content=f"Sorry, I encountered an error: {str(e)}",
                message_type=MessageType.ERROR,
                metadata={"error": True, "error_details": str(e)},
            )

            return {
                "success": False,
                "error": str(e),
                "error_message_id": error_message["id"],
            }

    async def health_check(self) -> Dict[str, Any]:
        """Check the health of the runner manager"""
        try:
            return {
                "status": "healthy",
                "runner_initialized": self._runner is not None,
                "session_service": "DatabaseSessionService",
                "artifact_service": "InMemoryArtifactService",
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
