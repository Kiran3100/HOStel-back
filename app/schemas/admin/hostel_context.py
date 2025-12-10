"""
Hostel context management schemas (for multi-hostel admins)
"""
from datetime import datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class HostelContext(BaseSchema):
    """Current hostel context for admin"""
    admin_id: UUID
    active_hostel_id: UUID
    hostel_name: str
    hostel_city: str
    
    permission_level: str
    
    # Session info
    context_started_at: datetime
    last_accessed_at: datetime
    
    # Quick stats for active hostel
    total_students: int
    occupancy_percentage: Decimal
    pending_tasks: int


class HostelSwitchRequest(BaseCreateSchema):
    """Request to switch active hostel context"""
    hostel_id: UUID = Field(..., description="Hostel ID to switch to")


class ActiveHostelResponse(BaseSchema):
    """Response after switching hostel"""
    admin_id: UUID
    previous_hostel_id: Optional[UUID]
    active_hostel_id: UUID
    hostel_name: str
    
    permission_level: str
    permissions: dict
    
    switched_at: datetime
    message: str = Field(..., description="Success message")


class ContextHistory(BaseSchema):
    """Hostel context switch history"""
    admin_id: UUID
    switches: List["ContextSwitch"]


class ContextSwitch(BaseSchema):
    """Individual context switch record"""
    from_hostel_id: Optional[UUID]
    from_hostel_name: Optional[str]
    to_hostel_id: UUID
    to_hostel_name: str
    switched_at: datetime
    session_duration_minutes: Optional[int] = Field(
        None,
        description="Duration in previous hostel (if applicable)"
    )