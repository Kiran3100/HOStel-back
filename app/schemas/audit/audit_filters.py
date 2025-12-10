"""
Audit log filtering schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseFilterSchema
from app.schemas.common.enums import AuditActionCategory, UserRole
from app.schemas.common.filters import DateTimeRangeFilter


class AuditFilterParams(BaseFilterSchema):
    """Filter criteria for querying audit logs"""
    # Actor
    user_id: Optional[UUID] = None
    user_role: Optional[UserRole] = None

    # Hostel
    hostel_id: Optional[UUID] = None

    # Entity
    entity_type: Optional[str] = Field(None, max_length=50)
    entity_id: Optional[UUID] = None

    # Action
    action_type: Optional[str] = Field(None, max_length=100)
    action_category: Optional[AuditActionCategory] = None

    # Time range
    datetime_range: Optional[DateTimeRangeFilter] = None

    # Request ID
    request_id: Optional[str] = None

    # Paging
    page: int = Field(1, ge=1)
    page_size: int = Field(50, ge=1, le=200)