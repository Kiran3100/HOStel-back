"""
Authentication and authorization related exceptions.
"""

from typing import Optional, Dict, Any
from .base import BaseAPIException


class AuthenticationException(BaseAPIException):
    """Base exception for authentication failures."""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        error_code: str = "AUTH_FAILED",
        **kwargs
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=401,
            user_message="Authentication required. Please log in.",
            **kwargs
        )


class InvalidCredentialsException(AuthenticationException):
    """Raised when user provides invalid login credentials."""
    
    def __init__(
        self,
        message: str = "Invalid username or password",
        error_code: str = "INVALID_CREDENTIALS",
        username: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            user_message="Invalid username or password. Please try again.",
            **kwargs
        )
        if username:
            self.add_context('username', username)


class TokenExpiredException(AuthenticationException):
    """Raised when JWT token has expired."""
    
    def __init__(
        self,
        message: str = "Token has expired",
        error_code: str = "TOKEN_EXPIRED",
        token_type: str = "access",
        **kwargs
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            user_message="Your session has expired. Please log in again.",
            **kwargs
        )
        self.add_context('token_type', token_type)


class InvalidTokenException(AuthenticationException):
    """Raised when JWT token is invalid or malformed."""
    
    def __init__(
        self,
        message: str = "Invalid token",
        error_code: str = "INVALID_TOKEN",
        token_type: str = "access",
        reason: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            user_message="Invalid authentication token. Please log in again.",
            **kwargs
        )
        self.add_context('token_type', token_type)
        if reason:
            self.add_context('reason', reason)


class UserNotActiveException(AuthenticationException):
    """Raised when user account is not active."""
    
    def __init__(
        self,
        message: str = "User account is not active",
        error_code: str = "USER_NOT_ACTIVE",
        user_id: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            user_message="Your account is not active. Please contact support.",
            **kwargs
        )
        if user_id:
            self.add_context('user_id', user_id)


class EmailNotVerifiedException(AuthenticationException):
    """Raised when user's email is not verified."""
    
    def __init__(
        self,
        message: str = "Email address not verified",
        error_code: str = "EMAIL_NOT_VERIFIED",
        email: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            user_message="Please verify your email address before logging in.",
            **kwargs
        )
        if email:
            self.add_context('email', email)


class AccountLockedException(AuthenticationException):
    """Raised when user account is locked due to security reasons."""
    
    def __init__(
        self,
        message: str = "Account is locked",
        error_code: str = "ACCOUNT_LOCKED",
        user_id: Optional[str] = None,
        lock_reason: Optional[str] = None,
        unlock_time: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            user_message="Your account has been locked. Please contact support.",
            **kwargs
        )
        if user_id:
            self.add_context('user_id', user_id)
        if lock_reason:
            self.add_context('lock_reason', lock_reason)
        if unlock_time:
            self.add_context('unlock_time', unlock_time)


class PasswordExpiredException(AuthenticationException):
    """Raised when user's password has expired."""
    
    def __init__(
        self,
        message: str = "Password has expired",
        error_code: str = "PASSWORD_EXPIRED",
        user_id: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            user_message="Your password has expired. Please