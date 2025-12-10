"""
Audit reporting schemas
"""
from datetime import datetime, date
from typing import List, Dict, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.enums import AuditActionCategory, UserRole
from app.schemas.common.filters import DateRangeFilter


class AuditSummary(BaseSchema):
    """High-level summary for audit log report"""
    period: DateRangeFilter
    total_events: int

    # Distribution
    events_by_category: Dict[AuditActionCategory, int] = Field(default_factory=dict)
    events_by_user_role: Dict[UserRole, int] = Field(default_factory=dict)

    # Top actors
    top_users_by_events: List["UserActivitySummary"] = Field(default_factory=list)


class UserActivitySummary(BaseSchema):
    """Aggregate audit activity for one user"""
    user_id: UUID
    user_name: Optional[str] = None
    user_role: Optional[UserRole] = None

    total_events: int
    events_by_category: Dict[AuditActionCategory, int] = Field(default_factory=dict)


class EntityChangeSummary(BaseSchema):
    """Summary of changes for one entity type"""
    entity_type: str
    change_count: int
    last_change_at: datetime


class EntityChangeRecord(BaseSchema):
    """Single change record for history view"""
    log_id: UUID
    action_type: str
    description: str
    old_values: Optional[dict]
    new_values: Optional[dict]
    changed_by: Optional[UUID]
    changed_by_name: Optional[str]
    changed_at: datetime


class EntityChangeHistory(BaseSchema):
    """Complete change history for a specific entity instance"""
    entity_type: str
    entity_id: UUID
    changes: List[EntityChangeRecord] = Field(default_factory=list)


class AuditReport(BaseSchema):
    """Full audit report response"""
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    period: DateRangeFilter

    summary: AuditSummary
    entity_summaries: List[EntityChangeSummary] = Field(default_factory=list)