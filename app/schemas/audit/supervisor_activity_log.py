"""
Supervisor activity audit log schemas
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema
from app.schemas.common.filters import DateTimeRangeFilter


class SupervisorActivityBase(BaseSchema):
    """
    Base fields for supervisor activity log.

    Mirrors the `supervisor_activity_logs` table:
    - supervisor_id
    - hostel_id
    - action_type
    - action_category
    - entity_type / entity_id
    - action_description
    - metadata
    - ip_address
    - user_agent
    - created_at
    """
    supervisor_id: UUID = Field(..., description="Supervisor performing the action")
    hostel_id: UUID = Field(..., description="Hostel where action occurred")

    action_type: str = Field(
        ...,
        max_length=100,
        description="Action identifier, e.g. 'complaint_resolved', 'attendance_marked'",
    )
    action_category: str = Field(
        ...,
        pattern=(
            r"^(complaint|attendance|maintenance|menu|announcement|"
            r"student_management|other)$"
        ),
        description="High-level category of action",
    )

    entity_type: Optional[str] = Field(
        None, max_length=50, description="Entity type, e.g. 'complaint', 'attendance'"
    )
    entity_id: Optional[UUID] = Field(
        None, description="ID of the entity affected (if applicable)"
    )

    action_description: str = Field(
        ...,
        max_length=2000,
        description="Human-readable description of the action",
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extra details/context for the action (JSON)",
    )

    ip_address: Optional[str] = Field(
        None,
        description="IP address from which the action originated (if tracked)",
    )
    user_agent: Optional[str] = Field(
        None,
        description="User-Agent string from supervisor's device (if tracked)",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the action was logged",
    )


class SupervisorActivityCreate(SupervisorActivityBase, BaseCreateSchema):
    """Used by services to record a new supervisor activity log entry."""
    pass


class SupervisorActivityLogResponse(BaseResponseSchema):
    """
    List item representation of supervisor activity log.
    Suitable for tables or basic activity feeds.
    """
    supervisor_id: UUID
    supervisor_name: Optional[str] = Field(
        None, description="Supervisor display name (if joined in query)"
    )
    hostel_id: UUID
    hostel_name: Optional[str] = Field(
        None, description="Hostel display name (if joined in query)"
    )

    action_type: str
    action_category: str

    entity_type: Optional[str]
    entity_id: Optional[UUID]

    action_description: str

    created_at: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]


class SupervisorActivityDetail(BaseResponseSchema):
    """
    Detailed view of a single supervisor activity entry,
    including full metadata.
    """
    supervisor_id: UUID
    supervisor_name: Optional[str] = None
    hostel_id: UUID
    hostel_name: Optional[str] = None

    action_type: str
    action_category: str

    entity_type: Optional[str]
    entity_id: Optional[UUID]

    action_description: str
    metadata: Dict[str, Any]

    ip_address: Optional[str]
    user_agent: Optional[str]
    created_at: datetime


class SupervisorActivityFilter(BaseSchema):
    """
    Filter criteria for querying supervisor activity logs.
    Typically used as a body/query schema for list endpoints.
    """
    supervisor_id: Optional[UUID] = None
    hostel_id: Optional[UUID] = None

    action_type: Optional[str] = Field(None, max_length=100)
    action_category: Optional[str] = Field(
        None,
        pattern=(
            r"^(complaint|attendance|maintenance|menu|announcement|"
            r"student_management|other)$"
        ),
    )

    entity_type: Optional[str] = Field(None, max_length=50)
    entity_id: Optional[UUID] = None

    datetime_range: Optional[DateTimeRangeFilter] = None

    # Pagination
    page: int = Field(1, ge=1)
    page_size: int = Field(50, ge=1, le=200)


class SupervisorActivitySummary(BaseSchema):
    """
    Summary statistics for a supervisor's activity over a period.
    Useful for performance dashboards.
    """
    supervisor_id: UUID
    supervisor_name: Optional[str] = None
    hostel_id: UUID
    hostel_name: Optional[str] = None

    period_start: datetime
    period_end: datetime

    total_actions: int
    actions_by_category: Dict[str, int] = Field(
        default_factory=dict,
        description="Category -> count",
    )
    actions_by_type: Dict[str, int] = Field(
        default_factory=dict,
        description="Action type -> count",
    )

    # For trending / charts (optional)
    timeline: List["SupervisorActivityTimelinePoint"] = Field(
        default_factory=list,
        description="Activity over time",
    )


class SupervisorActivityTimelinePoint(BaseSchema):
    """Time-bucketed count of supervisor actions (e.g., daily/weekly)."""
    bucket_label: str = Field(
        ...,
        description="Label for the time bucket (e.g. '2025-01-15', 'Week 12')",
    )
    action_count: int = Field(..., ge=0)