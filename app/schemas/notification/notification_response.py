"""
Notification response schemas
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import NotificationType, NotificationStatus


class NotificationResponse(BaseResponseSchema):
    """Notification response"""
    recipient_user_id: Optional[UUID]
    recipient_email: Optional[str]
    recipient_phone: Optional[str]
    
    notification_type: NotificationType
    
    subject: Optional[str]
    message_body: str
    
    priority: str
    status: NotificationStatus
    
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    
    created_at: datetime


class NotificationDetail(BaseResponseSchema):
    """Detailed notification information"""
    recipient_user_id: Optional[UUID]
    recipient_email: Optional[str]
    recipient_phone: Optional[str]
    
    notification_type: NotificationType
    template_code: Optional[str]
    
    subject: Optional[str]
    message_body: str
    
    priority: str
    status: NotificationStatus
    
    # Schedule
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    failed_at: Optional[datetime]
    
    # Delivery
    failure_reason: Optional[str]
    retry_count: int
    max_retries: int
    
    # Metadata
    metadata: Dict[str, Any]
    
    # Related
    hostel_id: Optional[UUID]
    
    # Timestamps
    created_at: datetime
    updated_at: datetime


class NotificationList(BaseSchema):
    """List of notifications for user"""
    user_id: UUID
    
    total_notifications: int
    unread_count: int
    
    notifications: List["NotificationListItem"]


class NotificationListItem(BaseSchema):
    """Notification list item"""
    id: UUID
    notification_type: NotificationType
    
    subject: Optional[str]
    message_preview: str = Field(..., description="First 100 characters")
    
    priority: str
    
    is_read: bool = Field(False)
    read_at: Optional[datetime]
    
    created_at: datetime
    
    # Quick actions
    action_url: Optional[str] = Field(None, description="URL to navigate to")
    icon: Optional[str] = Field(None, description="Icon identifier")


class UnreadCount(BaseSchema):
    """Unread notification count"""
    user_id: UUID
    
    total_unread: int
    
    # By type
    email_unread: int
    sms_unread: int
    push_unread: int
    in_app_unread: int
    
    # By priority
    urgent_unread: int
    high_unread: int


class NotificationSummary(BaseSchema):
    """Notification summary for user"""
    user_id: UUID
    
    # Counts
    total_notifications: int
    unread_notifications: int
    
    # Recent
    last_notification_at: Optional[datetime]
    
    # By type
    notifications_by_type: Dict[str, int]
    
    # By status
    notifications_by_status: Dict[str, int]