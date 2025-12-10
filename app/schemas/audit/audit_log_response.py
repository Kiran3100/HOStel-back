"""
Audit log response schemas
"""
from typing import Optional, Dict, Any
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema
from app.schemas.common.enums import AuditActionCategory, UserRole


class AuditLogResponse(BaseResponseSchema):
    """Audit log list item"""
    user_id: Optional[UUID]
    user_role: Optional[UserRole]

    action_type: str
    action_category: AuditActionCategory

    entity_type: Optional[str]
    entity_id: Optional[UUID]
    hostel_id: Optional[UUID]

    description: str

    ip_address: Optional[str]
    created_at: datetime


class AuditLogDetail(BaseResponseSchema):
    """Detailed audit log with old/new values"""
    user_id: Optional[UUID]
    user_role: Optional[UserRole]

    action_type: str
    action_category: AuditActionCategory

    entity_type: Optional[str]
    entity_id: Optional[UUID]
    hostel_id: Optional[UUID]

    description: str

    old_values: Optional[Dict[str, Any]]
    new_values: Optional[Dict[str, Any]]

    ip_address: Optional[str]
    user_agent: Optional[str]
    request_id: Optional[str]

    created_at: datetime