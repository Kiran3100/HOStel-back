"""
Payment schedule schemas
"""
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema
from app.schemas.common.enums import FeeType, PaymentType


class PaymentSchedule(BaseResponseSchema):
    """Payment schedule"""
    student_id: UUID
    student_name: str
    hostel_id: UUID
    hostel_name: str
    
    fee_type: FeeType
    amount: Decimal
    
    start_date: date
    end_date: Optional[date]
    next_due_date: date
    
    auto_generate_invoice: bool
    is_active: bool


class ScheduleCreate(BaseCreateSchema):
    """Create payment schedule"""
    student_id: UUID = Field(..., description="Student ID")
    hostel_id: UUID = Field(..., description="Hostel ID")
    
    fee_type: FeeType = Field(..., description="Fee type (monthly/quarterly/etc)")
    amount: Decimal = Field(..., ge=0, description="Amount per period")
    
    start_date: date = Field(..., description="Schedule start date")
    end_date: Optional[date] = Field(None, description="Schedule end date (null for indefinite)")
    
    # First due date
    first_due_date: date = Field(..., description="First payment due date")
    
    # Settings
    auto_generate_invoice: bool = Field(True, description="Auto-generate invoices")
    send_reminders: bool = Field(True, description="Send payment reminders")


class ScheduleUpdate(BaseUpdateSchema):
    """Update payment schedule"""
    amount: Optional[Decimal] = Field(None, ge=0)
    next_due_date: Optional[date] = None
    end_date: Optional[date] = None
    auto_generate_invoice: Optional[bool] = None
    is_active: Optional[bool] = None


class ScheduleGeneration(BaseSchema):
    """Generate scheduled payments"""
    schedule_id: UUID
    
    # Generate for period
    generate_from_date: date
    generate_to_date: date
    
    # Options
    skip_if_already_paid: bool = Field(True)
    send_notifications: bool = Field(True)


class ScheduledPaymentGenerated(BaseSchema):
    """Result of schedule generation"""
    schedule_id: UUID
    
    payments_generated: int
    payments_skipped: int
    
    generated_payment_ids: List[UUID]
    
    next_generation_date: date


class BulkScheduleCreate(BaseCreateSchema):
    """Create schedules for multiple students"""
    hostel_id: UUID
    student_ids: List[UUID] = Field(..., min_items=1)
    
    fee_type: FeeType
    amount: Decimal = Field(..., ge=0)
    
    start_date: date
    first_due_date: date


class ScheduleSuspension(BaseCreateSchema):
    """Suspend payment schedule temporarily"""
    schedule_id: UUID
    suspension_reason: str = Field(..., min_length=10, max_length=500)
    
    suspend_from_date: date
    suspend_to_date: date
    
    skip_dues_during_suspension: bool = Field(True, description="Skip generating dues during suspension")