"""
Student room history and transfer schemas
"""
from datetime import date
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class RoomHistoryResponse(BaseSchema):
    """Student room history"""
    student_id: UUID
    student_name: str
    hostel_id: UUID
    hostel_name: str
    room_history: List["RoomHistoryItem"] = Field(..., description="Room assignment history")


class RoomHistoryItem(BaseResponseSchema):
    """Individual room history entry"""
    hostel_id: UUID
    hostel_name: str
    room_id: UUID
    room_number: str
    room_type: str
    bed_id: Optional[UUID]
    bed_number: Optional[str]
    
    move_in_date: date
    move_out_date: Optional[date]
    duration_days: Optional[int]
    
    rent_amount: Optional[Decimal]
    reason: Optional[str]
    
    requested_by: Optional[UUID]
    approved_by: Optional[UUID]


class RoomTransferRequest(BaseCreateSchema):
    """Request room transfer"""
    student_id: UUID = Field(..., description="Student ID")
    current_room_id: UUID = Field(..., description="Current room ID")
    requested_room_id: UUID = Field(..., description="Desired room ID")
    requested_bed_id: Optional[UUID] = Field(None, description="Desired bed ID (if specific)")
    
    transfer_date: date = Field(..., description="Desired transfer date")
    reason: str = Field(..., min_length=10, max_length=500, description="Transfer reason")
    
    # Financial implications
    accept_price_difference: bool = Field(
        False,
        description="Accept if new room has different price"
    )


class RoomTransferApproval(BaseCreateSchema):
    """Approve/reject room transfer"""
    transfer_request_id: UUID = Field(..., description="Transfer request ID")
    approved: bool = Field(..., description="Approval status")
    
    # If approved
    new_room_id: Optional[UUID] = Field(None, description="Approved room (may differ from requested)")
    new_bed_id: Optional[UUID] = Field(None, description="Assigned bed")
    transfer_date: Optional[date] = Field(None, description="Approved transfer date")
    
    # If rejected
    rejection_reason: Optional[str] = Field(None, description="Rejection reason")
    
    # Financial adjustments
    rent_adjustment: Optional[Decimal] = Field(None, description="Rent adjustment amount")
    additional_charges: Optional[Decimal] = Field(None, description="Transfer charges")
    
    admin_notes: Optional[str] = Field(None, description="Admin notes")


class RoomTransferStatus(BaseSchema):
    """Room transfer request status"""
    request_id: UUID
    student_id: UUID
    student_name: str
    
    current_room: str
    requested_room: str
    
    transfer_date: date
    reason: str
    
    status: str = Field(..., pattern="^(pending|approved|rejected|completed|cancelled)$")
    requested_at: datetime
    processed_at: Optional[datetime]
    processed_by: Optional[UUID]
    
    approval_notes: Optional[str]


class BulkRoomTransfer(BaseCreateSchema):
    """Bulk room transfer (admin only)"""
    transfers: List["SingleTransfer"] = Field(..., min_items=1, description="List of transfers")
    transfer_date: date = Field(..., description="Transfer date for all")
    reason: str = Field(..., description="Common reason")


class SingleTransfer(BaseSchema):
    """Single transfer in bulk operation"""
    student_id: UUID
    new_room_id: UUID
    new_bed_id: Optional[UUID]