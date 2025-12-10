"""
Bed response schemas
"""
from datetime import date
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import BedStatus


class BedResponse(BaseResponseSchema):
    """Bed response schema"""
    room_id: UUID
    bed_number: str
    is_occupied: bool
    status: BedStatus
    current_student_id: Optional[UUID]
    occupied_from: Optional[date]


class BedAvailability(BaseSchema):
    """Bed availability information"""
    bed_id: UUID
    room_id: UUID
    room_number: str
    bed_number: str
    is_available: bool
    status: BedStatus
    available_from: Optional[date] = Field(None, description="Date when bed becomes available")
    current_student_name: Optional[str] = None


class BedAssignment(BaseResponseSchema):
    """Bed assignment details"""
    bed_id: UUID
    room_id: UUID
    room_number: str
    bed_number: str
    student_id: UUID
    student_name: str
    occupied_from: date
    expected_vacate_date: Optional[date]
    monthly_rent: Decimal


class BedHistory(BaseSchema):
    """Bed occupancy history"""
    bed_id: UUID
    room_number: str
    bed_number: str
    assignments: List["BedAssignmentHistory"]


class BedAssignmentHistory(BaseSchema):
    """Individual bed assignment history"""
    student_id: UUID
    student_name: str
    move_in_date: date
    move_out_date: Optional[date]
    duration_days: Optional[int]