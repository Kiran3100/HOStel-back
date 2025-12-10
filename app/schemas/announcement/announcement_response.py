"""
Announcement response schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import AnnouncementCategory, Priority


class AnnouncementResponse(BaseResponseSchema):
    """Announcement response"""
    hostel_id: UUID
    hostel_name: str
    
    title: str
    content: str
    
    category: AnnouncementCategory
    priority: Priority
    
    is_urgent: bool
    is_pinned: bool
    
    created_by: UUID
    created_by_name: str
    
    is_published: bool
    published_at: Optional[datetime]
    
    total_recipients: int
    read_count: int


class AnnouncementDetail(BaseResponseSchema):
    """Detailed announcement"""
    hostel_id: UUID
    hostel_name: str
    
    title: str
    content: str
    category: AnnouncementCategory
    priority: Priority
    
    is_urgent: bool
    is_pinned: bool
    
    # Target audience
    target_audience: str
    target_room_ids: List[UUID]
    target_student_ids: List[UUID]
    target_floor_numbers: List[int]
    
    # Attachments
    attachments: List[str]
    
    # Schedule
    scheduled_publish_at: Optional[datetime]
    published_at: Optional[datetime]
    expires_at: Optional[datetime]
    is_published: bool
    
    # Creation and approval
    created_by: UUID
    created_by_name: str
    created_by_role: str
    
    approved_by: Optional[UUID]
    approved_by_name: Optional[str]
    approved_at: Optional[datetime]
    requires_approval: bool
    
    # Delivery
    send_email: bool
    send_sms: bool
    send_push: bool
    
    email_sent_at: Optional[datetime]
    sms_sent_at: Optional[datetime]
    push_sent_at: Optional[datetime]
    
    # Tracking
    total_recipients: int
    read_count: int
    acknowledged_count: int
    
    # Engagement
    engagement_rate: Decimal = Field(..., description="% who read the announcement")


class AnnouncementList(BaseSchema):
    """List of announcements"""
    hostel_id: Optional[UUID] = None
    
    total_announcements: int
    active_announcements: int
    pinned_announcements: int
    
    announcements: List["AnnouncementListItem"]


class AnnouncementListItem(BaseSchema):
    """Announcement list item"""
    id: UUID
    title: str
    category: str
    priority: str
    
    is_urgent: bool
    is_pinned: bool
    
    created_by_name: str
    published_at: Optional[datetime]
    
    read_count: int
    total_recipients: int
    
    is_read: bool = Field(False, description="For student view")