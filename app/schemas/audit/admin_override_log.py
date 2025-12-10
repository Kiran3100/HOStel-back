"""
Admin override audit log schemas
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class AdminOverrideBase(BaseSchema):
    """
    Base admin override log fields.

    Mirrors `admin_override_logs` table:
    - admin_id
    - supervisor_id (optional)
    - hostel_id
    - override_type
    - entity_type
    - entity_id
    - reason
    - original_action
    - override_action
    - created_at
    """
    admin_id: UUID = Field(..., description="Admin who performed the override")
    supervisor_id: Optional[UUID] = Field(
        None,
        description="Supervisor whose decision was overridden (if applicable)",
    )
    hostel_id: UUID = Field(..., description="Hostel where the override occurred")

    override_type: str = Field(
        ...,
        max_length=100,
        description="Type of override, e.g. 'complaint_reassignment', 'maintenance_approval'",
    )

    entity_type: str = Field(
        ...,
        max_length=50,
        description="Entity type affected, e.g. 'complaint', 'maintenance_request'",
    )
    entity_id: UUID = Field(..., description="Primary key of affected entity")

    reason: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Why the admin override was performed",
    )

    original_action: Optional[Dict[str, Any]] = Field(
        None,
        description="Snapshot of supervisor's original action/decision",
    )
    override_action: Dict[str, Any] = Field(
        ...,
        description="Admin's override decision, details",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when override was recorded",
    )


class AdminOverrideCreate(AdminOverrideBase, BaseCreateSchema):
    """Payload used by services to record a new admin override."""
    pass


class AdminOverrideLogResponse(BaseResponseSchema):
    """
    List item representation of an admin override log.
    Useful for audit tables, supervisor performance review, etc.
    """
    admin_id: UUID
    admin_name: Optional[str] = Field(None, description="Admin display name")

    supervisor_id: Optional[UUID]
    supervisor_name: Optional[str] = Field(None, description="Supervisor display name")

    hostel_id: UUID
    hostel_name: Optional[str] = None

    override_type: str
    entity_type: str
    entity_id: UUID

    reason: str

    created_at: datetime


class AdminOverrideDetail(BaseResponseSchema):
    """
    Detailed view of a single admin override entry,
    including original and override actions.
    """
    admin_id: UUID
    admin_name: Optional[str] = None

    supervisor_id: Optional[UUID]
    supervisor_name: Optional[str] = None

    hostel_id: UUID
    hostel_name: Optional[str] = None

    override_type: str
    entity_type: str
    entity_id: UUID

    reason: str

    original_action: Optional[Dict[str, Any]]
    override_action: Dict[str, Any]

    created_at: datetime


class AdminOverrideSummary(BaseSchema):
    """
    Summary statistics for admin overrides,
    typically for supervisor performance/oversight dashboards.
    """
    period_start: datetime
    period_end: datetime

    # Scope
    supervisor_id: Optional[UUID] = Field(
        None, description="If summarizing overrides for specific supervisor"
    )
    hostel_id: Optional[UUID] = Field(
        None, description="If summarizing for specific hostel"
    )

    # Overall stats
    total_overrides: int = Field(..., ge=0)
    overrides_by_type: Dict[str, int] = Field(
        default_factory=dict,
        description="override_type -> count",
    )
    overrides_by_admin: Dict[UUID, int] = Field(
        default_factory=dict,
        description="admin_id -> count",
    )

    # For supervisor perspective
    override_rate_for_supervisor: Optional[float] = Field(
        None,
        description="For a given supervisor: overridden_actions / total_actions",
    )


class AdminOverrideTimelinePoint(BaseSchema):
    """Time-bucketed view of overrides (e.g., by day/week)."""
    bucket_label: str = Field(..., description="e.g. '2025-01-10' or 'Week 02'")
    override_count: int = Field(..., ge=0)