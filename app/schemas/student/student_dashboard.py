"""
Student dashboard schemas
"""
from decimal import Decimal
from datetime import date, datetime
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema


class StudentDashboard(BaseSchema):
    """Student dashboard overview"""
    student_id: UUID
    student_name: str
    
    # Hostel info
    hostel_name: str
    room_number: str
    bed_number: str
    
    # Financial summary
    financial_summary: "StudentFinancialSummary"
    
    # Attendance summary
    attendance_summary: "AttendanceSummary"
    
    # Recent activity
    recent_payments: List["RecentPayment"] = Field(default_factory=list, max_items=5)
    recent_complaints: List["RecentComplaint"] = Field(default_factory=list, max_items=5)
    pending_leave_applications: List["PendingLeave"] = Field(default_factory=list)
    
    # Announcements
    recent_announcements: List["RecentAnnouncement"] = Field(default_factory=list, max_items=5)
    
    # Mess menu
    today_mess_menu: Optional["TodayMessMenu"] = None
    
    # Quick stats
    stats: "StudentStats"


class StudentFinancialSummary(BaseSchema):
    """Financial summary for student"""
    monthly_rent: Decimal
    next_due_date: date
    amount_due: Decimal
    amount_overdue: Decimal
    advance_balance: Decimal
    security_deposit: Decimal
    
    # Mess
    mess_charges: Decimal
    mess_balance: Decimal
    
    # Payment status
    payment_status: str = Field(..., pattern="^(current|due_soon|overdue)$")
    days_until_due: Optional[int]


class AttendanceSummary(BaseSchema):
    """Attendance summary"""
    current_month_percentage: Decimal
    current_month_present: int
    current_month_absent: int
    current_month_leaves: int
    
    last_30_days_percentage: Decimal
    
    # Status
    attendance_status: str = Field(
        ...,
        pattern="^(good|warning|critical)$",
        description="Based on minimum required %"
    )
    
    # Leaves
    leave_balance: int
    pending_leave_requests: int


class StudentStats(BaseSchema):
    """Quick statistics for student"""
    days_in_hostel: int
    total_payments_made: int
    total_amount_paid: Decimal
    complaints_raised: int
    complaints_resolved: int
    current_attendance_percentage: Decimal


class RecentPayment(BaseSchema):
    """Recent payment item"""
    payment_id: UUID
    amount: Decimal
    payment_type: str
    payment_date: date
    status: str
    receipt_url: Optional[str]


class RecentComplaint(BaseSchema):
    """Recent complaint item"""
    complaint_id: UUID
    title: str
    category: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime


class PendingLeave(BaseSchema):
    """Pending leave application"""
    leave_id: UUID
    leave_type: str
    from_date: date
    to_date: date
    total_days: int
    status: str
    applied_at: datetime


class RecentAnnouncement(BaseSchema):
    """Recent announcement"""
    announcement_id: UUID
    title: str
    category: str
    priority: str
    published_at: datetime
    is_read: bool


class TodayMessMenu(BaseSchema):
    """Today's mess menu"""
    date: date
    breakfast: List[str]
    lunch: List[str]
    snacks: List[str]
    dinner: List[str]
    is_special: bool