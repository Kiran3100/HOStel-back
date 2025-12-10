# app/services/users/__init__.py
"""
User-related services.

- UserService: core user CRUD and listing
- UserProfileService: profile/contact updates
- UserActivityService: writes to audit.user_activity
"""

from .user_service import UserService
from .user_profile_service import UserProfileService
from .user_activity_service import UserActivityService

__all__ = [
    "UserService",
    "UserProfileService",
    "UserActivityService",
]