"""
User base schemas
"""
from datetime import date
from typing import Optional
from pydantic import EmailStr, Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import UserRole, Gender
from app.schemas.common.mixins import AddressMixin, EmergencyContactMixin


class UserBase(BaseSchema):
    """Base user schema"""
    email: EmailStr = Field(..., description="Email address")
    phone: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$', description="Phone number")
    full_name: str = Field(..., min_length=2, max_length=255, description="Full name")
    user_role: UserRole = Field(..., description="User role")
    gender: Optional[Gender] = Field(None, description="Gender")
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    profile_image_url: Optional[str] = Field(None, description="Profile image URL")
    
    @field_validator('date_of_birth')
    @classmethod
    def validate_age(cls, v: Optional[date]) -> Optional[date]:
        """Validate user is at least 16 years old"""
        if v:
            from datetime import date
            today = date.today()
            age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
            if age < 16:
                raise ValueError('User must be at least 16 years old')
            if age > 100:
                raise ValueError('Invalid date of birth')
        return v


class UserCreate(UserBase, BaseCreateSchema):
    """Create user schema"""
    password: str = Field(..., min_length=8, max_length=128, description="Password")
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v


class UserUpdate(BaseUpdateSchema):
    """Update user schema (all fields optional)"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{9,14}$')
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None
    profile_image_url: Optional[str] = None
    is_active: Optional[bool] = None


class UserAddressUpdate(AddressMixin, BaseUpdateSchema):
    """Update user address"""
    pass


class UserEmergencyContactUpdate(EmergencyContactMixin, BaseUpdateSchema):
    """Update emergency contact information"""
    pass