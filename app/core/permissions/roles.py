"""
Role Management Utilities.

This module defines the hierarchy of roles and helper methods
to check user role types.
"""

from typing import Any, List
from app.core.enums import UserType


class RoleManager:
    """
    Manages user roles, hierarchy, and capability checking.
    """

    def get_role_hierarchy(self) -> List[UserType]:
        """
        Returns roles ordered by privilege (Highest -> Lowest).
        """
        return [
            UserType.SUPER_ADMIN,
            UserType.HOSTEL_ADMIN,
            UserType.SUPERVISOR,
            UserType.STUDENT,
            UserType.VISITOR
        ]

    def can_manage_role(self, actor_role: UserType, target_role: UserType) -> bool:
        """
        Determines if the actor can manage/edit the target user based on rank.
        
        Example: 
        - Super Admin can manage Hostel Admin (True).
        - Hostel Admin cannot manage Super Admin (False).
        """
        hierarchy = self.get_role_hierarchy()
        try:
            actor_index = hierarchy.index(actor_role)
            target_index = hierarchy.index(target_role)
            # Lower index in the list means higher privilege
            return actor_index < target_index
        except ValueError:
            return False

    # --- Role Check Helpers ---

    def is_super_admin(self, user: Any) -> bool:
        return user.user_type == UserType.SUPER_ADMIN

    def is_hostel_admin(self, user: Any) -> bool:
        return user.user_type == UserType.HOSTEL_ADMIN

    def is_supervisor(self, user: Any) -> bool:
        return user.user_type == UserType.SUPERVISOR

    def is_staff(self, user: Any) -> bool:
        """Checks if user is any staff role (Admin or Supervisor)."""
        return user.user_type in [UserType.SUPER_ADMIN, UserType.HOSTEL_ADMIN, UserType.SUPERVISOR]

    def is_student(self, user: Any) -> bool:
        return user.user_type == UserType.STUDENT

    def is_visitor(self, user: Any) -> bool:
        return user.user_type == UserType.VISITOR


# Global instance
role_manager = RoleManager()