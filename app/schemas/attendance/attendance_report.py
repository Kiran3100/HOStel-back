"""
Attendance reporting schemas
"""
from datetime import date
from decimal import Decimal
from typing import List, Dict, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.filters import DateRangeFilter


class AttendanceReport(BaseSchema):
    """Comprehensive attendance report"""
    hostel_id: Optional[UUID] = None
    student_id: Optional[UUID] = None
    
    report_period: DateRangeFilter
    generated_at: datetime
    
    # Summary
    summary: "AttendanceSummary"
    
    # Detailed records
    daily_records: List["DailyAttendanceRecord"] = Field(default_factory=list)
    
    # Analysis
    trend_analysis: Optional["TrendAnalysis"] = None


class AttendanceSummary(BaseSchema):
    """Attendance summary statistics"""
    total_days: int
    total_present: int
    total_absent: int
    total_late: int
    total_on_leave: int
    total_half_day: int
    
    attendance_percentage: Decimal
    late_percentage: Decimal
    
    # Streaks
    current_present_streak: int
    longest_present_streak: int
    current_absent_streak: int
    
    # Status
    attendance_status: str = Field(
        ...,
        pattern="^(excellent|good|warning|critical)$",
        description="Based on attendance percentage"
    )
    
    meets_minimum_requirement: bool


class DailyAttendanceRecord(BaseSchema):
    """Daily attendance record for report"""
    date: date
    day_of_week: str
    
    status: str
    check_in_time: Optional[time]
    check_out_time: Optional[time]
    
    is_late: bool
    late_minutes: Optional[int]
    
    notes: Optional[str]


class TrendAnalysis(BaseSchema):
    """Attendance trend analysis"""
    period_start: date
    period_end: date
    
    # Weekly trend
    weekly_attendance: List["WeeklyAttendance"]
    
    # Monthly comparison
    monthly_comparison: Optional[List["MonthlyComparison"]] = None
    
    # Patterns
    most_absent_day: Optional[str] = Field(None, description="Day of week with most absences")
    attendance_improving: bool
    improvement_rate: Optional[Decimal] = None


class WeeklyAttendance(BaseSchema):
    """Weekly attendance summary"""
    week_number: int
    week_start_date: date
    week_end_date: date
    
    total_days: int
    present_days: int
    absent_days: int
    
    attendance_percentage: Decimal


class MonthlyComparison(BaseSchema):
    """Monthly attendance comparison"""
    month: str  # YYYY-MM format
    attendance_percentage: Decimal
    total_present: int
    total_absent: int


class MonthlyReport(BaseSchema):
    """Monthly attendance report"""
    hostel_id: UUID
    month: str  # YYYY-MM
    
    # Student-wise summary
    student_summaries: List["StudentMonthlySummary"]
    
    # Hostel-wide stats
    hostel_average_attendance: Decimal
    total_students: int
    students_meeting_requirement: int
    students_below_requirement: int


class StudentMonthlySummary(BaseSchema):
    """Monthly summary for individual student"""
    student_id: UUID
    student_name: str
    room_number: Optional[str]
    
    total_days: int
    present_days: int
    absent_days: int
    late_days: int
    on_leave_days: int
    
    attendance_percentage: Decimal
    meets_requirement: bool
    
    # Actions needed
    requires_attention: bool
    action_required: Optional[str] = None


class AttendanceComparison(BaseSchema):
    """Compare attendance across students/hostels"""
    comparison_type: str = Field(..., pattern="^(student|hostel|room)$")
    period: DateRangeFilter
    
    comparisons: List["ComparisonItem"]


class ComparisonItem(BaseSchema):
    """Individual comparison item"""
    entity_id: UUID
    entity_name: str
    
    attendance_percentage: Decimal
    total_present: int
    total_absent: int
    
    rank: int
    percentile: Decimal