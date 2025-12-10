"""
Booking room and bed assignment schemas
"""
from datetime import date
from typing import Optional, List
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class RoomAssignment(BaseSchema):
    """Room assignment for booking"""
    booking_id: UUID
    booking_reference: str
    
    hostel_id: UUID
    room_id: UUID
    room_number: str
    room_type: str
    
    assigned_by: UUID
    assigned_by_name: str
    assigned_at: datetime
    
    check_in_date: date


class BedAssignment(BaseSchema):
    """Bed assignment for booking"""
    booking_id: UUID
    booking_reference: str
    
    room_id: UUID
    room_number: str
    bed_id: UUID
    bed_number: str
    
    assigned_by: UUID
    assigned_by_name: str
    assigned_at: datetime


class AssignmentRequest(BaseCreateSchema):
    """Assign room and bed to booking"""
    booking_id: UUID = Field(..., description="Booking ID")
    room_id: UUID = Field(..., description="Room to assign")
    bed_id: UUID = Field(..., description="Bed to assign")
    
    # Override check-in date if needed
    override_check_in_date: Optional[date] = Field(None, description="Override preferred check-in date")
    
    notes: Optional[str] = Field(None, max_length=500, description="Assignment notes")


class BulkAssignmentRequest(BaseCreateSchema):
    """Bulk assign rooms to multiple bookings"""
    assignments: List["SingleAssignment"] = Field(..., min_items=1, description="List of assignments")
    
    auto_approve: bool = Field(False, description="Auto-approve after assignment")


class SingleAssignment(BaseSchema):
    """Single assignment in bulk operation"""
    booking_id: UUID
    room_id: UUID
    bed_id: UUID


class AssignmentResponse(BaseSchema):
    """Assignment response"""
    booking_id: UUID
    booking_reference: str
    
    room_assigned: bool
    room_number: Optional[str]
    bed_number: Optional[str]
    
    message: str
    next_steps: List[str]


class ReassignmentRequest(BaseCreateSchema):
    """Reassign booking to different room/bed"""
    booking_id: UUID
    current_room_id: UUID
    new_room_id: UUID
    new_bed_id: UUID
    
    reason: str = Field(..., min_length=10, max_length=500)
    notify_guest: bool = Field(True)