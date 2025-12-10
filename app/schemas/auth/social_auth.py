"""
Social authentication schemas (Google, Facebook OAuth)
"""
from typing import Optional
from pydantic import EmailStr, Field, HttpUrl

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.enums import UserRole, Gender


class SocialAuthRequest(BaseCreateSchema):
    """Base social authentication request"""
    access_token: str = Field(..., description="OAuth access token from provider")
    provider: str = Field(..., pattern="^(google|facebook)$", description="OAuth provider")


class GoogleAuthRequest(BaseCreateSchema):
    """Google OAuth authentication request"""
    id_token: str = Field(..., description="Google ID token")
    access_token: Optional[str] = Field(None, description="Google access token")


class FacebookAuthRequest(BaseCreateSchema):
    """Facebook OAuth authentication request"""
    access_token: str = Field(..., description="Facebook access token")
    user_id: str = Field(..., description="Facebook user ID")


class SocialAuthResponse(BaseSchema):
    """Social authentication response"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")
    user: "SocialUserInfo" = Field(..., description="User information")
    is_new_user: bool = Field(..., description="Whether this is a new user registration")


class SocialUserInfo(BaseSchema):
    """User information from social auth"""
    id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    full_name: str = Field(..., description="User full name")
    role: UserRole = Field(..., description="User role")
    profile_image_url: Optional[str] = Field(None, description="Profile image URL")
    is_email_verified: bool = Field(True, description="Email verification status")


class SocialProfileData(BaseSchema):
    """Profile data from social provider"""
    provider_user_id: str = Field(..., description="User ID from provider")
    email: EmailStr = Field(..., description="Email from provider")
    full_name: str = Field(..., description="Full name from provider")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    profile_picture_url: Optional[HttpUrl] = Field(None, description="Profile picture URL")
    gender: Optional[Gender] = Field(None, description="Gender")
    locale: Optional[str] = Field(None, description="User locale")