"""
Attendance base schemas
"""
from datetime import date, time
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import AttendanceStatus, AttendanceMode


class AttendanceBase(BaseSchema):
    """Base attendance schema"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    student_id: UUID = Field(..., description="Student ID")
    attendance_date: date = Field(..., description="Attendance date")
    
    check_in_time: Optional[time] = Field(None, description="Check-in time")
    check_out_time: Optional[time] = Field(None, description="Check-out time")
    
    status: AttendanceStatus = Field(AttendanceStatus.PRESENT, description="Attendance status")
    
    is_late: bool = Field(False, description="Late arrival")
    late_minutes: Optional[int] = Field(None, ge=0, description="Minutes late")
    
    attendance_mode: AttendanceMode = Field(AttendanceMode.MANUAL, description="How attendance was recorded")
    
    marked_by: UUID = Field(..., description="User who marked attendance (supervisor/admin)")
    supervisor_id: Optional[UUID] = Field(None, description="Supervisor who marked")
    
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")


class AttendanceCreate(AttendanceBase, BaseCreateSchema):
    """Create attendance record"""
    # Location data (for mobile app check-in)
    location_lat: Optional[Decimal] = Field(None, ge=-90, le=90)
    location_lng: Optional[Decimal] = Field(None, ge=-180, le=180)
    
    # Device info (for mobile app)
    device_info: Optional[dict] = None


class AttendanceUpdate(BaseUpdateSchema):
    """Update attendance record"""
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None
    status: Optional[AttendanceStatus] = None
    is_late: Optional[bool] = None
    late_minutes: Optional[int] = None
    notes: Optional[str] = None


class BulkAttendanceCreate(BaseCreateSchema):
    """Bulk create attendance records"""
    hostel_id: UUID
    attendance_date: date
    
    records: List["SingleAttendanceRecord"] = Field(..., min_items=1, max_items=500)
    
    marked_by: UUID
    supervisor_id: Optional[UUID] = None


class SingleAttendanceRecord(BaseSchema):
    """Single attendance in bulk"""
    student_id: UUID
    status: AttendanceStatus = Field(AttendanceStatus.PRESENT)
    check_in_time: Optional[time] = None
    is_late: bool = Field(False)
    notes: Optional[str] = None