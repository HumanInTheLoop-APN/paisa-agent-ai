import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar

import firebase_admin
from firebase_admin import firestore

from ..models import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    """Base repository class for Firestore operations with common error handling"""

    def __init__(self, collection_name: str):
        self.db = firestore.client()
        self.collection_name = collection_name
        self.collection = self.db.collection(collection_name)

    def _generate_id(self) -> str:
        """Generate a unique ID for documents"""
        return str(uuid.uuid4())

    def _add_timestamps(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add created_at and updated_at timestamps to data"""
        now = datetime.now()
        data["created_at"] = now
        data["updated_at"] = now
        return data

    def _update_timestamp(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add updated_at timestamp to data"""
        data["updated_at"] = datetime.now()
        return data

    async def create(self, data: Dict[str, Any], doc_id: Optional[str] = None) -> str:
        """Create a new document in Firestore"""
        try:
            # Add timestamps
            data = self._add_timestamps(data)

            # Generate ID if not provided
            if not doc_id:
                doc_id = self._generate_id()

            # Add ID to data
            data["id"] = doc_id

            # Create document
            doc_ref = self.collection.document(doc_id)
            doc_ref.set(data)

            return doc_id
        except Exception as e:
            raise RepositoryError(
                f"Failed to create document in {self.collection_name}: {str(e)}"
            )

    async def get(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get a document by ID"""
        try:
            doc_ref = self.collection.document(doc_id)
            doc = doc_ref.get()

            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            raise RepositoryError(
                f"Failed to get document {doc_id} from {self.collection_name}: {str(e)}"
            )

    async def update(self, doc_id: str, data: Dict[str, Any]) -> bool:
        """Update a document by ID"""
        try:
            # Add updated timestamp
            data = self._update_timestamp(data)

            # Update document
            doc_ref = self.collection.document(doc_id)
            doc_ref.update(data)

            return True
        except Exception as e:
            raise RepositoryError(
                f"Failed to update document {doc_id} in {self.collection_name}: {str(e)}"
            )

    async def delete(self, doc_id: str) -> bool:
        """Delete a document by ID"""
        try:
            doc_ref = self.collection.document(doc_id)
            doc_ref.delete()
            return True
        except Exception as e:
            raise RepositoryError(
                f"Failed to delete document {doc_id} from {self.collection_name}: {str(e)}"
            )

    async def list(
        self,
        filters: Optional[List[tuple]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """List documents with optional filtering and ordering"""
        try:
            query = self.collection

            # Apply filters
            if filters:
                for field, operator, value in filters:
                    query = query.where(field, operator, value)

            # Apply ordering
            if order_by:
                query = query.order_by(order_by)

            # Apply limit
            if limit:
                query = query.limit(limit)

            # Execute query
            docs = query.stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            raise RepositoryError(
                f"Failed to list documents from {self.collection_name}: {str(e)}"
            )

    async def exists(self, doc_id: str) -> bool:
        """Check if a document exists"""
        try:
            doc_ref = self.collection.document(doc_id)
            doc = doc_ref.get()
            return doc.exists
        except Exception as e:
            raise RepositoryError(
                f"Failed to check existence of document {doc_id} in {self.collection_name}: {str(e)}"
            )


class RepositoryError(Exception):
    """Custom exception for repository operations"""

    pass
