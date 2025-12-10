"""
Student base schemas
"""
from datetime import date
from typing import Optional
from pydantic import Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import StudentStatus, IDProofType, DietaryPreference


class StudentBase(BaseSchema):
    """Base student schema"""
    user_id: UUID = Field(..., description="Associated user ID")
    hostel_id: UUID = Field(..., description="Current hostel ID")
    room_id: Optional[UUID] = Field(None, description="Assigned room ID")
    bed_id: Optional[UUID] = Field(None, description="Assigned bed ID")
    
    # Identification
    id_proof_type: Optional[IDProofType] = Field(None, description="ID proof type")
    id_proof_number: Optional[str] = Field(None, max_length=50, description="ID proof number")
    
    # Guardian information
    guardian_name: str = Field(..., min_length=2, max_length=255, description="Guardian name")
    guardian_phone: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$', description="Guardian phone")
    guardian_email: Optional[str] = Field(None, description="Guardian email")
    guardian_relation: Optional[str] = Field(None, max_length=50, description="Relation to student")
    guardian_address: Optional[str] = Field(None, max_length=500, description="Guardian address")
    
    # Institutional information (for students)
    institution_name: Optional[str] = Field(None, max_length=255, description="College/University name")
    course: Optional[str] = Field(None, max_length=255, description="Course name")
    year_of_study: Optional[str] = Field(None, max_length=50, description="Year/Semester")
    student_id_number: Optional[str] = Field(None, max_length=100, description="College ID number")
    
    # Employment information (for working professionals)
    company_name: Optional[str] = Field(None, max_length=255, description="Company name")
    designation: Optional[str] = Field(None, max_length=255, description="Job designation")
    
    # Check-in/Check-out dates
    check_in_date: Optional[date] = Field(None, description="Check-in date")
    expected_checkout_date: Optional[date] = Field(None, description="Expected checkout date")
    
    # Financial
    security_deposit_amount: Decimal = Field(Decimal("0.00"), ge=0, description="Security deposit amount")
    monthly_rent_amount: Optional[Decimal] = Field(None, ge=0, description="Monthly rent")
    
    # Meal preferences
    mess_subscribed: bool = Field(False, description="Subscribed to mess facility")
    dietary_preference: Optional[DietaryPreference] = Field(None, description="Dietary preference")
    food_allergies: Optional[str] = Field(None, max_length=500, description="Food allergies")
    
    @field_validator('expected_checkout_date')
    @classmethod
    def validate_checkout_after_checkin(cls, v: Optional[date], info) -> Optional[date]:
        """Validate checkout date is after check-in"""
        if v and info.data.get('check_in_date'):
            if v <= info.data['check_in_date']:
                raise ValueError('Checkout date must be after check-in date')
        return v


class StudentCreate(StudentBase, BaseCreateSchema):
    """Create student schema"""
    # Optionally link to booking
    booking_id: Optional[UUID] = Field(None, description="Source booking ID if from booking conversion")


class StudentUpdate(BaseUpdateSchema):
    """Update student schema"""
    room_id: Optional[UUID] = None
    bed_id: Optional[UUID] = None
    
    # Guardian updates
    guardian_name: Optional[str] = Field(None, min_length=2, max_length=255)
    guardian_phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{9,14}$')
    guardian_email: Optional[str] = None
    
    # Institutional updates
    institution_name: Optional[str] = None
    course: Optional[str] = None
    year_of_study: Optional[str] = None
    
    # Employment updates
    company_name: Optional[str] = None
    designation: Optional[str] = None
    
    # Dates
    check_in_date: Optional[date] = None
    expected_checkout_date: Optional[date] = None
    actual_checkout_date: Optional[date] = None
    
    # Financial
    security_deposit_amount: Optional[Decimal] = Field(None, ge=0)
    monthly_rent_amount: Optional[Decimal] = Field(None, ge=0)
    
    # Meal
    mess_subscribed: Optional[bool] = None
    dietary_preference: Optional[DietaryPreference] = None
    food_allergies: Optional[str] = None
    
    # Status
    student_status: Optional[StudentStatus] = None


class StudentCheckInRequest(BaseCreateSchema):
    """Check-in student request"""
    student_id: UUID = Field(..., description="Student ID")
    check_in_date: date = Field(..., description="Check-in date")
    room_id: UUID = Field(..., description="Assigned room")
    bed_id: UUID = Field(..., description="Assigned bed")
    security_deposit_paid: bool = Field(False, description="Security deposit payment status")
    initial_rent_paid: bool = Field(False, description="Initial rent payment status")


class StudentCheckOutRequest(BaseCreateSchema):
    """Check-out student request"""
    student_id: UUID = Field(..., description="Student ID")
    checkout_date: date = Field(..., description="Checkout date")
    reason: Optional[str] = Field(None, description="Checkout reason")
    refund_security_deposit: bool = Field(True, description="Refund security deposit")
    final_dues_cleared: bool = Field(False, description="All dues cleared")