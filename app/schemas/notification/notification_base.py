"""
Notification base schemas
"""
from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import NotificationType, Priority


class NotificationBase(BaseSchema):
    """Base notification schema"""
    recipient_user_id: Optional[UUID] = Field(None, description="Recipient user ID")
    recipient_email: Optional[str] = Field(None, description="Recipient email")
    recipient_phone: Optional[str] = Field(None, description="Recipient phone")
    
    notification_type: NotificationType = Field(..., description="Notification channel")
    
    # Template
    template_code: Optional[str] = Field(None, description="Template code to use")
    
    # Content
    subject: Optional[str] = Field(None, max_length=255, description="Subject/Title")
    message_body: str = Field(..., description="Message content")
    
    # Priority
    priority: Priority = Field(Priority.MEDIUM, description="Delivery priority")
    
    # Schedule
    scheduled_at: Optional[datetime] = Field(None, description="When to send (null = immediate)")
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context data")
    
    # Related entity
    hostel_id: Optional[UUID] = Field(None, description="Related hostel")


class NotificationCreate(NotificationBase, BaseCreateSchema):
    """Create notification"""
    pass


class NotificationUpdate(BaseUpdateSchema):
    """Update notification (limited fields)"""
    scheduled_at: Optional[datetime] = None
    priority: Optional[Priority] = None
    status: Optional[str] = None


class MarkAsRead(BaseCreateSchema):
    """Mark notification as read"""
    notification_id: UUID
    user_id: UUID


class BulkMarkAsRead(BaseCreateSchema):
    """Mark multiple notifications as read"""
    notification_ids: List[UUID] = Field(..., min_items=1)
    user_id: UUID


class NotificationDelete(BaseCreateSchema):
    """Delete notification"""
    notification_id: UUID
    user_id: UUID
    
    # Soft delete
    permanent: bool = Field(False, description="Permanently delete vs soft delete")