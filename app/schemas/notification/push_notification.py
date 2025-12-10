"""
Push notification schemas
"""
from datetime import datetime
from typing import Dict, Optional, List, Any
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema
from app.schemas.common.enums import DeviceType


class PushRequest(BaseCreateSchema):
    """Send push notification"""
    # Recipients
    user_id: Optional[UUID] = Field(None, description="Send to all devices of this user")
    device_token: Optional[str] = Field(None, description="Send to specific device")
    device_tokens: Optional[List[str]] = Field(None, description="Send to multiple devices")
    
    # Content
    title: str = Field(..., min_length=1, max_length=100)
    body: str = Field(..., min_length=1, max_length=500)
    
    # Additional data
    data: Dict[str, Any] = Field(default_factory=dict, description="Custom data payload")
    
    # Action
    action_url: Optional[str] = Field(None, description="Deep link or URL to open")
    
    # Appearance
    icon: Optional[str] = None
    image_url: Optional[str] = None
    badge_count: Optional[int] = Field(None, ge=0)
    
    # Sound
    sound: Optional[str] = Field("default", description="Notification sound")
    
    # Priority
    priority: str = Field("normal", pattern="^(low|normal|high)$")
    
    # Time to live
    ttl: int = Field(86400, ge=0, description="Time to live in seconds")


class PushConfig(BaseSchema):
    """Push notification configuration"""
    # Firebase
    firebase_project_id: str
    firebase_server_key: str
    
    # APNs (iOS)
    apns_key_id: Optional[str]
    apns_team_id: Optional[str]
    apns_bundle_id: Optional[str]
    
    # Settings
    collapse_key: Optional[str] = Field(None, description="Notification grouping")
    
    # Badge management
    auto_increment_badge: bool = Field(True)


class DeviceToken(BaseResponseSchema):
    """Device token registration"""
    user_id: UUID
    device_token: str
    device_type: DeviceType
    
    device_name: Optional[str]
    device_model: Optional[str]
    os_version: Optional[str]
    app_version: Optional[str]
    
    is_active: bool
    last_used_at: datetime
    registered_at: datetime


class DeviceRegistration(BaseCreateSchema):
    """Register device for push notifications"""
    user_id: UUID
    device_token: str = Field(..., min_length=10)
    device_type: DeviceType
    
    # Device details
    device_name: Optional[str] = None
    device_model: Optional[str] = None
    os_version: Optional[str] = None
    app_version: Optional[str] = None
    
    # Timezone
    timezone: Optional[str] = Field(None, description="Device timezone")


class DeviceUnregistration(BaseCreateSchema):
    """Unregister device"""
    device_token: str
    user_id: Optional[UUID] = None


class PushTemplate(BaseSchema):
    """Push notification template"""
    template_code: str
    
    title: str
    body: str
    
    # Default settings
    default_icon: Optional[str]
    default_sound: str = Field("default")
    
    # Variables
    required_variables: List[str]
    
    # Actions
    default_action_url: Optional[str]


class PushDeliveryStatus(BaseSchema):
    """Push notification delivery status"""
    notification_id: UUID
    device_token: str
    
    status: str = Field(
        ...,
        pattern="^(queued|sent|delivered|failed|expired)$"
    )
    
    sent_at: Optional[datetime]
    delivered_at: Optional[datetime]
    failed_at: Optional[datetime]
    
    error_code: Optional[str]
    error_message: Optional[str]
    
    # Provider details
    provider_message_id: Optional[str]


class PushStats(BaseSchema):
    """Push notification statistics"""
    total_sent: int
    total_delivered: int
    total_failed: int
    
    delivery_rate: Decimal
    
    # By platform
    ios_sent: int
    android_sent: int
    web_sent: int
    
    # Engagement
    total_opened: int
    open_rate: Decimal
    
    period_start: date
    period_end: date