# --- File: app/schemas/audit/supervisor_activity_log.py ---
"""
Supervisor activity audit log schemas with enhanced tracking.

Provides comprehensive tracking of supervisor activities including
task management, student interactions, facility oversight, and
performance metrics for accountability and analytics.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Any, Dict, List, Optional
from enum import Enum

from pydantic import Field, field_validator, computed_field, model_validator
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema
from app.schemas.common.filters import DateTimeRangeFilter

__all__ = [
    "SupervisorActionCategory",
    "SupervisorActivityBase",
    "SupervisorActivityCreate",
    "SupervisorActivityLogResponse",
    "SupervisorActivityDetail",
    "SupervisorActivityFilter",
    "SupervisorActivitySummary",
    "SupervisorActivityTimelinePoint",
    "SupervisorPerformanceMetrics",
    "SupervisorShiftReport",
]


class SupervisorActionCategory(str, Enum):
    """Categories of supervisor actions for classification."""
    
    COMPLAINT = "complaint"
    ATTENDANCE = "attendance"
    MAINTENANCE = "maintenance"
    MENU = "menu"
    ANNOUNCEMENT = "announcement"
    STUDENT_MANAGEMENT = "student_management"
    VISITOR_MANAGEMENT = "visitor_management"
    ROOM_INSPECTION = "room_inspection"
    FACILITY_MANAGEMENT = "facility_management"
    EMERGENCY_RESPONSE = "emergency_response"
    DISCIPLINARY = "disciplinary"
    OTHER = "other"


class SupervisorActivityBase(BaseSchema):
    """
    Base fields for supervisor activity log.
    
    Comprehensive tracking of all supervisor actions for
    accountability, performance monitoring, and audit trails.
    """
    
    # Actor
    supervisor_id: UUID = Field(
        ...,
        description="Supervisor performing the action"
    )
    supervisor_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Supervisor name (for display)"
    )
    
    # Context
    hostel_id: UUID = Field(
        ...,
        description="Hostel where action occurred"
    )
    hostel_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Hostel name (for display)"
    )
    
    # Action details
    action_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Specific action identifier (e.g., 'complaint_resolved', 'attendance_marked')"
    )
    action_category: SupervisorActionCategory = Field(
        ...,
        description="High-level category of action"
    )
    action_description: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Human-readable description of the action"
    )
    
    # Entity affected
    entity_type: Optional[str] = Field(
        None,
        max_length=50,
        description="Entity type affected (e.g., 'complaint', 'attendance', 'student')"
    )
    entity_id: Optional[UUID] = Field(
        None,
        description="ID of the entity affected (if applicable)"
    )
    entity_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Display name of affected entity"
    )
    
    # Related entities (for complex actions)
    related_student_id: Optional[UUID] = Field(
        None,
        description="Student involved in the action"
    )
    related_room_id: Optional[UUID] = Field(
        None,
        description="Room involved in the action"
    )
    
    # Action outcome
    status: str = Field(
        "completed",
        pattern="^(completed|pending|failed|cancelled)$",
        description="Status of the action"
    )
    outcome: Optional[str] = Field(
        None,
        max_length=500,
        description="Brief outcome description"
    )
    
    # Additional data
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extra details/context for the action (JSON)"
    )
    
    # Performance metrics
    time_taken_minutes: Optional[int] = Field(
        None,
        ge=0,
        description="Time taken to complete the action (minutes)"
    )
    priority_level: Optional[str] = Field(
        None,
        pattern="^(low|medium|high|urgent|critical)$",
        description="Priority level of the action"
    )
    
    # Request context
    ip_address: Optional[str] = Field(
        None,
        max_length=45,
        description="IP address from which the action originated"
    )
    user_agent: Optional[str] = Field(
        None,
        max_length=500,
        description="User-Agent string from supervisor's device"
    )
    device_type: Optional[str] = Field(
        None,
        pattern="^(mobile|tablet|desktop|other)$",
        description="Device type used"
    )
    
    # Location (for field activities)
    location: Optional[str] = Field(
        None,
        max_length=255,
        description="Physical location where action was performed"
    )
    gps_coordinates: Optional[str] = Field(
        None,
        pattern=r"^-?\d+\.\d+,-?\d+\.\d+$",
        description="GPS coordinates (latitude,longitude)"
    )
    
    # Shift context
    shift_id: Optional[UUID] = Field(
        None,
        description="Shift during which action occurred"
    )
    shift_type: Optional[str] = Field(
        None,
        pattern="^(morning|afternoon|evening|night)$",
        description="Type of shift"
    )
    
    # Timestamp
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the action was logged"
    )
    
    # Quality indicators
    quality_score: Optional[Decimal] = Field(
        None,
        ge=0,
        le=5,
        decimal_places=2,
        description="Quality score for the action (0-5)"
    )
    student_feedback_score: Optional[Decimal] = Field(
        None,
        ge=0,
        le=5,
        decimal_places=2,
        description="Student feedback score (if applicable)"
    )
    
    # Follow-up
    requires_follow_up: bool = Field(
        False,
        description="Whether action requires follow-up"
    )
    follow_up_date: Optional[datetime] = Field(
        None,
        description="When follow-up is due"
    )
    
    @field_validator("time_taken_minutes")
    @classmethod
    def validate_time_taken(cls, v: Optional[int]) -> Optional[int]:
        """Validate time taken is reasonable."""
        if v is not None and v > 1440:  # More than 24 hours
            raise ValueError("time_taken_minutes cannot exceed 1440 (24 hours)")
        return v
    
    @computed_field
    @property
    def efficiency_score(self) -> Optional[Decimal]:
        """
        Calculate efficiency score based on time taken and priority.
        
        Returns:
            Score from 0-100, or None if insufficient data
        """
        if self.time_taken_minutes is None or not self.priority_level:
            return None
        
        # Expected time based on priority
        expected_times = {
            "critical": 15,
            "urgent": 30,
            "high": 60,
            "medium": 120,
            "low": 240,
        }
        
        expected = expected_times.get(self.priority_level, 120)
        
        # Calculate efficiency (100 = exactly on time, >100 = faster, <100 = slower)
        if self.time_taken_minutes == 0:
            return Decimal("100.00")
        
        efficiency = (expected / self.time_taken_minutes) * 100
        return round(Decimal(str(min(100, efficiency))), 2)


class SupervisorActivityCreate(SupervisorActivityBase, BaseCreateSchema):
    """
    Payload for creating new supervisor activity log entries.
    
    Used by services to record supervisor actions throughout
    their shift and activities.
    """
    
    @classmethod
    def for_complaint_action(
        cls,
        supervisor_id: UUID,
        hostel_id: UUID,
        complaint_id: UUID,
        action: str,
        description: str,
        time_taken: Optional[int] = None,
        **kwargs
    ) -> "SupervisorActivityCreate":
        """
        Factory method for complaint-related activities.
        
        Args:
            supervisor_id: Supervisor performing action
            hostel_id: Hostel context
            complaint_id: Complaint being acted upon
            action: Specific action (resolved, assigned, etc.)
            description: Action description
            time_taken: Minutes taken to complete
            **kwargs: Additional fields
            
        Returns:
            SupervisorActivityCreate instance
        """
        return cls(
            supervisor_id=supervisor_id,
            hostel_id=hostel_id,
            action_type=f"complaint.{action}",
            action_category=SupervisorActionCategory.COMPLAINT,
            action_description=description,
            entity_type="complaint",
            entity_id=complaint_id,
            time_taken_minutes=time_taken,
            **kwargs
        )
    
    @classmethod
    def for_attendance_action(
        cls,
        supervisor_id: UUID,
        hostel_id: UUID,
        student_id: UUID,
        action: str,
        description: str,
        **kwargs
    ) -> "SupervisorActivityCreate":
        """
        Factory method for attendance-related activities.
        
        Args:
            supervisor_id: Supervisor performing action
            hostel_id: Hostel context
            student_id: Student whose attendance is recorded
            action: Specific action (marked, verified, etc.)
            description: Action description
            **kwargs: Additional fields
            
        Returns:
            SupervisorActivityCreate instance
        """
        return cls(
            supervisor_id=supervisor_id,
            hostel_id=hostel_id,
            action_type=f"attendance.{action}",
            action_category=SupervisorActionCategory.ATTENDANCE,
            action_description=description,
            entity_type="attendance",
            related_student_id=student_id,
            **kwargs
        )


class SupervisorActivityLogResponse(BaseResponseSchema):
    """
    List item representation of supervisor activity log.
    
    Optimized for tables and activity feeds with essential
    information for quick scanning.
    """
    
    id: UUID = Field(..., description="Activity log entry ID")
    
    # Actor
    supervisor_id: UUID
    supervisor_name: Optional[str] = None
    
    # Context
    hostel_id: UUID
    hostel_name: Optional[str] = None
    
    # Action
    action_type: str
    action_category: SupervisorActionCategory
    action_description: str
    
    # Entity
    entity_type: Optional[str]
    entity_id: Optional[UUID]
    entity_name: Optional[str]
    
    # Status
    status: str
    outcome: Optional[str]
    
    # Metrics
    time_taken_minutes: Optional[int]
    priority_level: Optional[str]
    quality_score: Optional[Decimal]
    
    # Timestamp
    created_at: datetime
    
    # Network
    ip_address: Optional[str]
    device_type: Optional[str]
    
    @computed_field
    @property
    def display_text(self) -> str:
        """Generate display-friendly text."""
        parts = [self.action_description]
        
        if self.time_taken_minutes:
            parts.append(f"({self.time_taken_minutes}m)")
        
        if self.entity_name:
            parts.append(f"- {self.entity_name}")
        
        return " ".join(parts)
    
    @computed_field
    @property
    def status_color(self) -> str:
        """Get color for status badge."""
        colors = {
            "completed": "green",
            "pending": "yellow",
            "failed": "red",
            "cancelled": "gray",
        }
        return colors.get(self.status, "gray")
    
    @computed_field
    @property
    def priority_badge_color(self) -> str:
        """Get color for priority badge."""
        colors = {
            "critical": "red",
            "urgent": "orange",
            "high": "yellow",
            "medium": "blue",
            "low": "gray",
        }
        return colors.get(self.priority_level or "", "gray")


class SupervisorActivityDetail(BaseResponseSchema):
    """
    Detailed view of a single supervisor activity entry.
    
    Includes all fields and metadata for comprehensive
    activity review and investigation.
    """
    
    id: UUID = Field(..., description="Activity log entry ID")
    
    # Actor
    supervisor_id: UUID
    supervisor_name: Optional[str] = None
    supervisor_email: Optional[str] = None
    
    # Context
    hostel_id: UUID
    hostel_name: Optional[str] = None
    
    # Action details
    action_type: str
    action_category: SupervisorActionCategory
    action_description: str
    
    # Entity
    entity_type: Optional[str]
    entity_id: Optional[UUID]
    entity_name: Optional[str]
    
    # Related entities
    related_student_id: Optional[UUID]
    related_student_name: Optional[str]
    related_room_id: Optional[UUID]
    related_room_number: Optional[str]
    
    # Outcome
    status: str
    outcome: Optional[str]
    
    # Metadata
    metadata: Dict[str, Any]
    
    # Performance
    time_taken_minutes: Optional[int]
    priority_level: Optional[str]
    efficiency_score: Optional[Decimal]
    
    # Quality
    quality_score: Optional[Decimal]
    student_feedback_score: Optional[Decimal]
    
    # Request context
    ip_address: Optional[str]
    user_agent: Optional[str]
    device_type: Optional[str]
    
    # Location
    location: Optional[str]
    gps_coordinates: Optional[str]
    
    # Shift context
    shift_id: Optional[UUID]
    shift_type: Optional[str]
    
    # Follow-up
    requires_follow_up: bool
    follow_up_date: Optional[datetime]
    follow_up_completed: Optional[bool] = None
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @computed_field
    @property
    def is_overdue(self) -> bool:
        """Check if follow-up is overdue."""
        if not self.requires_follow_up or not self.follow_up_date:
            return False
        
        if self.follow_up_completed:
            return False
        
        return datetime.utcnow() > self.follow_up_date
    
    @computed_field
    @property
    def performance_rating(self) -> str:
        """Get overall performance rating for this activity."""
        scores = []
        
        if self.efficiency_score:
            scores.append(float(self.efficiency_score))
        
        if self.quality_score:
            scores.append(float(self.quality_score) * 20)  # Scale to 0-100
        
        if self.student_feedback_score:
            scores.append(float(self.student_feedback_score) * 20)
        
        if not scores:
            return "unknown"
        
        avg_score = sum(scores) / len(scores)
        
        if avg_score >= 90:
            return "excellent"
        elif avg_score >= 75:
            return "good"
        elif avg_score >= 60:
            return "satisfactory"
        elif avg_score >= 40:
            return "needs_improvement"
        else:
            return "poor"


class SupervisorActivityFilter(BaseSchema):
    """
    Filter criteria for querying supervisor activity logs.
    
    Provides comprehensive filtering options for activity
    analysis and reporting.
    """
    
    # Actor filters
    supervisor_id: Optional[UUID] = Field(
        None,
        description="Filter by specific supervisor"
    )
    supervisor_ids: Optional[List[UUID]] = Field(
        None,
        max_length=50,
        description="Filter by multiple supervisors"
    )
    
    # Context filters
    hostel_id: Optional[UUID] = Field(
        None,
        description="Filter by hostel"
    )
    hostel_ids: Optional[List[UUID]] = Field(
        None,
        max_length=100,
        description="Filter by multiple hostels"
    )
    
    # Action filters
    action_type: Optional[str] = Field(
        None,
        max_length=100,
        description="Filter by action type"
    )
    action_types: Optional[List[str]] = Field(
        None,
        max_length=50,
        description="Filter by multiple action types"
    )
    action_category: Optional[SupervisorActionCategory] = Field(
        None,
        description="Filter by action category"
    )
    action_categories: Optional[List[SupervisorActionCategory]] = Field(
        None,
        max_length=12,
        description="Filter by multiple categories"
    )
    
    # Entity filters
    entity_type: Optional[str] = Field(
        None,
        max_length=50,
        description="Filter by entity type"
    )
    entity_id: Optional[UUID] = Field(
        None,
        description="Filter by specific entity"
    )
    
    # Related entity filters
    related_student_id: Optional[UUID] = Field(
        None,
        description="Filter by student"
    )
    related_room_id: Optional[UUID] = Field(
        None,
        description="Filter by room"
    )
    
    # Status filters
    status: Optional[str] = Field(
        None,
        pattern="^(completed|pending|failed|cancelled)$",
        description="Filter by status"
    )
    statuses: Optional[List[str]] = Field(
        None,
        max_length=4,
        description="Filter by multiple statuses"
    )
    
    # Priority filters
    priority_level: Optional[str] = Field(
        None,
        pattern="^(low|medium|high|urgent|critical)$",
        description="Filter by priority level"
    )
    min_priority: Optional[str] = Field(
        None,
        description="Minimum priority level"
    )
    
    # Time filters
    datetime_range: Optional[DateTimeRangeFilter] = Field(
        None,
        description="Filter by datetime range"
    )
    created_after: Optional[datetime] = Field(
        None,
        description="Filter activities after this datetime"
    )
    created_before: Optional[datetime] = Field(
        None,
        description="Filter activities before this datetime"
    )
    
    # Quick time filters
    last_hours: Optional[int] = Field(
        None,
        ge=1,
        le=168,  # Max 1 week
        description="Filter activities in last N hours"
    )
    today_only: bool = Field(
        False,
        description="Filter today's activities only"
    )
    
    # Shift filters
    shift_id: Optional[UUID] = Field(
        None,
        description="Filter by shift"
    )
    shift_type: Optional[str] = Field(
        None,
        pattern="^(morning|afternoon|evening|night)$",
        description="Filter by shift type"
    )
    
    # Performance filters
    min_quality_score: Optional[Decimal] = Field(
        None,
        ge=0,
        le=5,
        description="Minimum quality score"
    )
    min_efficiency_score: Optional[Decimal] = Field(
        None,
        ge=0,
        le=100,
        description="Minimum efficiency score"
    )
    
    # Follow-up filters
    requires_follow_up: Optional[bool] = Field(
        None,
        description="Filter by follow-up requirement"
    )
    overdue_follow_ups: bool = Field(
        False,
        description="Show only overdue follow-ups"
    )
    
    # Search
    search_query: Optional[str] = Field(
        None,
        min_length=1,
        max_length=500,
        description="Search in action descriptions"
    )
    
    # Sorting
    sort_by: str = Field(
        "created_at",
        pattern="^(created_at|priority_level|time_taken|quality_score)$",
        description="Field to sort by"
    )
    sort_order: str = Field(
        "desc",
        pattern="^(asc|desc)$",
        description="Sort order"
    )
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(50, ge=1, le=200, description="Items per page")
    
    @model_validator(mode='after')
    def validate_time_filters(self) -> 'SupervisorActivityFilter':
        """Validate time filter combinations."""
        if self.datetime_range and (self.created_after or self.created_before):
            raise ValueError(
                "Cannot use datetime_range with created_after/created_before"
            )
        return self


class SupervisorActivityTimelinePoint(BaseSchema):
    """
    Time-bucketed view of supervisor activities.
    
    Aggregates activities into time buckets for
    timeline visualizations and trend analysis.
    """
    
    bucket_label: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Label for the time bucket (e.g., '2025-01-15', 'Week 12', '14:00-15:00')"
    )
    bucket_start: datetime = Field(
        ...,
        description="Start of the time bucket"
    )
    bucket_end: datetime = Field(
        ...,
        description="End of the time bucket"
    )
    
    # Activity counts
    action_count: int = Field(
        ...,
        ge=0,
        description="Total actions in this bucket"
    )
    completed_count: int = Field(
        0,
        ge=0,
        description="Completed actions"
    )
    pending_count: int = Field(
        0,
        ge=0,
        description="Pending actions"
    )
    failed_count: int = Field(
        0,
        ge=0,
        description="Failed actions"
    )
    
    # By category
    actions_by_category: Dict[str, int] = Field(
        default_factory=dict,
        description="Action count by category"
    )
    
    # Performance metrics
    avg_time_taken_minutes: Optional[Decimal] = Field(
        None,
        ge=0,
        decimal_places=2,
        description="Average time taken for actions"
    )
    avg_quality_score: Optional[Decimal] = Field(
        None,
        ge=0,
        le=5,
        decimal_places=2,
        description="Average quality score"
    )
    
    # Top actions
    top_action_types: List[str] = Field(
        default_factory=list,
        max_length=5,
        description="Top 5 action types in this bucket"
    )
    
    @computed_field
    @property
    def completion_rate(self) -> Decimal:
        """Calculate completion rate for this bucket."""
        if self.action_count == 0:
            return Decimal("100.00")
        return round(
            (Decimal(self.completed_count) / Decimal(self.action_count)) * 100,
            2
        )
    
    @computed_field
    @property
    def workload_intensity(self) -> str:
        """Assess workload intensity."""
        if self.action_count == 0:
            return "idle"
        elif self.action_count <= 5:
            return "light"
        elif self.action_count <= 15:
            return "moderate"
        elif self.action_count <= 30:
            return "heavy"
        else:
            return "very_heavy"


class SupervisorPerformanceMetrics(BaseSchema):
    """
    Performance metrics calculated from supervisor activities.
    
    Provides aggregated performance data for supervisor
    evaluation and recognition.
    """
    
    supervisor_id: UUID
    supervisor_name: Optional[str] = None
    hostel_id: UUID
    hostel_name: Optional[str] = None
    
    period_start: datetime
    period_end: datetime
    
    # Volume metrics
    total_activities: int = Field(..., ge=0)
    total_shifts_worked: int = Field(0, ge=0)
    total_hours_worked: Decimal = Field(
        0,
        ge=0,
        decimal_places=2,
        description="Total hours worked in period"
    )
    
    # Activity distribution
    activities_by_category: Dict[str, int] = Field(default_factory=dict)
    activities_by_priority: Dict[str, int] = Field(default_factory=dict)
    
    # Quality metrics
    avg_quality_score: Decimal = Field(
        0,
        ge=0,
        le=5,
        decimal_places=2,
        description="Average quality score"
    )
    avg_student_feedback: Decimal = Field(
        0,
        ge=0,
        le=5,
        decimal_places=2,
        description="Average student feedback score"
    )
    
    # Efficiency metrics
    avg_time_per_task_minutes: Decimal = Field(
        0,
        ge=0,
        decimal_places=2,
        description="Average time per task"
    )
    avg_efficiency_score: Decimal = Field(
        0,
        ge=0,
        le=100,
        decimal_places=2,
        description="Average efficiency score"
    )
    
    # Completion metrics
    completion_rate: Decimal = Field(
        0,
        ge=0,
        le=100,
        decimal_places=2,
        description="Task completion rate"
    )
    on_time_completion_rate: Decimal = Field(
        0,
        ge=0,
        le=100,
        decimal_places=2,
        description="On-time completion rate"
    )
    
    # Issue resolution
    complaints_handled: int = Field(0, ge=0)
    complaints_resolved: int = Field(0, ge=0)
    avg_complaint_resolution_time_hours: Decimal = Field(
        0,
        ge=0,
        decimal_places=2
    )
    
    # Follow-up tracking
    follow_ups_required: int = Field(0, ge=0)
    follow_ups_completed: int = Field(0, ge=0)
    overdue_follow_ups: int = Field(0, ge=0)
    
    # Attendance tracking
    attendance_records_marked: int = Field(0, ge=0)
    attendance_accuracy_rate: Decimal = Field(
        0,
        ge=0,
        le=100,
        decimal_places=2,
        description="Attendance marking accuracy"
    )
    
    @computed_field
    @property
    def overall_performance_score(self) -> Decimal:
        """
        Calculate overall performance score (0-100).
        
        Weighted combination of multiple metrics.
        """
        weights = {
            "quality": 0.3,
            "efficiency": 0.25,
            "completion": 0.25,
            "feedback": 0.2,
        }
        
        quality_score = float(self.avg_quality_score) * 20  # Scale to 0-100
        efficiency_score = float(self.avg_efficiency_score)
        completion_score = float(self.completion_rate)
        feedback_score = float(self.avg_student_feedback) * 20
        
        score = (
            quality_score * weights["quality"] +
            efficiency_score * weights["efficiency"] +
            completion_score * weights["completion"] +
            feedback_score * weights["feedback"]
        )
        
        return round(Decimal(str(score)), 2)
    
    @computed_field
    @property
    def performance_grade(self) -> str:
        """Get letter grade for performance."""
        score = float(self.overall_performance_score)
        
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    @computed_field
    @property
    def productivity_rate(self) -> Decimal:
        """Calculate tasks per hour worked."""
        if float(self.total_hours_worked) == 0:
            return Decimal("0.00")
        
        rate = self.total_activities / float(self.total_hours_worked)
        return round(Decimal(str(rate)), 2)


class SupervisorActivitySummary(BaseSchema):
    """
    Summary statistics for a supervisor's activity over a period.
    
    Comprehensive overview for performance dashboards and
    supervisor self-assessment.
    """
    
    supervisor_id: UUID
    supervisor_name: Optional[str] = None
    hostel_id: UUID
    hostel_name: Optional[str] = None
    
    period_start: datetime
    period_end: datetime
    
    # Overall stats
    total_actions: int = Field(..., ge=0)
    actions_by_category: Dict[str, int] = Field(
        default_factory=dict,
        description="Category -> count"
    )
    actions_by_type: Dict[str, int] = Field(
        default_factory=dict,
        description="Action type -> count"
    )
    actions_by_status: Dict[str, int] = Field(
        default_factory=dict,
        description="Status -> count"
    )
    
    # Performance metrics
    performance_metrics: Optional[SupervisorPerformanceMetrics] = None
    
    # Timeline
    timeline: List[SupervisorActivityTimelinePoint] = Field(
        default_factory=list,
        description="Activity over time"
    )
    
    # Top actions
    top_action_types: List[Dict[str, Any]] = Field(
        default_factory=list,
        max_length=10,
        description="Top 10 action types by frequency"
    )
    
    # Highlights
    peak_activity_hour: Optional[int] = Field(
        None,
        ge=0,
        le=23,
        description="Hour with most activity"
    )
    peak_activity_day: Optional[str] = Field(
        None,
        description="Day of week with most activity"
    )
    busiest_date: Optional[date] = Field(
        None,
        description="Date with most activities"
    )
    
    # Achievements
    high_quality_actions: int = Field(
        0,
        ge=0,
        description="Actions with quality score >= 4.0"
    )
    quick_resolutions: int = Field(
        0,
        ge=0,
        description="Actions completed in < 30 minutes"
    )
    perfect_days: int = Field(
        0,
        ge=0,
        description="Days with 100% completion rate"
    )
    
    @computed_field
    @property
    def avg_daily_actions(self) -> Decimal:
        """Calculate average actions per day."""
        days = (self.period_end - self.period_start).days + 1
        if days == 0:
            return Decimal("0.00")
        
        return round(Decimal(self.total_actions) / Decimal(days), 2)
    
    @computed_field
    @property
    def most_common_action(self) -> Optional[str]:
        """Identify most common action type."""
        if not self.actions_by_type:
            return None
        return max(self.actions_by_type, key=self.actions_by_type.get)


class SupervisorShiftReport(BaseSchema):
    """
    End-of-shift report for supervisor activities.
    
    Summarizes activities performed during a single shift
    for handover and record-keeping.
    """
    
    shift_id: UUID
    supervisor_id: UUID
    supervisor_name: str
    hostel_id: UUID
    hostel_name: str
    
    # Shift details
    shift_type: str = Field(
        ...,
        pattern="^(morning|afternoon|evening|night)$"
    )
    shift_start: datetime
    shift_end: datetime
    shift_duration_hours: Decimal = Field(..., ge=0, decimal_places=2)
    
    # Activities
    total_activities: int = Field(..., ge=0)
    activities_by_category: Dict[str, int] = Field(default_factory=dict)
    completed_activities: int = Field(..., ge=0)
    pending_activities: int = Field(..., ge=0)
    
    # Detailed activity list
    activities: List[SupervisorActivityLogResponse] = Field(
        default_factory=list,
        description="All activities during shift"
    )
    
    # Key events
    critical_incidents: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Critical incidents during shift"
    )
    
    # Handover notes
    handover_notes: Optional[str] = Field(
        None,
        max_length=2000,
        description="Notes for next shift"
    )
    pending_tasks: List[str] = Field(
        default_factory=list,
        description="Tasks to be completed by next shift"
    )
    
    # Performance
    shift_performance_score: Decimal = Field(
        ...,
        ge=0,
        le=100,
        decimal_places=2
    )
    
    # Generated metadata
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @computed_field
    @property
    def productivity_rate(self) -> Decimal:
        """Calculate activities per hour."""
        if float(self.shift_duration_hours) == 0:
            return Decimal("0.00")
        
        rate = self.total_activities / float(self.shift_duration_hours)
        return round(Decimal(str(rate)), 2)
    
    @computed_field
    @property
    def completion_rate(self) -> Decimal:
        """Calculate completion rate."""
        if self.total_activities == 0:
            return Decimal("100.00")
        
        return round(
            (Decimal(self.completed_activities) / Decimal(self.total_activities)) * 100,
            2
        )