"""
User profile update schemas
"""
from datetime import date
from typing import Optional
from pydantic import EmailStr, Field, HttpUrl

from app.schemas.common.base import BaseUpdateSchema
from app.schemas.common.enums import Gender


class ProfileUpdate(BaseUpdateSchema):
    """Update user profile"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=255, description="Full name")
    gender: Optional[Gender] = Field(None, description="Gender")
    date_of_birth: Optional[date] = Field(None, description="Date of birth")
    address_line1: Optional[str] = Field(None, description="Address line 1")
    address_line2: Optional[str] = Field(None, description="Address line 2")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    pincode: Optional[str] = Field(None, pattern=r'^\d{6}$', description="Pincode")
    country: Optional[str] = Field(None, description="Country")


class ProfileImageUpdate(BaseUpdateSchema):
    """Update profile image"""
    profile_image_url: HttpUrl = Field(..., description="Profile image URL")


class ContactInfoUpdate(BaseUpdateSchema):
    """Update contact information"""
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{9,14}$', description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    emergency_contact_name: Optional[str] = Field(None, description="Emergency contact name")
    emergency_contact_phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{9,14}$', description="Emergency phone")
    emergency_contact_relation: Optional[str] = Field(None, description="Relation")


class NotificationPreferencesUpdate(BaseUpdateSchema):
    """Update notification preferences"""
    email_notifications: bool = Field(True, description="Enable email notifications")
    sms_notifications: bool = Field(True, description="Enable SMS notifications")
    push_notifications: bool = Field(True, description="Enable push notifications")
    
    # Specific notification types
    booking_notifications: bool = Field(True, description="Booking-related notifications")
    payment_notifications: bool = Field(True, description="Payment notifications")
    complaint_notifications: bool = Field(True, description="Complaint updates")
    announcement_notifications: bool = Field(True, description="Hostel announcements")
    marketing_notifications: bool = Field(False, description="Marketing communications")