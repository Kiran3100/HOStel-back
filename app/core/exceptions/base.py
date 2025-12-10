# --- File: app/core/exceptions/base.py ---
"""
Base exception classes for the application.

This module defines the foundation exception classes that all other
custom exceptions inherit from.
"""

from typing import Any, Dict, Optional, Union
from fastapi import status


class BaseAPIException(Exception):
    """
    Base exception class for all API-related exceptions.
    
    This class provides a foundation for all custom exceptions
    with consistent error handling and response formatting.
    """
    
    def __init__(
        self,
        message: str = "An error occurred",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        """
        Initialize base API exception.
        
        Args:
            message: Human-readable error message
            status_code: HTTP status code
            error_code: Application-specific error code
            details: Additional error details
            headers: HTTP headers to include in response
        """
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        self.headers = headers or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to dictionary for JSON response.
        
        Returns:
            Dictionary representation of the exception
        """
        error_dict = {
            "error": True,
            "message": self.message,
            "status_code": self.status_code
        }
        
        if self.error_code:
            error_dict["error_code"] = self.error_code
        
        if self.details:
            error_dict["details"] = self.details
        
        return error_dict
    
    def __str__(self) -> str:
        """String representation of the exception."""
        return f"{self.__class__.__name__}: {self.message}"
class BaseBusinessException(BaseAPIException):
    """
    Base exception class for business logic violations.
    
    This class is used for exceptions that occur due to business rule
    violations rather than technical errors.
    """
    
    def __init__(
        self,
        message: str = "Business rule violation",
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize business exception.
        
        Args:
            message: Business rule violation message
            error_code: Business-specific error code
            details: Additional business context
        """
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code=error_code,
            details=details
        )


class BaseValidationException(BaseAPIException):
    """
    Base exception class for validation errors.
    
    This class is used for input validation failures and
    data integrity violations.
    """
    
    def __init__(
        self,
        message: str = "Validation failed",
        field: Optional[str] = None,
        value: Optional[Any] = None,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize validation exception.
        
        Args:
            message: Validation error message
            field: Field that failed validation
            value: Value that failed validation
            error_code: Validation-specific error code
            details: Additional validation context
        """
        validation_details = details or {}
        
        if field:
            validation_details["field"] = field
        
        if value is not None:
            validation_details["value"] = str(value)
        
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=error_code,
            details=validation_details
        )


class BaseSecurityException(BaseAPIException):
    """
    Base exception class for security-related errors.
    
    This class is used for authentication, authorization,
    and other security violations.
    """
    
    def __init__(
        self,
        message: str = "Security violation",
        status_code: int = status.HTTP_403_FORBIDDEN,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize security exception.
        
        Args:
            message: Security violation message
            status_code: HTTP status code (default: 403)
            error_code: Security-specific error code
            details: Additional security context
        """
        super().__init__(
            message=message,
            status_code=status_code,
            error_code=error_code,
            details=details
        )


class BaseResourceException(BaseAPIException):
    """
    Base exception class for resource-related errors.
    
    This class is used for resource not found, resource
    conflicts, and other resource-related issues.
    """
    
    def __init__(
        self,
        message: str = "Resource error",
        resource_type: Optional[str] = None,
        resource_id: Optional[Union[str, int]] = None,
        status_code: int = status.HTTP_404_NOT_FOUND,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize resource exception.
        
        Args:
            message: Resource error message
            resource_type: Type of resource (e.g., 'user', 'hostel')
            resource_id: ID of the resource
            status_code: HTTP status code (default: 404)
            error_code: Resource-specific error code
            details: Additional resource context
        """
        resource_details = details or {}
        
        if resource_type:
            resource_details["resource_type"] = resource_type
        
        if resource_id is not None:
            resource_details["resource_id"] = str(resource_id)
        
        super().__init__(
            message=message,
            status_code=status_code,
            error_code=error_code,
            details=resource_details
        )