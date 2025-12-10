"""
Announcement base schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import AnnouncementCategory, Priority, TargetAudience


class AnnouncementBase(BaseSchema):
    """Base announcement schema"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    
    title: str = Field(..., min_length=5, max_length=255, description="Announcement title")
    content: str = Field(..., min_length=10, max_length=5000, description="Announcement content")
    
    category: AnnouncementCategory = Field(..., description="Announcement category")
    priority: Priority = Field(Priority.MEDIUM, description="Priority level")
    
    # Visibility
    is_urgent: bool = Field(False, description="Mark as urgent")
    is_pinned: bool = Field(False, description="Pin to top")
    
    # Target audience
    target_audience: TargetAudience = Field(TargetAudience.ALL, description="Target audience")
    target_room_ids: List[UUID] = Field(default_factory=list, description="Specific rooms")
    target_student_ids: List[UUID] = Field(default_factory=list, description="Specific students")
    target_floor_numbers: List[int] = Field(default_factory=list, description="Specific floors")
    
    # Attachments
    attachments: List[HttpUrl] = Field(default_factory=list, description="Attachment URLs")
    
    # Expiry
    expires_at: Optional[datetime] = Field(None, description="When announcement expires")


class AnnouncementCreate(AnnouncementBase, BaseCreateSchema):
    """Create announcement"""
    created_by: UUID = Field(..., description="Creator (admin/supervisor)")
    
    # Delivery settings
    send_email: bool = Field(False, description="Send email notification")
    send_sms: bool = Field(False, description="Send SMS notification")
    send_push: bool = Field(True, description="Send push notification")


class AnnouncementUpdate(BaseUpdateSchema):
    """Update announcement"""
    title: Optional[str] = Field(None, min_length=5, max_length=255)
    content: Optional[str] = Field(None, min_length=10, max_length=5000)
    category: Optional[AnnouncementCategory] = None
    priority: Optional[Priority] = None
    
    is_urgent: Optional[bool] = None
    is_pinned: Optional[bool] = None
    
    expires_at: Optional[datetime] = None
    
    # Publication
    is_published: Optional[bool] = None