"""
Booking waitlist schemas
"""
from datetime import date, datetime
from typing import Optional
from pydantic import Field, EmailStr
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema
from app.schemas.common.enums import RoomType, WaitlistStatus


class WaitlistRequest(BaseCreateSchema):
    """Add to waitlist when hostel is full"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    visitor_id: UUID = Field(..., description="Visitor ID")
    
    room_type: RoomType = Field(..., description="Desired room type")
    preferred_check_in_date: date = Field(..., description="Desired check-in date")
    
    # Contact
    contact_email: EmailStr = Field(..., description="Email for notifications")
    contact_phone: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$')
    
    # Additional info
    notes: Optional[str] = Field(None, max_length=500)


class WaitlistResponse(BaseResponseSchema):
    """Waitlist entry response"""
    hostel_id: UUID
    hostel_name: str
    visitor_id: UUID
    
    room_type: RoomType
    preferred_check_in_date: date
    
    contact_email: str
    contact_phone: str
    
    priority: int = Field(..., description="Position in waitlist (1 = first)")
    status: WaitlistStatus
    
    estimated_availability_date: Optional[date] = Field(
        None,
        description="Estimated date when room might be available"
    )
    
    created_at: datetime


class WaitlistStatus(BaseSchema):
    """Waitlist status for visitor"""
    waitlist_id: UUID
    hostel_name: str
    room_type: str
    
    position: int = Field(..., description="Current position in queue")
    total_in_queue: int
    
    status: str = Field(..., pattern="^(waiting|notified|converted|expired|cancelled)$")
    
    # Notifications
    last_notification_sent: Optional[datetime]
    notification_count: int
    
    # Estimated wait
    estimated_wait_days: Optional[int]


class WaitlistNotification(BaseSchema):
    """Notification when room becomes available"""
    waitlist_id: UUID
    visitor_id: UUID
    hostel_id: UUID
    
    message: str
    available_room_id: UUID
    available_bed_id: UUID
    
    # Action required
    response_deadline: datetime = Field(..., description="Deadline to respond")
    
    # Booking link
    booking_link: str


class WaitlistConversion(BaseCreateSchema):
    """Convert waitlist to booking"""
    waitlist_id: UUID
    accept: bool = Field(..., description="Accept the available room")
    
    # If accepting
    proceed_with_booking: bool = Field(True)


class WaitlistCancellation(BaseCreateSchema):
    """Remove from waitlist"""
    waitlist_id: UUID
    cancellation_reason: Optional[str] = Field(None, max_length=500)


class WaitlistManagement(BaseSchema):
    """Manage waitlist (admin)"""
    hostel_id: UUID
    room_type: RoomType
    
    total_in_waitlist: int
    entries: List["WaitlistEntry"]


class WaitlistEntry(BaseSchema):
    """Individual waitlist entry"""
    waitlist_id: UUID
    visitor_name: str
    contact_email: str
    contact_phone: str
    
    preferred_check_in_date: date
    priority: int
    status: WaitlistStatus
    
    days_waiting: int
    created_at: datetime