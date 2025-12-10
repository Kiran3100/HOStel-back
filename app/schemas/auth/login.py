"""
Login schemas
"""
from typing import Optional
from pydantic import EmailStr, Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.enums import UserRole


class LoginRequest(BaseCreateSchema):
    """Login request schema"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="User password")
    remember_me: bool = Field(False, description="Remember user session")


class PhoneLoginRequest(BaseCreateSchema):
    """Phone-based login request"""
    phone: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$', description="Phone number")
    password: str = Field(..., min_length=8, max_length=128, description="User password")
    remember_me: bool = Field(False, description="Remember user session")


class TokenData(BaseSchema):
    """Token data embedded in JWT"""
    user_id: UUID = Field(..., description="User unique identifier")
    email: str = Field(..., description="User email")
    role: UserRole = Field(..., description="User role")
    hostel_id: Optional[UUID] = Field(None, description="Active hostel context (for multi-hostel admins)")


class LoginResponse(BaseSchema):
    """Login response schema"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: "UserLoginInfo" = Field(..., description="User information")


class UserLoginInfo(BaseSchema):
    """User information in login response"""
    id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    full_name: str = Field(..., description="User full name")
    role: UserRole = Field(..., description="User role")
    is_email_verified: bool = Field(..., description="Email verification status")
    is_phone_verified: bool = Field(..., description="Phone verification status")
    profile_image_url: Optional[str] = Field(None, description="Profile image URL")