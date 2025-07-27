"""
Service dependencies for FastAPI dependency injection
"""

from functools import cache
from typing import Annotated

from fastapi import Depends

from ..config.firebase_config import get_auth
from ..dependencies.repositories import (
    ArtifactRepositoryDep,
    ChatSessionRepositoryDep,
    MessageRepositoryDep,
    UserRepositoryDep,
)
from ..services.artifact_service import ArtifactService
from ..services.chat_session_service import ChatSessionService
from ..services.message_service import MessageService
from ..services.runner_manager_service import RunnerManagerService


@cache
def get_artifact_service(
    artifact_repo: ArtifactRepositoryDep,
    message_repo: MessageRepositoryDep,
    user_repo: UserRepositoryDep,
) -> ArtifactService:
    """Get ArtifactService instance with dependency injection"""
    return ArtifactService(artifact_repo, message_repo, user_repo)


@cache
def get_artifact_service_with_deps(
    artifact_repo: ArtifactRepositoryDep,
    message_repo: MessageRepositoryDep,
    user_repo: UserRepositoryDep,
) -> ArtifactService:
    """Get ArtifactService instance with all dependencies"""
    # Create a service that has access to all repositories it needs
    service = ArtifactService(artifact_repo, message_repo, user_repo)

    return service


@cache
def get_chat_session_service(
    chat_session_repo: ChatSessionRepositoryDep,
    message_repo: MessageRepositoryDep,
) -> ChatSessionService:
    """Get ChatSessionService instance with dependency injection"""
    return ChatSessionService(chat_session_repo, message_repo)


@cache
def get_chat_session_service_simple(
    chat_session_repo: ChatSessionRepositoryDep,
    message_repo: MessageRepositoryDep,
) -> ChatSessionService:
    """Get ChatSessionService instance with only chat session repository"""
    return ChatSessionService(chat_session_repo, message_repo)


@cache
def get_message_service(
    message_repo: MessageRepositoryDep,
) -> MessageService:
    """Get MessageService instance with dependency injection"""
    return MessageService(message_repo)


@cache
def get_runner_manager_service(
    message_service: MessageService = Depends(get_message_service),
) -> RunnerManagerService:
    """Get RunnerManagerService instance with dependency injection"""
    auth_client = get_auth()
    return RunnerManagerService(
        message_service,
        auth_client,
    )


ArtifactServiceDep = Annotated[ArtifactService, Depends(get_artifact_service)]
ArtifactServiceWithDepsDep = Annotated[
    ArtifactService, Depends(get_artifact_service_with_deps)
]
ChatSessionServiceDep = Annotated[
    ChatSessionService,
    Depends(
        get_chat_session_service,
    ),
]
MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]
RunnerManagerServiceDep = Annotated[
    RunnerManagerService, Depends(get_runner_manager_service)
]
