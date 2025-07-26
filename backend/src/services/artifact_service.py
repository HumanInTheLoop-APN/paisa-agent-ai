import os
import uuid
from typing import Any, Dict, List, Optional

from ..models.artifact import (
    Artifact,
    ArtifactCreate,
    ArtifactSource,
    ArtifactStatus,
    ArtifactType,
    ArtifactUpdate,
)
from ..repositories.artifact_repository import ArtifactRepository
from ..repositories.message_repository import MessageRepository
from ..repositories.user_repository import UserRepository


class ArtifactService:
    """Service for artifact operations with consent management"""

    def __init__(
        self,
        artifact_repository: ArtifactRepository,
        message_repository: MessageRepository,
        user_repository: UserRepository,
    ):
        self.repository = artifact_repository
        self.message_repository = message_repository

    async def create_user_upload_artifact(
        self,
        session_id: str,
        user_id: str,
        message_id: str,
        file_data: bytes,
        filename: str,
        mime_type: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Artifact:
        """Create an artifact from user file upload"""
        # Determine artifact type from file extension
        artifact_type = self._get_artifact_type_from_filename(filename)

        # Generate unique filename
        file_extension = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # Save file to local storage (or cloud storage)
        file_path = await self._save_uploaded_file(file_data, unique_filename)

        artifact_data = ArtifactCreate(
            session_id=session_id,
            user_id=user_id,
            message_id=message_id,
            artifact_type=artifact_type,
            source=ArtifactSource.USER_UPLOAD,
            title=title or filename,
            description=description,
            metadata={
                "original_filename": filename,
                "file_size": len(file_data),
                "mime_type": mime_type,
            },
            consent_required=False,  # User uploads don't need consent
            consent_granted=True,  # User implicitly consents by uploading
        )

        artifact = await self.repository.create_artifact(artifact_data)

        # Update with file information
        await self.repository.update_artifact(
            artifact.id,
            user_id,
            ArtifactUpdate(
                file_path=file_path,
                file_size=len(file_data),
                mime_type=mime_type,
                original_filename=filename,
                status=ArtifactStatus.COMPLETED,
            ),
        )

        return await self.get_artifact(artifact.id, user_id)

    async def create_ai_generated_artifact(
        self,
        session_id: str,
        user_id: str,
        message_id: str,
        artifact_type: ArtifactType,
        title: str,
        content: Dict[str, Any],
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Artifact:
        """Create an AI-generated artifact with consent check"""
        # Check user consent for storing artifacts
        user = await self.user_repository.get_user(user_id)
        consent_required = not user.consents.store_artifacts

        artifact_data = ArtifactCreate(
            session_id=session_id,
            user_id=user_id,
            message_id=message_id,
            artifact_type=artifact_type,
            source=ArtifactSource.AI_GENERATED,
            title=title,
            description=description,
            metadata=metadata or {},
            consent_required=consent_required,
            consent_granted=not consent_required,  # Auto-grant if user has consent
        )

        artifact = await self.repository.create_artifact(artifact_data)

        if not consent_required:
            # User has consent, store the artifact
            await self.repository.update_artifact(
                artifact.id,
                user_id,
                ArtifactUpdate(
                    content=content,
                    status=ArtifactStatus.COMPLETED,
                ),
            )
        else:
            # Consent required, mark as pending consent
            await self.repository.update_artifact(
                artifact.id,
                user_id,
                ArtifactUpdate(
                    content=content,
                    status=ArtifactStatus.CONSENT_REQUIRED,
                ),
            )

        return await self.get_artifact(artifact.id, user_id)

    async def grant_consent_for_artifact(
        self, artifact_id: str, user_id: str
    ) -> Artifact:
        """Grant consent for an AI-generated artifact"""
        artifact = await self.get_artifact(artifact_id, user_id)

        if artifact.source != ArtifactSource.AI_GENERATED:
            raise ValueError("Consent can only be granted for AI-generated artifacts")

        if not artifact.consent_required:
            raise ValueError("This artifact does not require consent")

        # Update artifact with consent granted
        updated_artifact = await self.repository.update_artifact(
            artifact_id,
            user_id,
            ArtifactUpdate(
                consent_granted=True,
                status=ArtifactStatus.COMPLETED,
            ),
        )

        # Update user's global consent if this is the first time
        user = await self.user_repository.get_user(user_id)
        if not user.consents.store_artifacts:
            await self.user_repository.update_user_consents(
                user_id, {"store_artifacts": True}
            )

        return updated_artifact

    async def deny_consent_for_artifact(
        self, artifact_id: str, user_id: str
    ) -> Artifact:
        """Deny consent for an AI-generated artifact"""
        artifact = await self.get_artifact(artifact_id, user_id)

        if artifact.source != ArtifactSource.AI_GENERATED:
            raise ValueError("Consent can only be denied for AI-generated artifacts")

        if not artifact.consent_required:
            raise ValueError("This artifact does not require consent")

        # Mark as consent denied and delete content
        updated_artifact = await self.repository.update_artifact(
            artifact_id,
            user_id,
            ArtifactUpdate(
                consent_granted=False,
                status=ArtifactStatus.CONSENT_DENIED,
                content=None,  # Remove content when consent is denied
            ),
        )

        return updated_artifact

    async def get_artifacts_requiring_consent(
        self, session_id: str, user_id: str
    ) -> List[Artifact]:
        """Get all artifacts that require user consent"""
        return await self.repository.get_artifacts_by_status(
            session_id, user_id, ArtifactStatus.CONSENT_REQUIRED
        )

    async def get_artifacts_by_source(
        self, session_id: str, user_id: str, source: ArtifactSource
    ) -> List[Artifact]:
        """Get artifacts by source (user upload or AI generated)"""
        return await self.repository.get_artifacts_by_source(
            session_id, user_id, source
        )

    async def cleanup_expired_artifacts(self) -> int:
        """Clean up artifacts that have exceeded retention period"""
        return await self.repository.delete_expired_artifacts()

    def _get_artifact_type_from_filename(self, filename: str) -> ArtifactType:
        """Determine artifact type from filename extension"""
        ext = os.path.splitext(filename)[1].lower()

        type_mapping = {
            ".pdf": ArtifactType.PDF,
            ".csv": ArtifactType.CSV,
            ".jpg": ArtifactType.IMAGE,
            ".jpeg": ArtifactType.IMAGE,
            ".png": ArtifactType.IMAGE,
            ".gif": ArtifactType.IMAGE,
            ".doc": ArtifactType.DOCUMENT,
            ".docx": ArtifactType.DOCUMENT,
            ".txt": ArtifactType.DOCUMENT,
            ".xls": ArtifactType.SPREADSHEET,
            ".xlsx": ArtifactType.SPREADSHEET,
        }

        return type_mapping.get(ext, ArtifactType.OTHER)

    async def _save_uploaded_file(self, file_data: bytes, filename: str) -> str:
        """Save uploaded file to storage and return file path"""
        # For now, save to local storage
        # In production, this should save to cloud storage (GCS, S3, etc.)
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(file_data)

        return file_path

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
            source=ArtifactSource.AI_GENERATED,  # Default to AI generated for backward compatibility
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
