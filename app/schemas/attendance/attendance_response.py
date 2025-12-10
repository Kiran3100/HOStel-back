"""
Attendance response schemas
"""
from datetime import date, time, datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import AttendanceStatus, AttendanceMode


class AttendanceResponse(BaseResponseSchema):
    """Attendance response schema"""
    hostel_id: UUID
    hostel_name: str
    
    student_id: UUID
    student_name: str
    room_number: Optional[str]
    
    attendance_date: date
    check_in_time: Optional[time]
    check_out_time: Optional[time]
    
    status: AttendanceStatus
    is_late: bool
    late_minutes: Optional[int]
    
    marked_by: UUID
    marked_by_name: str


class AttendanceDetail(BaseResponseSchema):
    """Detailed attendance information"""
    hostel_id: UUID
    hostel_name: str
    
    student_id: UUID
    student_name: str
    student_email: str
    student_phone: str
    room_number: Optional[str]
    
    attendance_date: date
    check_in_time: Optional[time]
    check_out_time: Optional[time]
    
    status: AttendanceStatus
    is_late: bool
    late_minutes: Optional[int]
    
    attendance_mode: AttendanceMode
    
    marked_by: UUID
    marked_by_name: str
    supervisor_id: Optional[UUID]
    supervisor_name: Optional[str]
    
    notes: Optional[str]
    
    # Location (if mobile app)
    location_lat: Optional[Decimal]
    location_lng: Optional[Decimal]
    device_info: Optional[dict]
    
    # Metadata
    created_at: datetime
    updated_at: datetime


class AttendanceListItem(BaseSchema):
    """Attendance list item"""
    id: UUID
    student_name: str
    room_number: Optional[str]
    
    attendance_date: date
    status: AttendanceStatus
    
    check_in_time: Optional[time]
    is_late: bool
    
    marked_by_name: str


class DailyAttendanceSummary(BaseSchema):
    """Daily attendance summary"""
    hostel_id: UUID
    hostel_name: str
    date: date
    
    total_students: int
    total_present: int
    total_absent: int
    total_late: int
    total_on_leave: int
    
    attendance_percentage: Decimal
    
    marked_by: UUID
    marked_by_name: str
    marking_completed: bool
    marked_at: Optional[datetime]