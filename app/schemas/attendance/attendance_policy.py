"""
Attendance policy schemas
"""
from datetime import time
from decimal import Decimal
from typing import Optional
from pydantic import Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseUpdateSchema, BaseResponseSchema


class AttendancePolicy(BaseResponseSchema):
    """Attendance policy configuration"""
    hostel_id: UUID
    hostel_name: str
    
    # Minimum requirements
    minimum_attendance_percentage: Decimal = Field(..., ge=0, le=100)
    
    # Late entry
    late_entry_threshold_minutes: int = Field(..., ge=0, description="Minutes after which marked as late")
    grace_days_per_month: int = Field(..., ge=0, description="Allowed late entries per month")
    
    # Absence alerts
    consecutive_absence_alert_days: int = Field(..., description="Alert after N consecutive absences")
    
    # Notifications
    notify_guardian_on_absence: bool = Field(True)
    notify_admin_on_low_attendance: bool = Field(True)
    low_attendance_threshold: Decimal = Field(Decimal("75.00"), ge=0, le=100)
    
    # Auto-marking
    auto_mark_absent_after_time: Optional[time] = Field(None, description="Auto mark absent if not checked in by this time")
    
    is_active: bool = Field(True)


class PolicyConfig(BaseSchema):
    """Policy configuration details"""
    # Attendance calculation
    calculation_period: str = Field("monthly", pattern="^(weekly|monthly|semester|yearly)$")
    
    # Leave handling
    count_leave_as_absent: bool = Field(False, description="Count approved leaves as absent")
    max_leaves_per_month: int = Field(3, ge=0)
    
    # Weekends
    include_weekends: bool = Field(False, description="Track attendance on weekends")
    weekend_days: List[str] = Field(default_factory=lambda: ["Saturday", "Sunday"])
    
    # Holidays
    exclude_holidays: bool = Field(True)
    
    # Penalties
    low_attendance_penalty: Optional[str] = None


class PolicyUpdate(BaseUpdateSchema):
    """Update attendance policy"""
    minimum_attendance_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    late_entry_threshold_minutes: Optional[int] = Field(None, ge=0)
    grace_days_per_month: Optional[int] = Field(None, ge=0)
    consecutive_absence_alert_days: Optional[int] = None
    
    notify_guardian_on_absence: Optional[bool] = None
    notify_admin_on_low_attendance: Optional[bool] = None
    low_attendance_threshold: Optional[Decimal] = Field(None, ge=0, le=100)
    
    auto_mark_absent_after_time: Optional[time] = None
    is_active: Optional[bool] = None


class PolicyViolation(BaseSchema):
    """Policy violation record"""
    student_id: UUID
    student_name: str
    hostel_id: UUID
    
    violation_type: str = Field(
        ...,
        pattern="^(low_attendance|consecutive_absences|excessive_late_entries)$"
    )
    
    # Details
    current_attendance_percentage: Optional[Decimal] = None
    consecutive_absences: Optional[int] = None
    late_entries_this_month: Optional[int] = None
    
    violation_date: date
    
    # Actions taken
    guardian_notified: bool
    admin_notified: bool
    warning_issued: bool
    
    notes: Optional[str] = None