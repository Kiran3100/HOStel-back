"""
OTP (One-Time Password) schemas
"""
from typing import Optional
from pydantic import EmailStr, Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.enums import OTPType


class OTPGenerateRequest(BaseCreateSchema):
    """Generate OTP request"""
    user_id: Optional[UUID] = Field(None, description="User ID (if authenticated)")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{9,14}$', description="Phone number")
    otp_type: OTPType = Field(..., description="OTP purpose")
    
    @field_validator('email', 'phone')
    @classmethod
    def at_least_one_contact(cls, v, info):
        """Ensure at least email or phone is provided"""
        email = info.data.get('email')
        phone = info.data.get('phone')
        if not email and not phone:
            raise ValueError('Either email or phone must be provided')
        return v


class OTPVerifyRequest(BaseCreateSchema):
    """Verify OTP request"""
    user_id: Optional[UUID] = Field(None, description="User ID")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{9,14}$', description="Phone number")
    otp_code: str = Field(..., min_length=6, max_length=6, pattern=r'^\d{6}$', description="6-digit OTP code")
    otp_type: OTPType = Field(..., description="OTP purpose")


class OTPResponse(BaseSchema):
    """OTP generation response"""
    message: str = Field(..., description="Response message")
    expires_in: int = Field(..., description="OTP expiration time in seconds")
    sent_to: str = Field(..., description="Masked email/phone where OTP was sent")
    otp_type: OTPType = Field(..., description="OTP type")
    max_attempts: int = Field(3, description="Maximum verification attempts")


class OTPVerifyResponse(BaseSchema):
    """OTP verification response"""
    is_valid: bool = Field(..., description="Whether OTP is valid")
    message: str = Field(..., description="Response message")
    verified_at: Optional[datetime] = Field(None, description="Verification timestamp")
    user_id: Optional[UUID] = Field(None, description="User ID if applicable")


class ResendOTPRequest(BaseCreateSchema):
    """Resend OTP request"""
    user_id: Optional[UUID] = Field(None, description="User ID")
    email: Optional[EmailStr] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    otp_type: OTPType = Field(..., description="OTP purpose")