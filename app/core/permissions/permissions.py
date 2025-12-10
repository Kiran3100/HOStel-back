"""
Permission Checker Logic.

This module evaluates whether a specific user request matches 
the allowed permissions defined in the matrix.
"""

from typing import Any, Set
from app.core.permissions.permission_matrix import PermissionMatrix
from app.core.enums import UserType


class PermissionChecker:
    """
    Evaluates permissions by checking static role definitions
    and dynamic user-specific overrides.
    """
    
    def check_permission(self, user: Any, required_permission: str) -> bool:
        """
        Primary entry point to check if a user has a specific permission.
        
        Args:
            user: The user object (must have .user_type)
            required_permission: The permission string (e.g., "hostel:create")
            
        Returns:
            True if allowed, False otherwise.
        """
        if not user or not getattr(user, "is_active", False):
            return False

        # 1. Super Admin Bypass
        if user.user_type == UserType.SUPER_ADMIN:
            return True

        # 2. Get Base Role Permissions
        permissions = PermissionMatrix.get_permissions_for_role(user.user_type)

        # 3. Add Custom/Dynamic Permissions (if user has them stored in DB)
        if hasattr(user, "custom_permissions") and user.custom_permissions:
            permissions.update(user.custom_permissions)

        # 4. Check logic
        resource, action = required_permission.split(":")
        return self._evaluate_permission_set(permissions, resource, action)

    def _evaluate_permission_set(self, permissions: Set[str], resource: str, action: str) -> bool:
        """
        Matches requested resource:action against the permission set 
        handling wildcards.
        """
        # Exact match (e.g., "room:create")
        if f"{resource}:{action}" in permissions:
            return True
        
        # Resource wildcard (e.g., "room:*")
        if f"{resource}:*" in permissions:
            return True
            
        # Manage wildcard (e.g., "room:manage") - specific semantic alias for *
        if f"{resource}:manage" in permissions:
            return True
            
        # Global wildcard (e.g., "*:*")
        if "*:*" in permissions:
            return True
            
        return False

    def validate_action(self, user: Any, resource: str, action: str) -> bool:
        """Helper wrapper for clean syntax."""
        return self.check_permission(user, f"{resource}:{action}")


# Global instance
permission_checker = PermissionChecker()