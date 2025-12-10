"""
Token management schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.enums import UserRole


class Token(BaseSchema):
    """JWT token schema"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenPayload(BaseSchema):
    """JWT token payload"""
    sub: str = Field(..., description="Subject (user_id)")
    user_id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    role: UserRole = Field(..., description="User role")
    hostel_id: Optional[UUID] = Field(None, description="Active hostel context")
    exp: int = Field(..., description="Expiration timestamp")
    iat: int = Field(..., description="Issued at timestamp")
    jti: str = Field(..., description="JWT ID (unique token identifier)")


class RefreshTokenRequest(BaseCreateSchema):
    """Refresh token request"""
    refresh_token: str = Field(..., description="Refresh token")


class RefreshTokenResponse(BaseSchema):
    """Refresh token response"""
    access_token: str = Field(..., description="New JWT access token")
    refresh_token: str = Field(..., description="New refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenValidationRequest(BaseCreateSchema):
    """Token validation request"""
    token: str = Field(..., description="Token to validate")


class TokenValidationResponse(BaseSchema):
    """Token validation response"""
    is_valid: bool = Field(..., description="Whether token is valid")
    user_id: Optional[UUID] = Field(None, description="User ID if valid")
    role: Optional[UserRole] = Field(None, description="User role if valid")
    expires_at: Optional[datetime] = Field(None, description="Token expiration datetime")


class RevokeTokenRequest(BaseCreateSchema):
    """Revoke token request"""
    token: str = Field(..., description="Token to revoke")
    revoke_all: bool = Field(False, description="Revoke all user tokens")


class LogoutRequest(BaseCreateSchema):
    """Logout request"""
    refresh_token: Optional[str] = Field(None, description="Refresh token to revoke")
    logout_all_devices: bool = Field(False, description="Logout from all devices")