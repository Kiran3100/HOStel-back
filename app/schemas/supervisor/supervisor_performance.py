"""
Supervisor performance tracking schemas
"""
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional, Dict
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.filters import DateRangeFilter


class PerformanceMetrics(BaseSchema):
    """Supervisor performance metrics"""
    supervisor_id: UUID
    supervisor_name: str
    hostel_id: UUID
    period_start: date
    period_end: date
    
    # Complaint handling
    complaints_handled: int
    complaints_resolved: int
    complaint_resolution_rate: Decimal = Field(..., description="% of complaints resolved")
    average_resolution_time_hours: Decimal
    sla_compliance_rate: Decimal = Field(..., description="% meeting SLA")
    
    # Attendance management
    attendance_records_created: int
    attendance_accuracy: Decimal = Field(..., description="% accuracy (if verified)")
    leaves_approved: int
    leaves_rejected: int
    
    # Maintenance management
    maintenance_requests_created: int
    maintenance_completed: int
    maintenance_completion_rate: Decimal
    average_maintenance_time_hours: Decimal
    
    # Announcements
    announcements_created: int
    announcement_reach: int = Field(..., description="Total students reached")
    
    # Responsiveness
    average_first_response_time_minutes: Decimal
    availability_percentage: Decimal = Field(..., description="% of working hours active")
    
    # Student satisfaction
    student_feedback_score: Optional[Decimal] = Field(
        None,
        ge=0,
        le=5,
        description="Average rating from students"
    )
    
    # Overall rating
    overall_performance_score: Decimal = Field(..., ge=0, le=100, description="Calculated performance score")


class PerformanceReport(BaseSchema):
    """Comprehensive performance report"""
    supervisor_id: UUID
    supervisor_name: str
    hostel_name: str
    report_period: DateRangeFilter
    generated_at: datetime
    
    # Summary metrics
    summary: PerformanceMetrics
    
    # Detailed breakdown
    complaint_performance: "ComplaintPerformance"
    attendance_performance: "AttendancePerformance"
    maintenance_performance: "MaintenancePerformance"
    
    # Trends
    performance_trends: List["PerformanceTrendPoint"]
    
    # Comparisons
    comparison_with_peers: Optional["PeerComparison"] = None
    comparison_with_previous_period: Optional["PeriodComparison"] = None
    
    # Strengths and areas for improvement
    strengths: List[str] = Field(default_factory=list)
    areas_for_improvement: List[str] = Field(default_factory=list)
    
    # Recommendations
    recommendations: List[str] = Field(default_factory=list)


class ComplaintPerformance(BaseSchema):
    """Complaint handling performance details"""
    total_complaints: int
    resolved_complaints: int
    pending_complaints: int
    
    # By category
    complaints_by_category: Dict[str, int]
    
    # By priority
    complaints_by_priority: Dict[str, int]
    
    # Resolution times
    average_resolution_time_hours: Decimal
    fastest_resolution_hours: Decimal
    slowest_resolution_hours: Decimal
    
    # SLA performance
    within_sla: int
    breached_sla: int
    sla_compliance_rate: Decimal
    
    # Student satisfaction
    average_complaint_rating: Optional[Decimal]


class AttendancePerformance(BaseSchema):
    """Attendance management performance"""
    total_attendance_records: int
    days_attendance_marked: int
    days_attendance_missed: int
    
    # Timeliness
    on_time_marking_rate: Decimal = Field(..., description="% of times marked on time")
    average_marking_delay_minutes: Decimal
    
    # Accuracy
    corrections_made: int
    accuracy_rate: Decimal
    
    # Leave management
    leaves_processed: int
    average_leave_approval_time_hours: Decimal


class MaintenancePerformance(BaseSchema):
    """Maintenance management performance"""
    requests_created: int
    requests_completed: int
    requests_pending: int
    
    # By category
    requests_by_category: Dict[str, int]
    
    # Completion time
    average_completion_time_hours: Decimal
    
    # Cost management
    total_maintenance_cost: Decimal
    average_cost_per_request: Decimal
    within_budget_rate: Decimal
    
    # Preventive maintenance
    preventive_tasks_completed: int
    preventive_compliance_rate: Decimal


