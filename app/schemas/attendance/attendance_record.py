"""
Attendance recording schemas
"""
from datetime import date, time
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.enums import AttendanceStatus


class AttendanceRecordRequest(BaseCreateSchema):
    """Record attendance for single student"""
    hostel_id: UUID
    student_id: UUID
    attendance_date: date
    
    status: AttendanceStatus = Field(AttendanceStatus.PRESENT)
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None
    
    is_late: bool = Field(False)
    notes: Optional[str] = Field(None, max_length=500)


class BulkAttendanceRequest(BaseCreateSchema):
    """Mark attendance for multiple students at once"""
    hostel_id: UUID
    attendance_date: date
    
    # Default status for all (can be overridden per student)
    default_status: AttendanceStatus = Field(AttendanceStatus.PRESENT)
    
    # Student-specific records
    student_records: List["StudentAttendanceRecord"] = Field(..., min_items=1)
    
    # Metadata
    marked_by: UUID
    marking_mode: str = Field("manual", pattern="^(manual|biometric|qr_code|mobile_app)$")


class StudentAttendanceRecord(BaseSchema):
    """Individual student attendance in bulk operation"""
    student_id: UUID
    status: Optional[AttendanceStatus] = None  # If None, uses default_status
    check_in_time: Optional[time] = None
    is_late: Optional[bool] = None
    notes: Optional[str] = None


class AttendanceCorrection(BaseCreateSchema):
    """Correct previously marked attendance"""
    attendance_id: UUID
    
    # Corrected values
    corrected_status: AttendanceStatus
    corrected_check_in_time: Optional[time] = None
    corrected_check_out_time: Optional[time] = None
    
    correction_reason: str = Field(..., min_length=10, max_length=500)
    corrected_by: UUID


class QuickAttendanceMarkAll(BaseCreateSchema):
    """Quick mark all students as present"""
    hostel_id: UUID
    attendance_date: date
    
    # Exceptions
    absent_student_ids: List[UUID] = Field(default_factory=list)
    on_leave_student_ids: List[UUID] = Field(default_factory=list)
    
    marked_by: UUID