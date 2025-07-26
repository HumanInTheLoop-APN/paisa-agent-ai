from typing import Any, Dict, List, Optional

from ..models.artifact import (
    Artifact,
    ArtifactCreate,
    ArtifactStatus,
    ArtifactType,
    ArtifactUpdate,
)
from ..repositories import ArtifactRepository
from ..repositories.message_repository import MessageRepository


class ArtifactService:
    """Service for artifact operations"""

    def __init__(self):
        self.repository = ArtifactRepository()
        self.message_repository = MessageRepository()

    async def create_artifact(
        self,
        session_id: str,
        user_id: str,
        message_id: str,
        artifact_type: ArtifactType,
        title: str,
        description: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> Artifact:
        """Create a new artifact"""
        # Verify message ownership
        message = await self.message_repository.get_message_by_user(message_id, user_id)
        if not message:
            raise ValueError("Message not found or access denied")

        artifact_data = ArtifactCreate(
            session_id=session_id,
            user_id=user_id,
            message_id=message_id,
            artifact_type=artifact_type,
            title=title,
            description=description,
            metadata=metadata,
        )

        return await self.repository.create_artifact(artifact_data)

    async def get_session_artifacts(
        self, session_id: str, user_id: str
    ) -> List[Artifact]:
        """Get all artifacts for a specific session (ensures ownership)"""
        return await self.repository.get_session_artifacts(session_id, user_id)

    async def get_artifact(self, artifact_id: str, user_id: str) -> Artifact:
        """Get a specific artifact for a user (ensures ownership)"""
        artifact = await self.repository.get_artifact_by_user(artifact_id, user_id)
        if artifact is None:
            raise ValueError(f"Artifact {artifact_id} not found or access denied")
        return artifact

    async def update_artifact(
        self,
        artifact_id: str,
        user_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[ArtifactStatus] = None,
        content: Optional[Dict[str, Any]] = None,
        metadata: Optional[dict] = None,
    ) -> Optional[Artifact]:
        """Update an artifact (ensures ownership)"""
        update_data = ArtifactUpdate(
            title=title,
            description=description,
            status=status,
            content=content,
            metadata=metadata,
        )
        return await self.repository.update_artifact(artifact_id, user_id, update_data)

    async def delete_artifact(self, artifact_id: str, user_id: str) -> bool:
        """Delete an artifact (ensures ownership)"""
        return await self.repository.delete_artifact(artifact_id, user_id)

    async def get_message_artifacts(
        self, message_id: str, user_id: str
    ) -> List[Artifact]:
        """Get all artifacts for a specific message (ensures ownership)"""
        return await self.repository.get_message_artifacts(message_id, user_id)

    async def get_artifacts_by_type(
        self, session_id: str, user_id: str, artifact_type: ArtifactType
    ) -> List[Artifact]:
        """Get artifacts by type for a specific session"""
        return await self.repository.get_artifacts_by_type(
            session_id, user_id, artifact_type
        )

    async def get_artifacts_by_status(
        self, session_id: str, user_id: str, status: ArtifactStatus
    ) -> List[Artifact]:
        """Get artifacts by status for a specific session"""
        return await self.repository.get_artifacts_by_status(
            session_id, user_id, status
        )

    async def update_artifact_status(
        self, artifact_id: str, user_id: str, status: ArtifactStatus
    ) -> bool:
        """Update artifact status"""
        return await self.repository.update_artifact_status(
            artifact_id, user_id, status
        )

    async def get_user_artifacts(
        self, user_id: str, limit: Optional[int] = None
    ) -> List[Artifact]:
        """Get all artifacts for a user across all sessions"""
        return await self.repository.get_user_artifacts(user_id, limit)

    async def create_chart_artifact(
        self,
        session_id: str,
        user_id: str,
        message_id: str,
        title: str,
        chart_data: Dict[str, Any],
        description: Optional[str] = None,
    ) -> Artifact:
        """Create a chart artifact"""
        metadata = {
            "chart_type": chart_data.get("type", "unknown"),
            "chart_config": chart_data.get("config", {}),
        }

        artifact = await self.create_artifact(
            session_id=session_id,
            user_id=user_id,
            message_id=message_id,
            artifact_type=ArtifactType.CHART,
            title=title,
            description=description,
            metadata=metadata,
        )

        # Update with content and mark as completed
        await self.update_artifact(
            artifact_id=artifact.id,
            user_id=user_id,
            content=chart_data,
            status=ArtifactStatus.COMPLETED,
        )

        return await self.get_artifact(artifact.id, user_id)

    async def create_report_artifact(
        self,
        session_id: str,
        user_id: str,
        message_id: str,
        title: str,
        report_content: Dict[str, Any],
        description: Optional[str] = None,
    ) -> Artifact:
        """Create a report artifact"""
        artifact = await self.create_artifact(
            session_id=session_id,
            user_id=user_id,
            message_id=message_id,
            artifact_type=ArtifactType.REPORT,
            title=title,
            description=description,
        )

        # Update with content and mark as completed
        await self.update_artifact(
            artifact_id=artifact.id,
            user_id=user_id,
            content=report_content,
            status=ArtifactStatus.COMPLETED,
        )

        return await self.get_artifact(artifact.id, user_id)

    async def create_analysis_artifact(
        self,
        session_id: str,
        user_id: str,
        message_id: str,
        title: str,
        analysis_content: Dict[str, Any],
        description: Optional[str] = None,
    ) -> Artifact:
        """Create an analysis artifact"""
        artifact = await self.create_artifact(
            session_id=session_id,
            user_id=user_id,
            message_id=message_id,
            artifact_type=ArtifactType.ANALYSIS,
            title=title,
            description=description,
        )

        # Update with content and mark as completed
        await self.update_artifact(
            artifact_id=artifact.id,
            user_id=user_id,
            content=analysis_content,
            status=ArtifactStatus.COMPLETED,
        )

        return await self.get_artifact(artifact.id, user_id)
