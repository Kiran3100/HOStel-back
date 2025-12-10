"""
Attendance alert schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class AttendanceAlert(BaseResponseSchema):
    """Attendance alert"""
    alert_id: UUID
    hostel_id: UUID
    student_id: UUID
    student_name: str
    
    alert_type: str = Field(
        ...,
        pattern="^(low_attendance|consecutive_absences|late_entry|irregular_pattern)$"
    )
    
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    
    # Alert details
    message: str
    details: dict = Field(..., description="Alert-specific details")
    
    # Triggered
    triggered_at: datetime
    triggered_by_rule: Optional[str] = None
    
    # Status
    acknowledged: bool = Field(False)
    acknowledged_by: Optional[UUID] = None
    acknowledged_at: Optional[datetime] = None
    
    # Actions taken
    actions_taken: List[str] = Field(default_factory=list)
    
    resolved: bool = Field(False)
    resolved_at: Optional[datetime] = None


class AlertConfig(BaseSchema):
    """Alert configuration"""
    hostel_id: UUID
    
    # Low attendance alerts
    enable_low_attendance_alerts: bool = Field(True)
    low_attendance_threshold: Decimal = Field(Decimal("75.00"), ge=0, le=100)
    
    # Consecutive absence alerts
    enable_consecutive_absence_alerts: bool = Field(True)
    consecutive_absence_threshold: int = Field(3, ge=1)
    
    # Late entry alerts
    enable_late_entry_alerts: bool = Field(True)
    late_entry_count_threshold: int = Field(5, description="Alert after N late entries in month")
    
    # Pattern detection
    enable_pattern_detection: bool = Field(False, description="Detect irregular patterns")
    
    # Notification settings
    notify_supervisor: bool = Field(True)
    notify_admin: bool = Field(True)
    notify_guardian: bool = Field(True)
    notify_student: bool = Field(True)
    
    # Escalation
    auto_escalate_after_days: int = Field(7, description="Auto-escalate unacknowledged alerts")


class AlertTrigger(BaseSchema):
    """Manual alert trigger"""
    student_id: UUID
    alert_type: str
    custom_message: str = Field(..., min_length=10, max_length=500)
    severity: str = Field("medium", pattern="^(low|medium|high|critical)$")


class AlertAcknowledgment(BaseCreateSchema):
    """Acknowledge alert"""
    alert_id: UUID
    acknowledged_by: UUID
    action_taken: str = Field(..., min_length=10, max_length=500)


class AlertList(BaseSchema):
    """List of alerts"""
    hostel_id: Optional[UUID] = None
    
    total_alerts: int
    unacknowledged_alerts: int
    critical_alerts: int
    
    alerts: List[AttendanceAlert]


class AlertSummary(BaseSchema):
    """Alert summary for dashboard"""
    hostel_id: UUID
    period_start: date
    period_end: date
    
    total_alerts: int
    
    # By type
    low_attendance_alerts: int
    consecutive_absence_alerts: int
    late_entry_alerts: int
    pattern_alerts: int
    
    # By severity
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    
    # Resolution
    acknowledged_count: int
    resolved_count: int
    pending_count: int