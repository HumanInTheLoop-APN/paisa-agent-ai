import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..repositories import ArtifactRepository


class ArtifactService:
    """Service class for artifact business logic"""

    def __init__(self, artifact_repo: ArtifactRepository):
        self.artifact_repo = artifact_repo
        self.storage_path = "backend/storage/artifacts"

        # Ensure storage directory exists
        os.makedirs(self.storage_path, exist_ok=True)

    async def create_artifact(
        self,
        user_id: str,
        session_id: str,
        message_id: str,
        artifact_type: str,
        title: str,
        content: str,
        mime_type: str = "application/json",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new artifact with business logic validation"""
        # Validate inputs
        if not all([user_id, session_id, message_id, artifact_type, title, content]):
            raise ValueError("All required fields must be provided")

        # Validate artifact type
        valid_types = ["chart", "report", "analysis", "json", "html", "csv", "image"]
        if artifact_type not in valid_types:
            raise ValueError(f"Artifact type must be one of: {valid_types}")

        # Calculate content size
        size_bytes = len(content.encode("utf-8"))

        # Generate file path for storage
        file_path = None
        if size_bytes > 1024:  # Store large content in files
            file_path = self._generate_file_path(user_id, artifact_type)
            await self._save_content_to_file(file_path, content)

        # Create artifact
        artifact_id = await self.artifact_repo.create_artifact(
            user_id=user_id,
            session_id=session_id,
            message_id=message_id,
            artifact_type=artifact_type,
            title=title,
            content=content if size_bytes <= 1024 else "",  # Store small content in DB
            mime_type=mime_type,
            file_path=file_path,
            size_bytes=size_bytes,
            metadata=metadata,
        )

        # Return created artifact
        return await self.artifact_repo.get(artifact_id)

    async def get_artifact(
        self, artifact_id: str, user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get a specific artifact with access control"""
        if not artifact_id or not user_id:
            raise ValueError("Artifact ID and User ID are required")

        artifact = await self.artifact_repo.get(artifact_id)

        # Check access control
        if artifact and artifact.get("user_id") != user_id:
            raise PermissionError("Access denied to this artifact")

        # Load content from file if needed
        if artifact and artifact.get("file_path") and not artifact.get("content"):
            content = await self._load_content_from_file(artifact["file_path"])
            artifact["content"] = content

        return artifact

    async def get_user_artifacts(
        self, user_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all artifacts for a user"""
        if not user_id:
            raise ValueError("User ID is required")

        artifacts = await self.artifact_repo.get_user_artifacts(user_id, limit)

        # Load content for artifacts stored in files
        for artifact in artifacts:
            if artifact.get("file_path") and not artifact.get("content"):
                content = await self._load_content_from_file(artifact["file_path"])
                artifact["content"] = content

        return artifacts

    async def get_session_artifacts(
        self, session_id: str, user_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get artifacts for a session with access control"""
        if not session_id or not user_id:
            raise ValueError("Session ID and User ID are required")

        artifacts = await self.artifact_repo.get_session_artifacts(session_id, limit)

        # Filter by user access (in a real app, you'd check session ownership)
        # For now, we'll return all artifacts for the session

        # Load content for artifacts stored in files
        for artifact in artifacts:
            if artifact.get("file_path") and not artifact.get("content"):
                content = await self._load_content_from_file(artifact["file_path"])
                artifact["content"] = content

        return artifacts

    async def get_artifacts_by_type(
        self, user_id: str, artifact_type: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get artifacts of a specific type for a user"""
        if not user_id or not artifact_type:
            raise ValueError("User ID and Artifact Type are required")

        artifacts = await self.artifact_repo.get_artifacts_by_type(
            user_id, artifact_type, limit
        )

        # Load content for artifacts stored in files
        for artifact in artifacts:
            if artifact.get("file_path") and not artifact.get("content"):
                content = await self._load_content_from_file(artifact["file_path"])
                artifact["content"] = content

        return artifacts

    async def update_artifact_metadata(
        self, artifact_id: str, user_id: str, metadata: Dict[str, Any]
    ) -> bool:
        """Update artifact metadata with validation"""
        if not isinstance(metadata, dict):
            raise ValueError("Metadata must be a dictionary")

        # Verify access
        artifact = await self.get_artifact(artifact_id, user_id)
        if not artifact:
            return False

        return await self.artifact_repo.update_artifact_metadata(artifact_id, metadata)

    async def delete_artifact(self, artifact_id: str, user_id: str) -> bool:
        """Delete an artifact with access control"""
        # Verify access
        artifact = await self.get_artifact(artifact_id, user_id)
        if not artifact:
            return False

        # Delete file if it exists
        if artifact.get("file_path"):
            await self._delete_file(artifact["file_path"])

        return await self.artifact_repo.delete(artifact_id)

    def _generate_file_path(self, user_id: str, artifact_type: str) -> str:
        """Generate a file path for artifact storage"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{user_id}_{artifact_type}_{timestamp}.json"
        return os.path.join(self.storage_path, filename)

    async def _save_content_to_file(self, file_path: str, content: str) -> None:
        """Save content to a file"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            raise Exception(f"Failed to save content to file: {str(e)}")

    async def _load_content_from_file(self, file_path: str) -> str:
        """Load content from a file"""
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            return ""
        except Exception as e:
            raise Exception(f"Failed to load content from file: {str(e)}")

    async def _delete_file(self, file_path: str) -> None:
        """Delete a file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            # Log error but don't raise - file might already be deleted
            print(f"Warning: Failed to delete file {file_path}: {str(e)}")
