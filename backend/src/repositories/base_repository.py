import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from firebase_admin import firestore
from google.cloud.firestore_v1.client import Client
from pydantic import BaseModel

# Constrain T to be a Pydantic BaseModel
T = TypeVar("T", bound=BaseModel)
CreateT = TypeVar("CreateT", bound=BaseModel)
UpdateT = TypeVar("UpdateT", bound=BaseModel)


class BaseRepository(ABC, Generic[T, CreateT, UpdateT]):
    """Base repository class for Firebase Firestore operations"""

    def __init__(
        self,
        collection_name: str,
        db: Optional[Client] = None,
    ):
        # Use provided Firestore client or get from Firebase config
        if db is None:
            from ..config.firebase_config import get_firestore

            self.db = get_firestore()
        else:
            self.db = db
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
    def _validate_create_item(self, item: CreateT) -> bool:
        """Validate an item before storage"""
        pass

    @abstractmethod
    def _validate_update_item(self, item: UpdateT) -> bool:
        """Validate an item before storage"""
        pass

    async def create(self, item: CreateT) -> T:
        """Create a new item in Firestore"""
        if not self._validate_create_item(item):
            raise ValueError("Invalid item data")

        create_item = item.model_dump()

        # Generate ID and timestamps if not present
        if not create_item.get("id"):
            print("Generating ID")
            create_item["id"] = self._generate_id()

        if not create_item.get("created_at"):
            print("Generating created_at")
            create_item["created_at"] = self._get_timestamp()

        if not create_item.get("updated_at"):
            print("Generating updated_at")
            create_item["updated_at"] = self._get_timestamp()

        # Convert to dict and store in Firestore
        print("Item data", create_item)
        doc_ref = self.collection.document(create_item["id"])
        doc_ref.set(create_item)

        return self._reconstruct_item(create_item)

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

    async def update(self, item: UpdateT) -> Optional[T]:
        """Update an existing item in Firestore"""
        if not self._validate_update_item(item):
            raise ValueError("Invalid item data")

        update_item = item.model_dump()
        # Update timestamp
        if not update_item.get("updated_at"):
            update_item["updated_at"] = self._get_timestamp()

        # Convert to dict and update in Firestore
        doc_ref = self.collection.document(update_item["id"])
        doc = doc_ref.get()

        if doc.exists:
            doc_ref.update(update_item)
            return self._reconstruct_item(update_item)
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
            print(f"Key: {key}, Value: {value}")
            if hasattr(value, "timestamp"):
                # Convert Firestore timestamp to datetime
                data[key] = value.timestamp()

        print(f"Data: {data}")
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
