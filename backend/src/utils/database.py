from datetime import datetime
from typing import Any, Dict, List, Optional

import firebase_admin
from firebase_admin import firestore

from ..models import (
    Artifact,
    ChatSession,
    DataAccessLog,
    Message,
    Schedule,
    User,
)


class FirestoreDB:
    def __init__(self):
        self.db = firestore.client()

    # User operations
    async def create_user(self, user: User) -> bool:
        """Create a new user in Firestore"""
        try:
            doc_ref = self.db.collection("users").document(user.uid)
            doc_ref.set(user.dict())
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    async def get_user(self, uid: str) -> Optional[User]:
        """Get user by UID"""
        try:
            doc_ref = self.db.collection("users").document(uid)
            doc = doc_ref.get()
            if doc.exists:
                return User(**doc.to_dict())
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    async def update_user(self, uid: str, updates: Dict[str, Any]) -> bool:
        """Update user in Firestore"""
        try:
            doc_ref = self.db.collection("users").document(uid)
            doc_ref.update(updates)
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    # Chat session operations
    async def create_chat_session(self, session: ChatSession) -> bool:
        """Create a new chat session"""
        try:
            doc_ref = self.db.collection("chat_sessions").document(session.id)
            doc_ref.set(session.dict())
            return True
        except Exception as e:
            print(f"Error creating chat session: {e}")
            return False

    async def get_user_chat_sessions(self, user_id: str) -> List[ChatSession]:
        """Get all chat sessions for a user"""
        try:
            docs = (
                self.db.collection("chat_sessions")
                .where("user_id", "==", user_id)
                .stream()
            )
            return [ChatSession(**doc.to_dict()) for doc in docs]
        except Exception as e:
            print(f"Error getting chat sessions: {e}")
            return []

    # Message operations
    async def create_message(self, message: Message) -> bool:
        """Create a new message"""
        try:
            doc_ref = self.db.collection("messages").document(message.id)
            doc_ref.set(message.dict())
            return True
        except Exception as e:
            print(f"Error creating message: {e}")
            return False

    async def get_session_messages(self, session_id: str) -> List[Message]:
        """Get all messages for a chat session"""
        try:
            docs = (
                self.db.collection("messages")
                .where("session_id", "==", session_id)
                .order_by("created_at")
                .stream()
            )
            return [Message(**doc.to_dict()) for doc in docs]
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []

    # Artifact operations
    async def create_artifact(self, artifact: Artifact) -> bool:
        """Create a new artifact"""
        try:
            doc_ref = self.db.collection("artifacts").document(artifact.id)
            doc_ref.set(artifact.dict())
            return True
        except Exception as e:
            print(f"Error creating artifact: {e}")
            return False

    async def get_user_artifacts(self, user_id: str) -> List[Artifact]:
        """Get all artifacts for a user"""
        try:
            docs = (
                self.db.collection("artifacts").where("user_id", "==", user_id).stream()
            )
            return [Artifact(**doc.to_dict()) for doc in docs]
        except Exception as e:
            print(f"Error getting artifacts: {e}")
            return []

    # Schedule operations
    async def create_schedule(self, schedule: Schedule) -> bool:
        """Create a new schedule"""
        try:
            doc_ref = self.db.collection("schedules").document(schedule.id)
            doc_ref.set(schedule.dict())
            return True
        except Exception as e:
            print(f"Error creating schedule: {e}")
            return False

    async def get_user_schedules(self, user_id: str) -> List[Schedule]:
        """Get all schedules for a user"""
        try:
            docs = (
                self.db.collection("schedules").where("user_id", "==", user_id).stream()
            )
            return [Schedule(**doc.to_dict()) for doc in docs]
        except Exception as e:
            print(f"Error getting schedules: {e}")
            return []

    # Data access log operations
    async def log_data_access(self, log_entry: DataAccessLog) -> bool:
        """Log data access for audit trail"""
        try:
            doc_ref = self.db.collection("data_access_logs").document(log_entry.id)
            doc_ref.set(log_entry.dict())
            return True
        except Exception as e:
            print(f"Error logging data access: {e}")
            return False

    async def get_user_access_logs(
        self, user_id: str, limit: int = 100
    ) -> List[DataAccessLog]:
        """Get access logs for a user"""
        try:
            docs = (
                self.db.collection("data_access_logs")
                .where("user_id", "==", user_id)
                .order_by("timestamp", direction=firestore.Query.DESCENDING)
                .limit(limit)
                .stream()
            )
            return [DataAccessLog(**doc.to_dict()) for doc in docs]
        except Exception as e:
            print(f"Error getting access logs: {e}")
            return []


# Global database instance
db = FirestoreDB()
