"""
Announcement scheduling schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class ScheduleRequest(BaseCreateSchema):
    """Schedule announcement for later"""
    announcement_id: UUID
    
    scheduled_publish_at: datetime = Field(..., description="When to publish")
    
    # Auto-expire
    auto_expire: bool = Field(False)
    expire_after_hours: Optional[int] = Field(None, ge=1, le=720, description="Expire after N hours")
    
    @field_validator('scheduled_publish_at')
    @classmethod
    def validate_future_time(cls, v: datetime) -> datetime:
        """Ensure scheduled time is in future"""
        from datetime import datetime as dt
        if v <= dt.now():
            raise ValueError('Scheduled time must be in the future')
        return v


class ScheduleConfig(BaseSchema):
    """Schedule configuration"""
    announcement_id: UUID
    
    is_scheduled: bool
    scheduled_publish_at: Optional[datetime]
    
    # Recurrence
    is_recurring: bool = Field(False)
    recurrence_pattern: Optional[str] = Field(None, description="daily, weekly, monthly")
    
    # End condition
    recurrence_end_date: Optional[datetime] = None
    max_occurrences: Optional[int] = Field(None, ge=1)


class RecurringAnnouncement(BaseCreateSchema):
    """Create recurring announcement"""
    hostel_id: UUID
    
    title: str = Field(..., min_length=5, max_length=255)
    content: str = Field(..., min_length=10, max_length=5000)
    
    # Recurrence
    recurrence_pattern: str = Field(..., pattern="^(daily|weekly|monthly)$")
    start_date: datetime
    
    # End condition
    end_date: Optional[datetime] = None
    max_occurrences: Optional[int] = None
    
    # Days (for weekly)
    weekdays: Optional[List[int]] = Field(None, description="0=Monday, 6=Sunday")
    
    # Time
    publish_time: str = Field(..., description="HH:MM format")
    
    # Targeting
    target_audience: str
    target_room_ids: List[UUID] = Field(default_factory=list)


class ScheduleUpdate(BaseCreateSchema):
    """Update scheduled announcement"""
    announcement_id: UUID
    
    new_scheduled_time: datetime
    
    reason: Optional[str] = Field(None, max_length=500, description="Reason for rescheduling")


class ScheduleCancel(BaseCreateSchema):
    """Cancel scheduled announcement"""
    announcement_id: UUID
    
    cancellation_reason: str = Field(..., min_length=10, max_length=500)
    
    # Whether to delete or just unpublish
    delete_announcement: bool = Field(False)


class PublishNow(BaseCreateSchema):
    """Publish scheduled announcement immediately"""
    announcement_id: UUID
    
    override_schedule: bool = Field(True)


class ScheduledAnnouncementsList(BaseSchema):
    """List of scheduled announcements"""
    hostel_id: UUID
    
    total_scheduled: int
    upcoming_24h: int
    
    announcements: List["ScheduledAnnouncementItem"]


class ScheduledAnnouncementItem(BaseSchema):
    """Scheduled announcement item"""
    announcement_id: UUID
    title: str
    scheduled_for: datetime
    
    is_recurring: bool
    next_occurrence: Optional[datetime]
    
    target_audience: str
    estimated_recipients: int