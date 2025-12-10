"""
Registration schemas
"""
from typing import Optional
from pydantic import EmailStr, Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.enums import UserRole, Gender


class RegisterRequest(BaseCreateSchema):
    """User registration request"""
    email: EmailStr = Field(..., description="Email address")
    phone: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$', description="Phone number")
    password: str = Field(..., min_length=8, max_length=128, description="Password")
    confirm_password: str = Field(..., description="Password confirmation")
    full_name: str = Field(..., min_length=2, max_length=255, description="Full name")
    role: UserRole = Field(UserRole.VISITOR, description="User role (defaults to visitor)")
    gender: Optional[Gender] = Field(None, description="Gender")
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """Validate passwords match"""
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @field_validator('password')
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
        return v


class RegisterResponse(BaseSchema):
    """Registration response"""
    user_id: UUID = Field(..., description="Created user ID")
    email: str = Field(..., description="User email")
    full_name: str = Field(..., description="User full name")
    role: UserRole = Field(..., description="User role")
    message: str = Field(..., description="Success message")
    verification_required: bool = Field(True, description="Whether email/phone verification is required")


class VerifyEmailRequest(BaseCreateSchema):
    """Email verification request"""
    user_id: UUID = Field(..., description="User ID")
    verification_code: str = Field(..., min_length=6, max_length=6, description="6-digit verification code")


class VerifyPhoneRequest(BaseCreateSchema):
    """Phone verification request"""
    user_id: UUID = Field(..., description="User ID")
    verification_code: str = Field(..., min_length=6, max_length=6, description="6-digit verification code")


class ResendVerificationRequest(BaseCreateSchema):
    """Resend verification code request"""
    user_id: UUID = Field(..., description="User ID")
    verification_type: str = Field(..., pattern="^(email|phone)$", description="Verification type")