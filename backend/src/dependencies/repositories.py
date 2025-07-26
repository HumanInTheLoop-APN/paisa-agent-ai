"""
Repository dependencies for FastAPI dependency injection
"""

from typing import Annotated

from fastapi import Depends

from ..config.firebase_config import get_firestore
from ..repositories.artifact_repository import ArtifactRepository
from ..repositories.chat_session_repository import ChatSessionRepository
from ..repositories.message_repository import MessageRepository
from ..repositories.user_repository import UserRepository


def get_artifact_repository() -> ArtifactRepository:
    """Get ArtifactRepository instance with dependency injection"""
    db = get_firestore()
    return ArtifactRepository(db=db)


def get_chat_session_repository() -> ChatSessionRepository:
    """Get ChatSessionRepository instance with dependency injection"""
    db = get_firestore()
    return ChatSessionRepository(db=db)


def get_message_repository() -> MessageRepository:
    """Get MessageRepository instance with dependency injection"""
    db = get_firestore()
    return MessageRepository(db=db)


def get_user_repository() -> UserRepository:
    """Get UserRepository instance with dependency injection"""
    db = get_firestore()
    return UserRepository(db=db)


ArtifactRepositoryDep = Annotated[
    ArtifactRepository,
    Depends(
        get_artifact_repository,
    ),
]
ChatSessionRepositoryDep = Annotated[
    ChatSessionRepository, Depends(get_chat_session_repository)
]
MessageRepositoryDep = Annotated[
    MessageRepository,
    Depends(
        get_message_repository,
    ),
]
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