class PerformanceTrendPoint(BaseSchema):
    """Performance trend data point"""
    period: str = Field(..., description="Time period (e.g., '2024-01' or 'Week 15')")
    overall_score: Decimal
    complaint_score: Decimal
    attendance_score: Decimal
    maintenance_score: Decimal


class PeerComparison(BaseSchema):
    """Comparison with peer supervisors"""
    total_supervisors: int
    rank: int = Field(..., description="Rank among peers (1 = best)")
    percentile: Decimal = Field(..., description="Performance percentile")
    
    # Metric comparisons
    metrics_vs_average: Dict[str, "MetricComparison"]


class MetricComparison(BaseSchema):
    """Individual metric comparison"""
    metric_name: str
    supervisor_value: Decimal
    peer_average: Decimal
    difference_percentage: Decimal
    better_than_average: bool


class PeriodComparison(BaseSchema):
    """Comparison with previous period"""
    previous_period: DateRangeFilter
    current_period: DateRangeFilter
    
    # Overall change
    overall_score_change: Decimal = Field(..., description="% change in overall score")
    
    # Metric changes
    metric_changes: Dict[str, Decimal] = Field(
        ...,
        description="% change for each metric"
    )
    
    # Improvement/decline indicators
    improved_metrics: List[str]
    declined_metrics: List[str]


class PerformanceReview(BaseCreateSchema):
    """Performance review by admin"""
    supervisor_id: UUID = Field(..., description="Supervisor being reviewed")
    review_period: DateRangeFilter = Field(..., description="Review period")
    
    # Ratings (1-5 scale)
    complaint_handling_rating: Decimal = Field(..., ge=1, le=5)
    attendance_management_rating: Decimal = Field(..., ge=1, le=5)
    maintenance_management_rating: Decimal = Field(..., ge=1, le=5)
    communication_rating: Decimal = Field(..., ge=1, le=5)
    professionalism_rating: Decimal = Field(..., ge=1, le=5)
    reliability_rating: Decimal = Field(..., ge=1, le=5)
    
    # Overall rating (calculated or manual)
    overall_rating: Decimal = Field(..., ge=1, le=5)
    
    # Textual feedback
    strengths: str = Field(..., min_length=20, description="Supervisor strengths")
    areas_for_improvement: str = Field(..., min_length=20, description="Areas to improve")
    goals_for_next_period: str = Field(..., description="Goals for next review period")
    
    # Additional comments
    admin_comments: Optional[str] = None
    
    # Action items
    action_items: List[str] = Field(default_factory=list, description="Specific action items")


class PerformanceReviewResponse(BaseSchema):
    """Performance review response"""
    review_id: UUID
    supervisor_id: UUID
    supervisor_name: str
    reviewed_by: UUID
    reviewed_by_name: str
    review_date: date
    
    review_period: DateRangeFilter
    
    # Ratings
    ratings: Dict[str, Decimal]
    overall_rating: Decimal
    
    # Feedback
    strengths: str
    areas_for_improvement: str
    goals_for_next_period: str
    admin_comments: Optional[str]
    
    # Actions
    action_items: List[str]
    
    # Supervisor acknowledgment
    acknowledged: bool = Field(False)
    acknowledged_at: Optional[datetime] = None
    supervisor_comments: Optional[str] = None


class PerformanceGoal(BaseCreateSchema):
    """Set performance goal for supervisor"""
    supervisor_id: UUID
    goal_name: str = Field(..., min_length=5, max_length=255)
    goal_description: str = Field(..., min_length=20)
    
    # Measurable target
    metric_name: str = Field(..., description="Metric to measure (e.g., 'complaint_resolution_rate')")
    target_value: Decimal = Field(..., description="Target value to achieve")
    
    # Timeline
    start_date: date
    end_date: date
    
    # Priority
    priority: str = Field("medium", pattern="^(low|medium|high)$")


class PerformanceGoalProgress(BaseSchema):
    """Track progress on performance goal"""
    goal_id: UUID
    goal_name: str
    metric_name: str
    target_value: Decimal
    current_value: Decimal
    progress_percentage: Decimal
    
    start_date: date
    end_date: date
    days_remaining: int
    
    status: str = Field(
        ...,
        pattern="^(on_track|at_risk|behind|completed|failed)$"
    )
    
    last_updated: datetime