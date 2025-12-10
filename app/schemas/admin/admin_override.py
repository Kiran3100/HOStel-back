"""
Admin override schemas (for supervisor decisions)
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class AdminOverrideRequest(BaseCreateSchema):
    """Request to override supervisor decision"""
    supervisor_id: Optional[UUID] = Field(None, description="Supervisor whose action is being overridden")
    hostel_id: UUID = Field(..., description="Hostel where override occurs")
    
    override_type: str = Field(
        ...,
        description="Type of override (complaint_reassignment, maintenance_approval, etc.)"
    )
    
    entity_type: str = Field(..., description="Type of entity (complaint, maintenance_request, etc.)")
    entity_id: UUID = Field(..., description="ID of entity being modified")
    
    reason: str = Field(..., min_length=20, max_length=1000, description="Detailed reason for override")
    
    # Original and new values
    original_action: Optional[Dict[str, Any]] = Field(None, description="Original supervisor action")
    override_action: Dict[str, Any] = Field(..., description="Admin's override action")
    
    # Notification
    notify_supervisor: bool = Field(True, description="Notify supervisor of override")


class OverrideLog(BaseResponseSchema):
    """Override log entry"""
    admin_id: UUID
    admin_name: str
    supervisor_id: Optional[UUID]
    supervisor_name: Optional[str]
    
    hostel_id: UUID
    hostel_name: str
    
    override_type: str
    entity_type: str
    entity_id: UUID
    
    reason: str
    
    original_action: Optional[Dict[str, Any]]
    override_action: Dict[str, Any]
    
    created_at: datetime


class OverrideReason(BaseSchema):
    """Predefined override reasons"""
    reason_code: str
    reason_text: str
    category: str
    requires_detailed_explanation: bool


class OverrideSummary(BaseSchema):
    """Summary of admin overrides"""
    admin_id: UUID
    period_start: date
    period_end: date
    
    total_overrides: int
    
    # By type
    overrides_by_type: Dict[str, int]
    
    # By supervisor
    overrides_by_supervisor: Dict[UUID, int]
    
    # By hostel
    overrides_by_hostel: Dict[UUID, int]
    
    # Trend
    override_trend: str = Field(
        ...,
        pattern="^(increasing|decreasing|stable)$",
        description="Override trend"
    )


class SupervisorOverrideStats(BaseSchema):
    """Override statistics for a supervisor"""
    supervisor_id: UUID
    supervisor_name: str
    
    total_actions: int
    total_overrides: int
    override_rate: Decimal = Field(..., description="% of actions overridden")
    
    # By type
    overrides_by_type: Dict[str, int]
    
    # Common reasons
    common_override_reasons: List[str]
    
    # Trend
    recent_trend: str = Field(..., pattern="^(improving|declining|stable)$")