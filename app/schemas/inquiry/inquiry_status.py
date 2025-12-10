"""
Inquiry status change & assignment schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema
from app.schemas.common.enums import InquiryStatus


class InquiryStatusUpdate(BaseCreateSchema):
    """Update inquiry status"""
    inquiry_id: UUID
    new_status: InquiryStatus
    notes: Optional[str] = Field(None, max_length=500)


class InquiryAssignment(BaseCreateSchema):
    """Assign inquiry to an admin/staff"""
    inquiry_id: UUID
    assigned_to: UUID
    assigned_by: UUID

    assignment_notes: Optional[str] = Field(None, max_length=500)


class InquiryTimelineEntry(BaseSchema):
    """Timeline record for inquiry lifetime"""
    status: InquiryStatus
    timestamp: datetime
    changed_by: Optional[UUID]
    notes: Optional[str]