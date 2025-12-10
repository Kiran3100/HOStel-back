"""
Supervisor activity and audit log schemas
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseResponseSchema, BaseFilterSchema
from app.schemas.common.enums import AuditActionCategory
from app.schemas.common.filters import DateTimeRangeFilter


class SupervisorActivityLog(BaseResponseSchema):
    """Supervisor activity log entry"""
    supervisor_id: UUID
    supervisor_name: str
    hostel_id: UUID
    hostel_name: str
    
    action_type: str = Field(..., description="Type of action performed")
    action_category: AuditActionCategory = Field(..., description="Action category")
    
    entity_type: Optional[str] = Field(None, description="Type of entity affected")
    entity_id: Optional[UUID] = Field(None, description="ID of affected entity")
    
    action_description: str = Field(..., description="Human-readable description")
    
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional action details")
    
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class ActivityDetail(BaseSchema):
    """Detailed activity information"""
    activity_id: UUID
    supervisor_id: UUID
    supervisor_name: str
    
    timestamp: datetime
    action_type: str
    action_category: AuditActionCategory
    action_description: str
    
    # Entity details
    entity_type: Optional[str]
    entity_id: Optional[UUID]
    entity_name: Optional[str]
    
    # Changes made
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    
    # Context
    ip_address: Optional[str]
    user_agent: Optional[str]
    location: Optional[str]
    
    # Result
    success: bool = Field(True, description="Whether action succeeded")
    error_message: Optional[str] = None


class ActivitySummary(BaseSchema):
    """Activity summary for supervisor"""
    supervisor_id: UUID
    supervisor_name: str
    period_start: datetime
    period_end: datetime
    
    total_actions: int
    
    # By category
    actions_by_category: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of actions by category"
    )
    
    # By type
    actions_by_type: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of actions by type"
    )
    
    # Top activities
    top_activities: List["TopActivity"] = Field(
        default_factory=list,
        description="Most frequent activities"
    )
    
    # Activity timeline
    activity_timeline: List["ActivityTimelinePoint"] = Field(
        default_factory=list,
        description="Activity over time"
    )
    
    # Peak activity times
    peak_hours: List[int] = Field(
        default_factory=list,
        description="Hours with most activity (0-23)"
    )


class TopActivity(BaseSchema):
    """Top activity item"""
    action_type: str
    action_category: str
    count: int
    last_performed: datetime


class ActivityTimelinePoint(BaseSchema):
    """Activity timeline data point"""
    timestamp: datetime
    action_count: int
    categories: Dict[str, int]


class ActivityFilterParams(BaseFilterSchema):
    """Filter parameters for activity logs"""
    # Supervisor filter
    supervisor_id: Optional[UUID] = None
    supervisor_ids: Optional[List[UUID]] = None
    
    # Hostel filter
    hostel_id: Optional[UUID] = None
    
    # Time range
    date_range: Optional[DateTimeRangeFilter] = None
    
    # Action filters
    action_category: Optional[AuditActionCategory] = None
    action_categories: Optional[List[AuditActionCategory]] = None
    action_type: Optional[str] = None
    
    # Entity filter
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    
    # Success filter
    success_only: Optional[bool] = None
    failed_only: Optional[bool] = None
    
    # Pagination
    page: int = Field(1, ge=1)
    page_size: int = Field(50, ge=1, le=100)


class ActivityExportRequest(BaseSchema):
    """Export activity logs"""
    filters: ActivityFilterParams = Field(..., description="Filter criteria")
    format: str = Field("csv", pattern="^(csv|excel|pdf|json)$")
    include_metadata: bool = Field(False, description="Include full metadata")