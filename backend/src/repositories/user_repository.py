from typing import Any, Dict, List, Optional

from ..models.user import User
from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for user operations"""

    def __init__(self, db=None):
        super().__init__("users", db=db)
        self._item_type = User

    def _get_key(self, item: User) -> str:
        """Get the unique key for a user"""
        return item.uid

    def _validate_item(self, item: User) -> bool:
        """Validate a user before storage"""
        return (
            hasattr(item, "uid")
            and item.uid is not None
            and hasattr(item, "profile")
            and item.profile is not None
            and hasattr(item, "consents")
            and item.consents is not None
        )

    def _reconstruct_item(self, data: Dict[str, Any]) -> User:
        """Reconstruct a User from stored data"""
        return User(**data)

    async def create_user(self, user: User) -> User:
        """Create a new user"""
        return await self.create(user)

    async def get_user(self, uid: str) -> Optional[User]:
        """Get user by UID"""
        return await self.get_by_id(uid)

    async def update_user(self, uid: str, updates: Dict[str, Any]) -> Optional[User]:
        """Update user with specific fields"""
        user = await self.get_user(uid)
        if not user:
            return None

        # Apply updates to the user object
        for field, value in updates.items():
            if field.startswith("profile."):
                # Update profile fields
                profile_field = field.split(".", 1)[1]
                if hasattr(user.profile, profile_field):
                    setattr(user.profile, profile_field, value)
            elif field.startswith("consents."):
                # Update consent fields
                consent_field = field.split(".", 1)[1]
                if hasattr(user.consents, consent_field):
                    setattr(user.consents, consent_field, value)
            else:
                # Update direct user fields
                if hasattr(user, field):
                    setattr(user, field, value)

        return await self.update(user)

    async def update_user_consents(
        self, uid: str, consent_updates: Dict[str, Any]
    ) -> Optional[User]:
        """Update user consent settings"""
        user = await self.get_user(uid)
        if not user:
            return None

        # Apply consent updates
        for field, value in consent_updates.items():
            if hasattr(user.consents, field):
                setattr(user.consents, field, value)

        return await self.update(user)

    async def update_user_profile(
        self, uid: str, profile_updates: Dict[str, Any]
    ) -> Optional[User]:
        """Update user profile information"""
        user = await self.get_user(uid)
        if not user:
            return None

        # Apply profile updates
        for field, value in profile_updates.items():
            if hasattr(user.profile, field):
                setattr(user.profile, field, value)

        return await self.update(user)

    async def delete_user(self, uid: str) -> bool:
        """Delete a user"""
        return await self.delete(uid)

    async def get_all_users(self, limit: Optional[int] = None) -> List[User]:
        """Get all users (for admin purposes)"""
        users = await self.get_all()

        if limit:
            users = users[:limit]

        return users

    async def get_users_by_consent(self, consent_field: str, value: bool) -> List[User]:
        """Get users by specific consent setting"""
        users = await self.get_all()
        filtered_users = []

        for user in users:
            if hasattr(user.consents, consent_field):
                if getattr(user.consents, consent_field) == value:
                    filtered_users.append(user)

        return filtered_users
