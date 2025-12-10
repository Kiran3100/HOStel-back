# --- File: app/core/exceptions/permission_exceptions.py ---
"""
Permission and authorization exceptions.

This module contains all exceptions related to user permissions,
role-based access control, and authorization failures.
"""

from typing import Optional, Dict, Any, List
from fastapi import status
from app.core.exceptions.base import BaseSecurityException
from app.core.constants import ERROR_PERMISSION_DENIED


class PermissionDeniedException(BaseSecurityException):
    """
    General permission denied exception.
    
    Raised when user doesn't have required permissions for an action.
    """
    
    def __init__(
        self,
        message: str = "Permission denied",
        required_permission: Optional[str] = None,
        user_permissions: Optional[List[str]] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        permission_details = details or {}
        if required_permission:
            permission_details["required_permission"] = required_permission
        if user_permissions:
            permission_details["user_permissions"] = user_permissions
        
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=ERROR_PERMISSION_DENIED,
            details=permission_details
        )


class InsufficientPermissionsException(PermissionDeniedException):
    """
    Exception raised when user has some permissions but not enough.
    
    User is authenticated but lacks specific permissions for the action.
    """
    
    def __init__(
        self,
        message: str = "Insufficient permissions for this action",
        required_permissions: Optional[List[str]] = None,
        missing_permissions: Optional[List[str]] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        permission_details = details or {}
        if required_permissions:
            permission_details["required_permissions"] = required_permissions
        if missing_permissions:
            permission_details["missing_permissions"] = missing_permissions
        
        super().__init__(
            message=message,
            details=permission_details
        )


class UnauthorizedAccessException(PermissionDeniedException):
    """
    Exception raised for unauthorized access attempts.
    
    User is trying to access resources they don't own or manage.
    """
    
    def __init__(
        self,
        message: str = "Unauthorized access to resource",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        action: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        access_details = details or {}
        if resource_type:
            access_details["resource_type"] = resource_type
        if resource_id:
            access_details["resource_id"] = resource_id
        if action:
            access_details["attempted_action"] = action
        
        super().__init__(
            message=message,
            details=access_details
        )


class HostelAccessDeniedException(PermissionDeniedException):
    """
    Exception raised when user tries to access a hostel they don't manage.
    
    Specific to hostel-based access control in the multi-tenant system.
    """
    
    def __init__(
        self,
        message: str = "Access denied to hostel",
        hostel_id: Optional[str] = None,
        user_hostels: Optional[List[str]] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        hostel_details = details or {}
        if hostel_id:
            hostel_details["hostel_id"] = hostel_id
        if user_hostels:
            hostel_details["user_hostels"] = user_hostels
        
        super().__init__(
            message=message,
            details=hostel_details
        )


class SupervisorScopeException(PermissionDeniedException):
    """
    Exception raised when supervisor tries to act outside their scope.
    
    Supervisors can only manage resources within their assigned hostel.
    """
    
    def __init__(
        self,
        message: str = "Action outside supervisor scope",
        supervisor_hostel: Optional[str] = None,
        attempted_hostel: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        scope_details = details or {}
        if supervisor_hostel:
            scope_details["supervisor_hostel"] = supervisor_hostel
        if attempted_hostel:
            scope_details["attempted_hostel"] = attempted_hostel
        
        super().__init__(
            message=message,
            details=scope_details
        )


class RoleHierarchyException(PermissionDeniedException):
    """
    Exception raised when user tries to manage someone with equal/higher role.
    
    Users cannot manage other users with equal or higher privilege levels.
    """
    
    def __init__(
        self,
        message: str = "Cannot manage user with equal or higher privileges",
        user_role: Optional[str] = None,
        target_role: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        hierarchy_details = details or {}
        if user_role:
            hierarchy_details["user_role"] = user_role
        if target_role:
            hierarchy_details["target_role"] = target_role
        
        super().__init__(
            message=message,
            details=hierarchy_details
        )


class ApprovalAuthorityException(PermissionDeniedException):
    """
    Exception raised when user lacks approval authority for financial thresholds.
    
    User cannot approve requests above their financial authority limits.
    """
    
    def __init__(
        self,
        message: str = "Insufficient approval authority",
        requested_amount: Optional[float] = None,
        user_limit: Optional[float] = None,
        approval_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        approval_details = details or {}
        if requested_amount is not None:
            approval_details["requested_amount"] = requested_amount
        if user_limit is not None:
            approval_details["user_limit"] = user_limit
        if approval_type:
            approval_details["approval_type"] = approval_type
        
        super().__init__(
            message=message,
            details=approval_details
        )


class ResourceOwnershipException(PermissionDeniedException):
    """
    Exception raised when user tries to access resources they don't own.
    
    Users can typically only access their own data unless they have admin rights.
    """
    
    def __init__(
        self,
        message: str = "Access denied: not resource owner",
        resource_type: Optional[str] = None,
        resource_owner: Optional[str] = None,
        requesting_user: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        ownership_details = details or {}
        if resource_type:
            ownership_details["resource_type"] = resource_type
        if resource_owner:
            ownership_details["resource_owner"] = resource_owner
        if requesting_user:
            ownership_details["requesting_user"] = requesting_user
        
        super().__init__(
            message=message,
            details=ownership_details
        )


class FeatureDisabledException(PermissionDeniedException):
    """
    Exception raised when trying to access a disabled feature.
    
    Some features may be disabled based on subscription plan or configuration.
    """
    
    def __init__(
        self,
        message: str = "Feature is not available",
        feature_name: Optional[str] = None,
        required_plan: Optional[str] = None,
        current_plan: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        feature_details = details or {}
        if feature_name:
            feature_details["feature_name"] = feature_name
        if required_plan:
            feature_details["required_plan"] = required_plan
        if current_plan:
            feature_details["current_plan"] = current_plan
        
        super().__init__(
            message=message,
            details=feature_details
        )


class TemporaryAccessDeniedException(PermissionDeniedException):
    """
    Exception raised when access is temporarily denied.
    
    Access may be denied due to maintenance, rate limiting, or temporary restrictions.
    """
    
    def __init__(
        self,
        message: str = "Access temporarily denied",
        reason: Optional[str] = None,
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        temp_details = details or {}
        if reason:
            temp_details["reason"] = reason
        if retry_after:
            temp_details["retry_after_seconds"] = retry_after
        
        headers = {}
        if retry_after:
            headers["Retry-After"] = str(retry_after)
        
        super().__init__(
            message=message,
            details=temp_details
        )
        self.headers.update(headers)