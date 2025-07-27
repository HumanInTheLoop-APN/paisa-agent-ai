import traceback
import uuid
from datetime import datetime
from typing import Any, AsyncGenerator, Dict, List, Optional

from google.adk.artifacts.in_memory_artifact_service import (
    InMemoryArtifactService,
)
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import (
    InMemorySessionService,
)
from google.genai import types

from ..agents.root_agent import root_agent
from ..models.artifact import ArtifactType
from ..models.message import MessageEvent, MessageRole, UsageMetadata
from ..services import MessageService


class RunnerManagerService:
    """Service for managing agent runners and sessions"""

    def __init__(
        self,
        message_service: MessageService,
        auth_client=None,
    ):
        # Create database session service
        self.app_name = "MoneyTalk"
        self.session_service = InMemorySessionService()
        self.artifact_service = InMemoryArtifactService()
        self.message_service = message_service
        self.auth_client = auth_client

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
    ):
        """Process a user message through the agent system"""
        try:
            # Generate session_id if None
            if session_id is None:
                session_id = str(uuid.uuid4())

            # Check if session exists
            existing_sessions = await self.session_service.list_sessions(
                app_name=self.app_name, user_id=user_id
            )
            print(f"Existing sessions: {existing_sessions}")

            existing_session_ids = [session[0] for session in existing_sessions]

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
            user_message = await self.message_service.create_user_message(
                session_id=backend_session_id,
                user_id=user_id,
                human_content=message_content,
            )

            # Process with agent
            print(f"Processing message for user {user_id} in session {session_id}")
            response = self.runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content,
            )

            # Collect events from agent response
            events: List[MessageEvent] = []
            event_sequence = 1
            all_tool_calls: List[Dict[str, Any]] = []
            all_tool_results: List[Dict[str, Any]] = []
            authors: List[str] = []
            has_errors = False
            error_summary: Dict[str, Any] = {}

            async for event in response:
                print(f"Event received: {event}")

                # Extract event data
                event_id = getattr(event, "id", str(uuid.uuid4()))
                author = getattr(event, "author", "unknown_agent")
                timestamp = datetime.now()

                # Add author to list if not already present
                if author not in authors:
                    authors.append(author)

                # Extract usage metadata
                usage_metadata = None
                if hasattr(event, "usage_metadata") and event.usage_metadata:
                    usage_metadata = UsageMetadata(
                        prompt_token_count=getattr(
                            event.usage_metadata, "prompt_token_count", None
                        ),
                        response_token_count=getattr(
                            event.usage_metadata, "candidates_token_count", None
                        ),
                        total_token_count=getattr(
                            event.usage_metadata, "total_token_count", None
                        ),
                        model_name=getattr(event.usage_metadata, "model_name", None),
                        invocation_id=getattr(event, "invocation_id", None),
                        processing_time=None,  # Will be calculated later
                        cost_estimate=None,  # Will be calculated later
                    )

                # Extract content and tool data
                event_content = ""
                event_tool_calls: List[Dict[str, Any]] = []
                event_tool_results: List[Dict[str, Any]] = []

                if hasattr(event, "content") and event.content:
                    for part in event.content.parts or []:
                        if hasattr(part, "text") and part.text:
                            event_content += part.text

                        if hasattr(part, "function_call") and part.function_call:
                            print(f"Function call received: {part.function_call}")
                            tool_call = {
                                "name": part.function_call.name,
                                "args": part.function_call.args,
                                "id": getattr(part.function_call, "id", None),
                            }
                            event_tool_calls.append(tool_call)
                            all_tool_calls.append(tool_call)

                        if (
                            hasattr(part, "function_response")
                            and part.function_response
                        ):
                            print(
                                f"Function response received: {part.function_response}"
                            )
                            tool_result = {
                                "name": part.function_response.name,
                                "response": part.function_response.response,
                                "id": getattr(part.function_response, "id", None),
                            }
                            event_tool_results.append(tool_result)
                            all_tool_results.append(tool_result)

                # Check for errors
                if hasattr(event, "error_code") and event.error_code:
                    has_errors = True
                    error_summary[event_id] = {
                        "error_code": event.error_code,
                        "error_message": getattr(event, "error_message", None),
                    }

                # Create MessageEvent
                message_event = MessageEvent(
                    event_id=event_id,
                    timestamp=timestamp,
                    sequence_number=event_sequence,
                    author=author,
                    content=event_content if event_content else None,
                    tool_calls=event_tool_calls if event_tool_calls else None,
                    tool_results=event_tool_results if event_tool_results else None,
                    metadata={
                        "adk_session_id": session_id,
                        "invocation_id": getattr(event, "invocation_id", None),
                        "turn_complete": getattr(event, "turn_complete", None),
                        "partial": getattr(event, "partial", None),
                        "interrupted": getattr(event, "interrupted", None),
                    },
                    usage_metadata=usage_metadata,
                    error_code=getattr(event, "error_code", None),
                    error_message=getattr(event, "error_message", None),
                    interrupted=getattr(event, "interrupted", None),
                    custom_metadata={
                        "grounding_metadata": getattr(
                            event, "grounding_metadata", None
                        ),
                        "actions": getattr(event, "actions", None),
                        "long_running_tool_ids": getattr(
                            event, "long_running_tool_ids", None
                        ),
                        "branch": getattr(event, "branch", None),
                    },
                    actions=getattr(event, "actions", None),
                    long_running_tool_ids=getattr(event, "long_running_tool_ids", None),
                    branch=getattr(event, "branch", None),
                    id=getattr(event, "id", None),
                )
                yield message_event.model_dump_json()
                events.append(message_event)
                event_sequence += 1

            # Save assistant message to backend
            await self.message_service.create_assistant_message(
                session_id=backend_session_id,
                user_id=user_id,
                events=events,
                metadata={
                    "adk_session_id": session_id,
                    "processing_complete": True,
                    "authors": authors,
                    "has_errors": has_errors,
                    "error_summary": error_summary if has_errors else None,
                },
            )
            yield '{"done": "true"}'
            print("Done")

        except Exception as e:
            print(f"Error processing message: {e}")
            traceback.print_exc()

            raise e

    def _map_adk_artifact_type(self, adk_type: str) -> ArtifactType:
        """Map ADK artifact types to our artifact types"""
        type_mapping = {
            "chart": ArtifactType.CHART,
            "report": ArtifactType.REPORT,
            "analysis": ArtifactType.ANALYSIS,
            "visualization": ArtifactType.VISUALIZATION,
            "data_export": ArtifactType.DATA_EXPORT,
            "recommendation": ArtifactType.RECOMMENDATION,
        }
        return type_mapping.get(adk_type.lower(), ArtifactType.OTHER)

    async def health_check(self) -> Dict[str, Any]:
        """Check the health of the runner manager"""
        try:
            return {
                "status": "healthy",
                "runner_initialized": self._runner is not None,
                "session_service": "InMemorySessionService",
                "artifact_service": "InMemoryArtifactService",
                "backend_artifact_service": "ArtifactService",
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
