import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..models.artifact import (
    Artifact,
    ArtifactCreate,
    ArtifactSource,
    ArtifactStatus,
    ArtifactType,
    ArtifactUpdate,
)
from .base_repository import BaseRepository


class ArtifactRepository(BaseRepository[Artifact]):
    """Repository for artifact operations"""

    def __init__(self, db=None):
        super().__init__("artifacts", db=db)
        self._item_type = Artifact

    def _get_key(self, item: Artifact) -> str:
        """Get the unique key for an artifact"""
        return item.id

    def _validate_item(self, item: Artifact) -> bool:
        """Validate an artifact before storage"""
        return (
            hasattr(item, "session_id")
            and item.session_id is not None
            and hasattr(item, "user_id")
            and item.user_id is not None
            and hasattr(item, "title")
            and item.title is not None
            and hasattr(item, "id")
            and item.id is not None
            and hasattr(item, "source")
            and item.source is not None
        )

    def _reconstruct_item(self, data: Dict[str, Any]) -> Artifact:
        """Reconstruct an Artifact from stored data"""
        return Artifact(**data)

    async def create_artifact(self, artifact_data: ArtifactCreate) -> Artifact:
        """Create a new artifact"""
        artifact = Artifact(
            id=None,  # Will be set by base repository
            session_id=artifact_data.session_id,
            user_id=artifact_data.user_id,
            message_id=artifact_data.message_id,
            title=artifact_data.title,
            description=artifact_data.description,
            artifact_type=artifact_data.artifact_type,
            source=artifact_data.source,
            metadata=artifact_data.metadata,
            consent_required=artifact_data.consent_required,
            consent_granted=artifact_data.consent_granted,
            created_at=None,  # Will be set by base repository
            updated_at=None,  # Will be set by base repository
            status=ArtifactStatus.PENDING,
            content=None,
            file_path=None,
            file_size=None,
            mime_type=None,
            original_filename=None,
            storage_uri=None,
            retention_expires_at=None,
        )
        return await self.create(artifact)

    async def get_session_artifacts(
        self, session_id: str, user_id: str
    ) -> List[Artifact]:
        """Get all artifacts for a specific session (ensures ownership)"""
        # First verify session ownership
        from .chat_session_repository import ChatSessionRepository

        session_repo = ChatSessionRepository()
        session = await session_repo.get_session_by_user(session_id, user_id)
        if not session:
            return []

        artifacts = await self.get_by_field("session_id", session_id)
        return artifacts

    async def get_artifact_by_user(
        self, artifact_id: str, user_id: str
    ) -> Optional[Artifact]:
        """Get a specific artifact for a user (ensures ownership)"""
        artifact = await self.get_by_id(artifact_id)
        if artifact and artifact.user_id == user_id:
            return artifact
        return None

    async def update_artifact(
        self, artifact_id: str, user_id: str, update_data: ArtifactUpdate
    ) -> Optional[Artifact]:
        """Update an artifact (ensures ownership)"""
        artifact = await self.get_artifact_by_user(artifact_id, user_id)
        if not artifact:
            return None

        # Apply updates
        if update_data.title is not None:
            artifact.title = update_data.title
        if update_data.description is not None:
            artifact.description = update_data.description
        if update_data.status is not None:
            artifact.status = update_data.status
        if update_data.content is not None:
            artifact.content = update_data.content
        if update_data.metadata is not None:
            artifact.metadata = update_data.metadata
        if update_data.consent_granted is not None:
            artifact.consent_granted = update_data.consent_granted

        return await self.update(artifact)

    async def delete_artifact(self, artifact_id: str, user_id: str) -> bool:
        """Delete an artifact (ensures ownership)"""
        artifact = await self.get_artifact_by_user(artifact_id, user_id)
        if not artifact:
            return False

        return await self.delete(artifact_id)

    async def get_message_artifacts(
        self, message_id: str, user_id: str
    ) -> List[Artifact]:
        """Get all artifacts for a specific message (ensures ownership)"""
        # First verify message ownership
        from .message_repository import MessageRepository

        message_repo = MessageRepository()
        message = await message_repo.get_message_by_user(message_id, user_id)
        if not message:
            return []

        artifacts = await self.get_by_field("message_id", message_id)
        return artifacts

    async def get_artifacts_by_type(
        self, session_id: str, user_id: str, artifact_type: ArtifactType
    ) -> List[Artifact]:
        """Get artifacts by type for a specific session"""
        artifacts = await self.get_session_artifacts(session_id, user_id)
        return [
            artifact
            for artifact in artifacts
            if artifact.artifact_type == artifact_type
        ]

    async def get_artifacts_by_status(
        self, session_id: str, user_id: str, status: ArtifactStatus
    ) -> List[Artifact]:
        """Get artifacts by status for a specific session"""
        artifacts = await self.get_session_artifacts(session_id, user_id)
        return [artifact for artifact in artifacts if artifact.status == status]

    async def get_artifacts_by_source(
        self, session_id: str, user_id: str, source: ArtifactSource
    ) -> List[Artifact]:
        """Get artifacts by source for a specific session"""
        artifacts = await self.get_session_artifacts(session_id, user_id)
        return [artifact for artifact in artifacts if artifact.source == source]

    async def update_artifact_status(
        self, artifact_id: str, user_id: str, status: ArtifactStatus
    ) -> bool:
        """Update artifact status"""
        artifact = await self.get_artifact_by_user(artifact_id, user_id)
        if not artifact:
            return False

        artifact.status = status
        await self.update(artifact)
        return True

    async def get_user_artifacts(
        self, user_id: str, limit: Optional[int] = None
    ) -> List[Artifact]:
        """Get all artifacts for a user across all sessions"""
        artifacts = await self.get_by_field("user_id", user_id)

        # Sort by created_at descending (most recent first)
        artifacts.sort(key=lambda x: x.created_at, reverse=True)

        if limit:
            artifacts = artifacts[:limit]

        return artifacts

    async def delete_expired_artifacts(self) -> int:
        """Delete artifacts that have exceeded their retention period"""
        all_artifacts = await self.get_all()
        deleted_count = 0

        for artifact in all_artifacts:
            if (
                artifact.retention_expires_at
                and artifact.retention_expires_at < datetime.now()
            ):
                success = await self.delete(artifact.id)
                if success:
                    deleted_count += 1

                    # Also delete the file if it exists
                    if artifact.file_path and os.path.exists(artifact.file_path):
                        try:
                            os.remove(artifact.file_path)
                        except OSError:
                            pass  # File might already be deleted

        return deleted_count
