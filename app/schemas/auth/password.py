"""
Password management schemas
"""
from typing import Optional
from pydantic import EmailStr, Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class PasswordResetRequest(BaseCreateSchema):
    """Password reset request (forgot password)"""
    email: EmailStr = Field(..., description="User email address")


class PasswordResetConfirm(BaseCreateSchema):
    """Confirm password reset with token"""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """Validate passwords match"""
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('Passwords do not match')
        return v
    
    @field_validator('new_password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in v):
            raise ValueError('Password must contain at least one special character')
        return v


class PasswordChangeRequest(BaseCreateSchema):
    """Change password (authenticated user)"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """Validate passwords match"""
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('Passwords do not match')
        return v
    
    @field_validator('new_password')
    @classmethod
    def validate_password_different(cls, v: str, info) -> str:
        """Ensure new password is different from current"""
        if 'current_password' in info.data and v == info.data['current_password']:
            raise ValueError('New password must be different from current password')
        return v


class PasswordChangeResponse(BaseSchema):
    """Password change response"""
    message: str = Field(..., description="Success message")
    user_id: UUID = Field(..., description="User ID")


class PasswordStrengthCheck(BaseCreateSchema):
    """Check password strength"""
    password: str = Field(..., description="Password to check")


class PasswordStrengthResponse(BaseSchema):
    """Password strength response"""
    score: int = Field(..., ge=0, le=5, description="Strength score (0-5)")
    strength: str = Field(..., description="Strength label (weak/medium/strong/very_strong)")
    has_minimum_length: bool = Field(..., description="Has minimum 8 characters")
    has_uppercase: bool = Field(..., description="Has uppercase letter")
    has_lowercase: bool = Field(..., description="Has lowercase letter")
    has_digit: bool = Field(..., description="Has digit")
    has_special_char: bool = Field(..., description="Has special character")
    suggestions: list[str] = Field(default_factory=list, description="Improvement suggestions")