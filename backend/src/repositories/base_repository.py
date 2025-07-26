import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

import firebase_admin
from firebase_admin import firestore
from pydantic import BaseModel

# Constrain T to be a Pydantic BaseModel
T = TypeVar("T", bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    """Base repository class for Firebase Firestore operations"""

    def __init__(self, collection_name: str):
        # Initialize Firestore client
        if not firebase_admin._apps:
            firebase_admin.initialize_app()

        self.db = firestore.client()
        self.collection = self.db.collection(collection_name)
        self._item_type: Optional[Type[T]] = None  # Will be set by subclasses

    def _generate_id(self) -> str:
        """Generate a unique ID"""
        return str(uuid.uuid4())

    def _get_timestamp(self) -> datetime:
        """Get current timestamp"""
        return datetime.utcnow()

    @abstractmethod
    def _get_key(self, item: T) -> str:
        """Get the unique key for an item"""
        pass

    @abstractmethod
    def _validate_item(self, item: T) -> bool:
        """Validate an item before storage"""
        pass

    async def create(self, item: T) -> T:
        """Create a new item in Firestore"""
        if not self._validate_item(item):
            raise ValueError("Invalid item data")

        # Generate ID and timestamps if not present
        if not hasattr(item, "id") or not getattr(item, "id"):
            setattr(item, "id", self._generate_id())

        if not hasattr(item, "created_at") or not getattr(item, "created_at"):
            setattr(item, "created_at", self._get_timestamp())

        if not hasattr(item, "updated_at") or not getattr(item, "updated_at"):
            setattr(item, "updated_at", self._get_timestamp())

        # Convert to dict and store in Firestore
        item_data = item.model_dump() if hasattr(item, "model_dump") else item.dict()
        doc_ref = self.collection.document(item.id)
        doc_ref.set(item_data)

        return item

    async def get_by_id(self, item_id: str) -> Optional[T]:
        """Get item by ID from Firestore"""
        doc_ref = self.collection.document(item_id)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            return self._reconstruct_item(data)
        return None

    async def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[T]:
        """Get all items with optional filters from Firestore"""
        query = self.collection

        # Apply filters
        if filters:
            for field, value in filters.items():
                query = query.where(field, "==", value)

        docs = query.stream()
        items = []

        for doc in docs:
            data = doc.to_dict()
            items.append(self._reconstruct_item(data))

        return items

    async def update(self, item: T) -> Optional[T]:
        """Update an existing item in Firestore"""
        if not self._validate_item(item):
            raise ValueError("Invalid item data")

        # Update timestamp
        if hasattr(item, "updated_at"):
            setattr(item, "updated_at", self._get_timestamp())

        # Convert to dict and update in Firestore
        item_data = item.model_dump() if hasattr(item, "model_dump") else item.dict()
        doc_ref = self.collection.document(item.id)
        doc = doc_ref.get()

        if doc.exists:
            doc_ref.update(item_data)
            return item
        return None

    async def delete(self, item_id: str) -> bool:
        """Delete an item by ID from Firestore"""
        doc_ref = self.collection.document(item_id)
        doc = doc_ref.get()

        if doc.exists:
            doc_ref.delete()
            return True
        return False

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count items with optional filters"""
        items = await self.get_all(filters)
        return len(items)

    def _reconstruct_item(self, data: Dict[str, Any]) -> T:
        """Reconstruct an item from Firestore data"""
        if self._item_type is None:
            raise NotImplementedError("Subclasses must set _item_type")

        # Handle Firestore timestamp conversion
        for key, value in data.items():
            if hasattr(value, "timestamp"):
                # Convert Firestore timestamp to datetime
                data[key] = value.timestamp()

        return self._item_type(**data)

    async def get_by_field(self, field: str, value: Any) -> List[T]:
        """Get items by a specific field value"""
        query = self.collection.where(field, "==", value)
        docs = query.stream()

        items = []
        for doc in docs:
            data = doc.to_dict()
            items.append(self._reconstruct_item(data))

        return items

    async def get_by_fields(self, filters: Dict[str, Any]) -> List[T]:
        """Get items by multiple field values (AND condition)"""
        query = self.collection

        for field, value in filters.items():
            query = query.where(field, "==", value)

        docs = query.stream()
        items = []

        for doc in docs:
            data = doc.to_dict()
            items.append(self._reconstruct_item(data))

        return items

    async def get_paginated(
        self,
        limit: int = 10,
        offset: int = 0,
        order_by: Optional[str] = None,
        direction: str = "desc",
    ) -> List[T]:
        """Get paginated items with optional ordering"""
        query = self.collection

        if order_by:
            if direction.lower() == "desc":
                query = query.order_by(order_by, direction=firestore.Query.DESCENDING)
            else:
                query = query.order_by(order_by, direction=firestore.Query.ASCENDING)

        # Apply pagination
        if offset > 0:
            # Get the document at offset position
            offset_docs = query.limit(offset).stream()
            offset_docs = list(offset_docs)
            if offset_docs:
                last_doc = offset_docs[-1]
                query = query.start_after(last_doc)

        docs = query.limit(limit).stream()
        items = []

        for doc in docs:
            data = doc.to_dict()
            items.append(self._reconstruct_item(data))

        return items
