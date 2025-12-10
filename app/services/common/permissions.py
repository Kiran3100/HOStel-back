# app/services/common/permissions.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Optional, Set
from uuid import UUID

from app.schemas.common.enums import UserRole


class PermissionDenied(Exception):
    """Raised when a user tries an action they are not allowed to perform."""


@dataclass(frozen=True)
class Principal:
    """
    Represents the current authenticated user in the service layer.
    """
    user_id: UUID
    role: UserRole
    # Optional fine-grained permissions (e.g. {'complaint.view', 'student.edit'})
    permissions: Optional[Set[str]] = None


def role_in(principal: Principal, allowed_roles: Iterable[UserRole]) -> bool:
    """Return True if principal.role is in allowed_roles."""
    return principal.role in set(allowed_roles)


def has_permission(
    principal: Principal,
    permission_key: str,
    *,
    matrix: Optional[Mapping[UserRole, Set[str]]] = None,
) -> bool:
    """
    Check if the principal has a given permission.

    Resolution:
    1. Check explicit principal.permissions if provided.
    2. Fallback to role-based matrix if provided.
    """
    if principal.permissions is not None and permission_key in principal.permissions:
        return True

    if matrix is not None:
        allowed_for_role = matrix.get(principal.role, set())
        if permission_key in allowed_for_role:
            return True

    return False


def require_permission(
    principal: Principal,
    permission_key: str,
    *,
    matrix: Optional[Mapping[UserRole, Set[str]]] = None,
) -> None:
    """
    Assert that the principal has the specified permission.

    Raises PermissionDenied if not.
    """
    if not has_permission(principal, permission_key, matrix=matrix):
        raise PermissionDenied(
            f"User {principal.user_id} with role {principal.role.value!r} "
            f"lacks permission {permission_key!r}"
        )