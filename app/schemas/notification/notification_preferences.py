"""
Notification preferences schemas
"""
from typing import Dict, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseUpdateSchema


class UserPreferences(BaseSchema):
    """User notification preferences"""
    user_id: UUID
    
    # Global settings
    notifications_enabled: bool = Field(True)
    
    # Channel preferences
    email_enabled: bool = Field(True)
    sms_enabled: bool = Field(True)
    push_enabled: bool = Field(True)
    
    # Frequency
    frequency_settings: "FrequencySettings"
    
    # Quiet hours
    quiet_hours_enabled: bool = Field(False)
    quiet_hours_start: Optional[str] = Field(None, description="HH:MM format")
    quiet_hours_end: Optional[str] = Field(None, description="HH:MM format")
    
    # Category preferences
    payment_notifications: bool = Field(True)
    booking_notifications: bool = Field(True)
    complaint_notifications: bool = Field(True)
    announcement_notifications: bool = Field(True)
    maintenance_notifications: bool = Field(True)
    attendance_notifications: bool = Field(True)
    marketing_notifications: bool = Field(False)


class ChannelPreferences(BaseSchema):
    """Channel-specific preferences"""
    user_id: UUID
    
    # Email preferences
    email: "EmailPreferences"
    
    # SMS preferences
    sms: "SMSPreferences"
    
    # Push preferences
    push: "PushPreferences"


class EmailPreferences(BaseSchema):
    """Email notification preferences"""
    enabled: bool = Field(True)
    
    # Digest settings
    daily_digest: bool = Field(False)
    weekly_digest: bool = Field(False)
    
    # Categories
    receive_payment_emails: bool = Field(True)
    receive_booking_emails: bool = Field(True)
    receive_announcement_emails: bool = Field(True)
    receive_marketing_emails: bool = Field(False)


class SMSPreferences(BaseSchema):
    """SMS notification preferences"""
    enabled: bool = Field(True)
    
    # Only critical by default
    urgent_only: bool = Field(True)
    
    # Categories
    receive_payment_sms: bool = Field(True)
    receive_booking_sms: bool = Field(True)
    receive_emergency_sms: bool = Field(True)


class PushPreferences(BaseSchema):
    """Push notification preferences"""
    enabled: bool = Field(True)
    
    # Sound
    sound_enabled: bool = Field(True)
    
    # Badge
    badge_enabled: bool = Field(True)
    
    # Preview
    show_preview: bool = Field(True, description="Show message preview on lock screen")


class FrequencySettings(BaseSchema):
    """Notification frequency settings"""
    # Immediate
    immediate_notifications: bool = Field(True)
    
    # Batching
    batch_notifications: bool = Field(False)
    batch_interval_hours: int = Field(4, ge=1, le=24)
    
    # Digest
    daily_digest_time: Optional[str] = Field(None, description="HH:MM format")
    weekly_digest_day: Optional[str] = Field(None, description="Monday, Tuesday, etc.")


class PreferenceUpdate(BaseUpdateSchema):
    """Update notification preferences"""
    notifications_enabled: Optional[bool] = None
    email_enabled: Optional[bool] = None
    sms_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None
    
    quiet_hours_enabled: Optional[bool] = None
    quiet_hours_start: Optional[str] = None
    quiet_hours_end: Optional[str] = None
    
    # Category toggles
    payment_notifications: Optional[bool] = None
    booking_notifications: Optional[bool] = None
    complaint_notifications: Optional[bool] = None
    announcement_notifications: Optional[bool] = None
    marketing_notifications: Optional[bool] = None


class UnsubscribeRequest(BaseSchema):
    """Unsubscribe from notifications"""
    user_id: UUID
    unsubscribe_token: str
    
    # What to unsubscribe from
    unsubscribe_type: str = Field(
        ...,
        pattern="^(all|email|sms|marketing|specific_category)$"
    )
    
    category: Optional[str] = None