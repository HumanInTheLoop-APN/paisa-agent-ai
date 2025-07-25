from datetime import datetime
from typing import Any, Dict, List, Optional

from ..models import Artifact
from .base_repository import BaseRepository


class ArtifactRepository(BaseRepository[Artifact]):
    """Repository for artifact operations"""

    def __init__(self):
        super().__init__("artifacts")

    async def create_artifact(
        self,
        user_id: str,
        session_id: str,
        message_id: str,
        artifact_type: str,
        title: str,
        content: str,
        mime_type: str,
        file_path: Optional[str] = None,
        size_bytes: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a new artifact"""
        artifact_data = {
            "user_id": user_id,
            "session_id": session_id,
            "message_id": message_id,
            "type": artifact_type,
            "title": title,
            "content": content,
            "file_path": file_path,
            "mime_type": mime_type,
            "size_bytes": size_bytes,
            "metadata": metadata or {},
        }
        return await self.create(artifact_data)

    async def get_user_artifacts(
        self, user_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all artifacts for a user"""
        filters = [("user_id", "==", user_id)]
        return await self.list(filters=filters, order_by="created_at", limit=limit)

    async def get_session_artifacts(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get all artifacts for a session"""
        filters = [("session_id", "==", session_id)]
        return await self.list(filters=filters, order_by="created_at", limit=limit)

    async def get_message_artifacts(self, message_id: str) -> List[Dict[str, Any]]:
        """Get all artifacts for a specific message"""
        filters = [("message_id", "==", message_id)]
        return await self.list(filters=filters, order_by="created_at")

    async def get_artifacts_by_type(
        self, user_id: str, artifact_type: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get artifacts of a specific type for a user"""
        filters = [("user_id", "==", user_id), ("type", "==", artifact_type)]
        return await self.list(filters=filters, order_by="created_at", limit=limit)

    async def update_artifact_metadata(
        self, artifact_id: str, metadata: Dict[str, Any]
    ) -> bool:
        """Update metadata for an artifact"""
        artifact = await self.get(artifact_id)
        if artifact:
            current_metadata = artifact.get("metadata", {})
            current_metadata.update(metadata)
            return await self.update(artifact_id, {"metadata": current_metadata})
        return False

    async def delete_session_artifacts(self, session_id: str) -> bool:
        """Delete all artifacts for a session (for cleanup)"""
        try:
            artifacts = await self.get_session_artifacts(session_id)
            for artifact in artifacts:
                await self.delete(artifact["id"])
            return True
        except Exception:
            return False

    async def get_recent_artifacts(
        self, user_id: str, days: int = 7
    ) -> List[Dict[str, Any]]:
        """Get artifacts created in the last N days"""
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days)
        filters = [("user_id", "==", user_id), ("created_at", ">=", cutoff_date)]
        return await self.list(filters=filters, order_by="created_at")
