"""
Subscription cancellation schemas
"""
from datetime import date, datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema


class CancellationRequest(BaseCreateSchema):
    """Cancel subscription"""
    subscription_id: UUID
    hostel_id: UUID

    cancellation_reason: str = Field(..., min_length=10, max_length=500)
    cancel_immediately: bool = Field(False, description="Cancel now vs at end of term")


class CancellationResponse(BaseSchema):
    """Cancellation response"""
    subscription_id: UUID
    hostel_id: UUID

    cancelled: bool
    cancellation_effective_date: date
    cancelled_at: datetime
    cancelled_by: UUID

    message: str