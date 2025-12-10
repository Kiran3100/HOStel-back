"""
Attendance filter schemas
"""
from datetime import date
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseFilterSchema
from app.schemas.common.enums import AttendanceStatus
from app.schemas.common.filters import DateRangeFilter


class AttendanceFilterParams(BaseFilterSchema):
    """Attendance filter parameters"""
    # Hostel filter
    hostel_id: Optional[UUID] = None
    hostel_ids: Optional[List[UUID]] = None
    
    # Student filter
    student_id: Optional[UUID] = None
    student_ids: Optional[List[UUID]] = None
    room_id: Optional[UUID] = None
    
    # Date range (required for most queries)
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    
    # Status filter
    status: Optional[AttendanceStatus] = None
    statuses: Optional[List[AttendanceStatus]] = None
    
    # Late filter
    late_only: Optional[bool] = None
    
    # Marked by
    marked_by: Optional[UUID] = None
    supervisor_id: Optional[UUID] = None
    
    # Attendance mode
    attendance_mode: Optional[str] = None


class DateRangeRequest(BaseFilterSchema):
    """Simple date range request"""
    start_date: date = Field(..., description="Start date (inclusive)")
    end_date: date = Field(..., description="End date (inclusive)")
    
    @field_validator('end_date')
    @classmethod
    def validate_date_range(cls, v: date, info) -> date:
        if 'start_date' in info.data and v < info.data['start_date']:
            raise ValueError('end_date must be after or equal to start_date')
        return v


class AttendanceExportRequest(BaseFilterSchema):
    """Export attendance data"""
    hostel_id: UUID
    date_range: DateRangeFilter
    
    # Student filter
    student_ids: Optional[List[UUID]] = None
    
    # Format
    format: str = Field("csv", pattern="^(csv|excel|pdf)$")
    
    # Options
    include_summary: bool = Field(True)
    include_percentage: bool = Field(True)
    include_notes: bool = Field(False)
    group_by: str = Field("student", pattern="^(student|date|room)$")