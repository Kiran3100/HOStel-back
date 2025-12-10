"""
Booking modification schemas
"""
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.enums import RoomType


class ModificationRequest(BaseCreateSchema):
    """Request to modify booking"""
    booking_id: UUID = Field(..., description="Booking ID")
    
    # What to modify
    modify_check_in_date: bool = Field(False)
    new_check_in_date: Optional[date] = None
    
    modify_duration: bool = Field(False)
    new_duration_months: Optional[int] = Field(None, ge=1, le=24)
    
    modify_room_type: bool = Field(False)
    new_room_type: Optional[RoomType] = None
    
    # Reason
    modification_reason: str = Field(..., min_length=10, max_length=500)
    
    # Accept price difference
    accept_price_change: bool = Field(False, description="Accept if price changes")


class ModificationResponse(BaseSchema):
    """Modification response"""
    booking_id: UUID
    booking_reference: str
    
    # What changed
    modifications_applied: List[str]
    
    # Price impact
    original_total: Decimal
    new_total: Decimal
    price_difference: Decimal
    additional_payment_required: bool
    additional_amount: Decimal
    
    # Status
    requires_admin_approval: bool
    auto_approved: bool
    
    message: str


class DateChangeRequest(BaseCreateSchema):
    """Request to change check-in date"""
    booking_id: UUID
    new_check_in_date: date = Field(..., description="New desired check-in date")
    reason: str = Field(..., min_length=10, max_length=500)


class DurationChangeRequest(BaseCreateSchema):
    """Request to change stay duration"""
    booking_id: UUID
    new_duration_months: int = Field(..., ge=1, le=24)
    reason: str = Field(..., min_length=10, max_length=500)


class RoomTypeChangeRequest(BaseCreateSchema):
    """Request to change room type"""
    booking_id: UUID
    new_room_type: RoomType
    reason: str = Field(..., min_length=10, max_length=500)
    accept_price_difference: bool = Field(False)


class ModificationApproval(BaseCreateSchema):
    """Approve/reject modification request"""
    modification_request_id: UUID
    approved: bool
    
    # If approved
    adjusted_price: Optional[Decimal] = None
    
    # If rejected
    rejection_reason: Optional[str] = None
    
    admin_notes: Optional[str] = None