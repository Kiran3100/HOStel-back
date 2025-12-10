"""
Supervisor dashboard schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema


class SupervisorDashboard(BaseSchema):
    """Supervisor dashboard overview"""
    supervisor_id: UUID
    supervisor_name: str
    hostel_id: UUID
    hostel_name: str
    
    # Metrics
    metrics: "DashboardMetrics"
    
    # Tasks
    tasks: "TaskSummary"
    
    # Recent activity
    recent_complaints: List["RecentComplaintItem"] = Field(default_factory=list, max_items=5)
    recent_maintenance: List["RecentMaintenanceItem"] = Field(default_factory=list, max_items=5)
    pending_leaves: List["PendingLeaveItem"] = Field(default_factory=list, max_items=5)
    
    # Today's schedule
    today_schedule: "TodaySchedule"
    
    # Alerts
    alerts: List["DashboardAlert"] = Field(default_factory=list)
    
    # Quick stats
    last_login: Optional[datetime]
    actions_today: int


class DashboardMetrics(BaseSchema):
    """Dashboard key metrics"""
    # Students
    total_students: int
    active_students: int
    
    # Occupancy
    total_beds: int
    occupied_beds: int
    available_beds: int
    occupancy_percentage: Decimal
    
    # Complaints
    total_complaints: int
    open_complaints: int
    assigned_to_me: int
    resolved_today: int
    average_resolution_time_hours: Decimal
    
    # Maintenance
    pending_maintenance: int
    in_progress_maintenance: int
    completed_today: int
    
    # Attendance
    attendance_marked_today: bool
    total_present_today: int
    total_absent_today: int
    students_on_leave: int
    
    # Payments (view only)
    overdue_payments_count: int
    
    # Announcements
    unread_admin_messages: int


class TaskSummary(BaseSchema):
    """Summary of pending tasks"""
    # High priority tasks
    urgent_complaints: int
    critical_maintenance: int
    pending_leave_approvals: int
    
    # Daily tasks
    attendance_pending: bool
    menu_published_today: bool
    daily_inspection_done: bool
    
    # Overdue tasks
    overdue_complaint_resolutions: int
    overdue_maintenance: int
    
    # Total pending
    total_pending_tasks: int


class RecentComplaintItem(BaseSchema):
    """Recent complaint item for dashboard"""
    complaint_id: UUID
    complaint_number: str
    title: str
    category: str
    priority: str
    status: str
    student_name: str
    room_number: str
    created_at: datetime
    age_hours: int


class RecentMaintenanceItem(BaseSchema):
    """Recent maintenance item for dashboard"""
    request_id: UUID
    request_number: str
    title: str
    category: str
    priority: str
    status: str
    room_number: Optional[str]
    estimated_cost: Optional[Decimal]
    created_at: datetime


class PendingLeaveItem(BaseSchema):
    """Pending leave approval"""
    leave_id: UUID
    student_name: str
    room_number: str
    leave_type: str
    from_date: date
    to_date: date
    total_days: int
    reason: str
    applied_at: datetime


class TodaySchedule(BaseSchema):
    """Today's schedule for supervisor"""
    date: date
    
    # Routine tasks
    attendance_marking_time: str = Field(..., description="Expected time for attendance")
    inspection_rounds: List[str] = Field(default_factory=list, description="Scheduled inspection areas")
    
    # Scheduled maintenance
    scheduled_maintenance: List["ScheduledMaintenanceItem"] = Field(default_factory=list)
    
    # Meetings
    scheduled_meetings: List["ScheduledMeeting"] = Field(default_factory=list)
    
    # Special events
    special_events: List[str] = Field(default_factory=list)


class ScheduledMaintenanceItem(BaseSchema):
    """Scheduled maintenance for today"""
    maintenance_id: UUID
    title: str
    scheduled_time: str
    room_number: Optional[str]
    assigned_staff: Optional[str]


class ScheduledMeeting(BaseSchema):
    """Scheduled meeting"""
    meeting_id: UUID
    title: str
    time: str
    attendees: List[str]
    location: str


class DashboardAlert(BaseSchema):
    """Dashboard alert/notification"""
    alert_id: UUID
    alert_type: str = Field(
        ...,
        pattern="^(urgent|warning|info)$",
        description="Alert severity"
    )
    title: str
    message: str
    action_required: bool
    action_url: Optional[str]
    created_at: datetime


class QuickActions(BaseSchema):
    """Quick action buttons for dashboard"""
    actions: List["QuickAction"]


class QuickAction(BaseSchema):
    """Individual quick action"""
    action_id: str
    label: str
    icon: str
    url: str
    badge_count: Optional[int] = Field(None, description="Number indicator (e.g., pending items)")