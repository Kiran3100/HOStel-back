"""
Booking to student conversion schemas
"""
from datetime import date
from typing import Optional, List
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class ConvertToStudentRequest(BaseCreateSchema):
    """Convert confirmed booking to student profile"""
    booking_id: UUID = Field(..., description="Booking ID to convert")
    
    # Check-in details
    actual_check_in_date: date = Field(..., description="Actual check-in date")
    
    # Financial confirmation
    security_deposit_paid: bool = Field(..., description="Security deposit paid")
    first_month_rent_paid: bool = Field(..., description="First month rent paid")
    
    # Additional student details (if not in booking)
    student_id_number: Optional[str] = None
    guardian_address: Optional[str] = None
    
    # Documents uploaded
    id_proof_uploaded: bool = Field(False)
    photo_uploaded: bool = Field(False)
    
    notes: Optional[str] = Field(None, max_length=500, description="Conversion notes")


class ConversionResponse(BaseSchema):
    """Conversion response"""
    booking_id: UUID
    student_profile_id: UUID
    
    converted: bool
    conversion_date: date
    
    # Room assignment
    room_number: str
    bed_number: str
    
    # Financial setup
    monthly_rent: Decimal
    security_deposit: Decimal
    next_payment_due_date: date
    
    message: str
    next_steps: List[str]


class ConversionChecklist(BaseSchema):
    """Pre-conversion checklist"""
    booking_id: UUID
    booking_reference: str
    
    # Checklist items
    checks: List["ChecklistItem"]
    
    all_checks_passed: bool
    can_convert: bool
    
    missing_items: List[str]


class ChecklistItem(BaseSchema):
    """Individual checklist item"""
    item_name: str
    description: str
    is_completed: bool
    is_required: bool
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None


class BulkConversion(BaseCreateSchema):
    """Convert multiple bookings to students"""
    booking_ids: List[UUID] = Field(..., min_items=1)
    conversion_date: date
    
    # Common financial confirmation
    all_deposits_paid: bool
    all_first_rents_paid: bool


class ConversionRollback(BaseCreateSchema):
    """Rollback conversion (emergency only)"""
    student_profile_id: UUID
    reason: str = Field(..., min_length=20, max_length=500)
    
    # What to do with data
    delete_student_profile: bool = Field(False)
    restore_booking: bool = Field(True)