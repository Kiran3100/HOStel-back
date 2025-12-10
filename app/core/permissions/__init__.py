"""
Permission Management Package.

This package handles the security layer responsible for:
1. Role-Based Access Control (RBAC) - What a role can generally do.
2. Resource-Level Permissions - Accessing specific data instances.
3. Approval Authority - Financial and operational thresholds.
"""

from app.core.permissions.roles import RoleManager, role_manager
from app.core.permissions.permissions import PermissionChecker, permission_checker
from app.core.permissions.rbac import RBACManager, rbac_manager
from app.core.permissions.permission_matrix import PermissionMatrix
from app.core.permissions.resource_permissions import ResourcePermission, resource_permission
from app.core.permissions.approval_authority import ApprovalAuthority, approval_authority

__all__ = [
    "RoleManager",
    "role_manager",
    "PermissionChecker",
    "permission_checker",
    "RBACManager",
    "rbac_manager",
    "PermissionMatrix",
    "ResourcePermission",
    "resource_permission",
    "ApprovalAuthority",
    "approval_authority",
]