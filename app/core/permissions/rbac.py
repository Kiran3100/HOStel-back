"""
RBAC (Role-Based Access Control) Manager.

This module acts as the facade for the permissions system,
combining Role checks, Permission checks, and Exception handling.
"""

from typing import Any, List, Optional, Union
from app.core.permissions.roles import role_manager
from app.core.permissions.permissions import permission_checker
from app.core.exceptions.permission_exceptions import (
    PermissionDeniedException,
    InsufficientPermissionsException
)


class RBACManager:
    """
    Main entry point for enforcing access control in the application.
    """
    
    # --- Check Methods (Return Boolean) ---

    def check_access(self, user: Any, permission: str) -> bool:
        """
        Non-blocking check if user has permission.
        """
        return permission_checker.check_permission(user, permission)

    def has_role(self, user: Any, roles: Union[str, List[str]]) -> bool:
        """
        Check if user has one of the specified roles.
        """
        if isinstance(roles, str):
            roles = [roles]
        return user.user_type in roles

    # --- Enforce Methods (Raise Exceptions) ---

    def require_access(self, user: Any, permission: str):
        """
        Enforce permission. Raises PermissionDeniedException if failed.
        
        Usage:
            rbac_manager.require_access(current_user, "hostel:create")
        """
        if not self.check_access(user, permission):
            raise PermissionDeniedException(
                f"User does not have required permission: {permission}"
            )

    def require_role(self, user: Any, allowed_roles: List[str]):
        """
        Enforce role membership.
        """
        if user.user_type not in allowed_roles:
            raise PermissionDeniedException(
                f"User role '{user.user_type}' is not allowed to perform this action"
            )

    def require_hierarchy(self, actor: Any, target_role: str):
        """
        Enforce that actor outranks the target role.
        """
        if not role_manager.can_manage_role(actor.user_type, target_role):
            raise InsufficientPermissionsException(
                "You cannot manage users with equal or higher privilege"
            )

    # --- Utility ---

    def get_effective_permissions(self, user: Any) -> list:
        """
        Return a list of all permissions (static + dynamic) for the UI to use.
        """
        from app.core.permissions.permission_matrix import PermissionMatrix
        
        # Get static permissions
        perms = set(PermissionMatrix.get_permissions_for_role(user.user_type))
        
        # Add dynamic/custom permissions if they exist
        if hasattr(user, "custom_permissions") and user.custom_permissions:
            perms.update(user.custom_permissions)
            
        return list(perms)


# Global instance
rbac_manager = RBACManager()