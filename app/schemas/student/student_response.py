"""
Student response schemas
"""
from decimal import Decimal
from datetime import date, datetime
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import StudentStatus, IDProofType, DietaryPreference


class StudentResponse(BaseResponseSchema):
    """Student response schema"""
    user_id: UUID
    hostel_id: UUID
    hostel_name: str
    room_id: Optional[UUID]
    room_number: Optional[str]
    bed_id: Optional[UUID]
    bed_number: Optional[str]
    
    # Personal info (from user)
    full_name: str
    email: str
    phone: str
    
    # Guardian
    guardian_name: str
    guardian_phone: str
    
    # Status
    student_status: StudentStatus
    check_in_date: Optional[date]
    expected_checkout_date: Optional[date]
    
    # Financial
    monthly_rent_amount: Optional[Decimal]
    security_deposit_amount: Decimal
    security_deposit_paid: bool
    
    # Meal
    mess_subscribed: bool


class StudentDetail(BaseResponseSchema):
    """Detailed student information"""
    # User information
    user_id: UUID
    full_name: str
    email: str
    phone: str
    gender: Optional[str]
    date_of_birth: Optional[date]
    profile_image_url: Optional[str]
    
    # Hostel assignment
    hostel_id: UUID
    hostel_name: str
    room_id: Optional[UUID]
    room_number: Optional[str]
    room_type: Optional[str]
    bed_id: Optional[UUID]
    bed_number: Optional[str]
    
    # Identification
    id_proof_type: Optional[IDProofType]
    id_proof_number: Optional[str]
    id_proof_document_url: Optional[str]
    
    # Guardian information
    guardian_name: str
    guardian_phone: str
    guardian_email: Optional[str]
    guardian_relation: Optional[str]
    guardian_address: Optional[str]
    
    # Institutional information
    institution_name: Optional[str]
    course: Optional[str]
    year_of_study: Optional[str]
    student_id_number: Optional[str]
    
    # Employment information
    company_name: Optional[str]
    designation: Optional[str]
    company_id_url: Optional[str]
    
    # Dates
    check_in_date: Optional[date]
    expected_checkout_date: Optional[date]
    actual_checkout_date: Optional[date]
    
    # Financial
    security_deposit_amount: Decimal
    security_deposit_paid: bool
    security_deposit_paid_date: Optional[date]
    monthly_rent_amount: Optional[Decimal]
    
    # Meal preferences
    mess_subscribed: bool
    dietary_preference: Optional[DietaryPreference]
    food_allergies: Optional[str]
    
    # Status
    student_status: StudentStatus
    notice_period_start: Optional[date]
    notice_period_end: Optional[date]
    
    # Source
    booking_id: Optional[UUID]
    
    # Documents
    additional_documents: List[dict] = Field(default_factory=list)


class StudentProfile(BaseSchema):
    """Student public profile"""
    id: UUID
    full_name: str
    profile_image_url: Optional[str]
    hostel_name: str
    room_number: Optional[str]
    check_in_date: Optional[date]
    institution_name: Optional[str]
    course: Optional[str]


class StudentListItem(BaseSchema):
    """Student list item (for admin views)"""
    id: UUID
    user_id: UUID
    full_name: str
    email: str
    phone: str
    room_number: Optional[str]
    bed_number: Optional[str]
    student_status: StudentStatus
    check_in_date: Optional[date]
    monthly_rent: Optional[Decimal]
    payment_status: str = Field(..., description="current/overdue/advance")
    created_at: datetime


class StudentFinancialInfo(BaseSchema):
    """Student financial information"""
    student_id: UUID
    student_name: str
    
    # Rent
    monthly_rent_amount: Decimal
    
    # Security deposit
    security_deposit_amount: Decimal
    security_deposit_paid: bool
    security_deposit_refundable: Decimal
    
    # Payments
    total_paid: Decimal
    total_due: Decimal
    last_payment_date: Optional[date]
    next_due_date: Optional[date]
    
    # Outstanding
    overdue_amount: Decimal
    advance_amount: Decimal
    
    # Mess
    mess_charges_monthly: Decimal
    mess_balance: Decimal


class StudentContactInfo(BaseSchema):
    """Student contact information"""
    student_id: UUID
    student_name: str
    email: str
    phone: str
    
    # Guardian
    guardian_name: str
    guardian_phone: str
    guardian_email: Optional[str]
    guardian_relation: Optional[str]
    
    # Emergency
    emergency_contact_name: Optional[str]
    emergency_contact_phone: Optional[str]