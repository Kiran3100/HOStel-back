"""
User response schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import UserRole, Gender


class UserResponse(BaseResponseSchema):
    """User response schema"""
    email: str = Field(..., description="Email address")
    phone: str = Field(..., description="Phone number")
    full_name: str = Field(..., description="Full name")
    user_role: UserRole = Field(..., description="User role")
    is_active: bool = Field(..., description="Account active status")
    is_email_verified: bool = Field(..., description="Email verification status")
    is_phone_verified: bool = Field(..., description="Phone verification status")
    profile_image_url: Optional[str] = Field(None, description="Profile image URL")
    last_login_at: Optional[datetime] = Field(None, description="Last login timestamp")


class UserDetail(BaseResponseSchema):
    """Detailed user information"""
    email: str = Field(..., description="Email address")
    phone: str = Field(..., description="Phone number")
    full_name: str = Field(..., description="Full name")
    user_role: UserRole = Field(..., description="User role")
    gender: Optional[Gender] = Field(None, description="Gender")
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    profile_image_url: Optional[str] = Field(None, description="Profile image URL")
    
    # Address
    address_line1: Optional[str] = Field(None, description="Address line 1")
    address_line2: Optional[str] = Field(None, description="Address line 2")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    country: Optional[str] = Field(None, description="Country")
    pincode: Optional[str] = Field(None, description="Pincode")
    
    # Emergency contact
    emergency_contact_name: Optional[str] = Field(None, description="Emergency contact name")
    emergency_contact_phone: Optional[str] = Field(None, description="Emergency contact phone")
    emergency_contact_relation: Optional[str] = Field(None, description="Relation")
    
    # Account status
    is_active: bool = Field(..., description="Account active status")
    is_email_verified: bool = Field(..., description="Email verification status")
    is_phone_verified: bool = Field(..., description="Phone verification status")
    email_verified_at: Optional[datetime] = Field(None, description="Email verification timestamp")
    phone_verified_at: Optional[datetime] = Field(None, description="Phone verification timestamp")
    last_login_at: Optional[datetime] = Field(None, description="Last login timestamp")


class UserListItem(BaseSchema):
    """User list item (minimal info for lists)"""
    id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="Email")
    full_name: str = Field(..., description="Full name")
    user_role: UserRole = Field(..., description="Role")
    is_active: bool = Field(..., description="Active status")
    profile_image_url: Optional[str] = Field(None, description="Profile image")
    created_at: datetime = Field(..., description="Registration date")


class UserProfile(BaseSchema):
    """User public profile"""
    id: UUID = Field(..., description="User ID")
    full_name: str = Field(..., description="Full name")
    profile_image_url: Optional[str] = Field(None, description="Profile image URL")
    user_role: UserRole = Field(..., description="User role")