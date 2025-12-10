"""
Base schemas for audit log entries
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.enums import AuditActionCategory, UserRole


class AuditLogBase(BaseSchema):
    """Base audit log entry schema (read model)"""
    user_id: Optional[UUID] = Field(None, description="Actor user ID (if any)")
    user_role: Optional[UserRole] = Field(None, description="Actor role (if known)")

    action_type: str = Field(..., max_length=100, description="Action type identifier")
    action_category: AuditActionCategory = Field(
        AuditActionCategory.OTHER, description="High-level action category"
    )

    entity_type: Optional[str] = Field(
        None, max_length=50, description="Entity type name (e.g. 'Booking', 'Payment')"
    )
    entity_id: Optional[UUID] = Field(None, description="Primary key of affected entity")

    hostel_id: Optional[UUID] = Field(
        None, description="Hostel context (if applicable)"
    )

    description: str = Field(
        ..., max_length=2000, description="Human-readable description of action"
    )

    old_values: Optional[Dict[str, Any]] = Field(
        None, description="Previous values (for update actions)"
    )
    new_values: Optional[Dict[str, Any]] = Field(
        None, description="New values (for update actions)"
    )

    ip_address: Optional[str] = Field(None, description="IP address (if web/API call)")
    user_agent: Optional[str] = Field(None, description="User-Agent string")
    request_id: Optional[str] = Field(
        None, max_length=100, description="Correlation/request ID (for tracing)"
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)


class AuditLogCreate(AuditLogBase, BaseCreateSchema):
    """Payload used by services to create a new audit log entry"""
    pass