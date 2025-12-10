"""
Student profile management schemas
"""
from typing import List, Optional
from pydantic import Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import IDProofType, DietaryPreference


class StudentProfileCreate(BaseCreateSchema):
    """Create student profile (extends user registration)"""
    # Guardian (required for students)
    guardian_name: str = Field(..., min_length=2, max_length=255)
    guardian_phone: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$')
    guardian_email: Optional[str] = None
    guardian_relation: Optional[str] = None
    guardian_address: Optional[str] = None
    
    # Institutional OR employment (at least one)
    institution_name: Optional[str] = None
    course: Optional[str] = None
    year_of_study: Optional[str] = None
    student_id_number: Optional[str] = None
    
    company_name: Optional[str] = None
    designation: Optional[str] = None
    
    # ID proof
    id_proof_type: Optional[IDProofType] = None
    id_proof_number: Optional[str] = None
    
    # Preferences
    dietary_preference: Optional[DietaryPreference] = None
    food_allergies: Optional[str] = None


class StudentProfileUpdate(BaseUpdateSchema):
    """Update student profile"""
    # Guardian updates
    guardian_name: Optional[str] = Field(None, min_length=2, max_length=255)
    guardian_phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{9,14}$')
    guardian_email: Optional[str] = None
    guardian_relation: Optional[str] = None
    guardian_address: Optional[str] = None
    
    # Institutional
    institution_name: Optional[str] = None
    course: Optional[str] = None
    year_of_study: Optional[str] = None
    student_id_number: Optional[str] = None
    
    # Employment
    company_name: Optional[str] = None
    designation: Optional[str] = None
    
    # Preferences
    dietary_preference: Optional[DietaryPreference] = None
    food_allergies: Optional[str] = None


class StudentDocuments(BaseSchema):
    """Student document management"""
    student_id: UUID
    documents: List["DocumentInfo"] = Field(default_factory=list)


class DocumentInfo(BaseSchema):
    """Individual document information"""
    document_type: str = Field(..., description="Type of document")
    document_name: str = Field(..., description="Document name")
    document_url: HttpUrl = Field(..., description="Document URL")
    uploaded_at: datetime = Field(..., description="Upload timestamp")
    verified: bool = Field(False, description="Verification status")
    verified_by: Optional[UUID] = None
    verified_at: Optional[datetime] = None


class DocumentUploadRequest(BaseCreateSchema):
    """Upload document request"""
    student_id: UUID = Field(..., description="Student ID")
    document_type: str = Field(
        ...,
        pattern="^(id_proof|address_proof|photo|institutional_id|company_id|other)$",
        description="Document type"
    )
    document_name: str = Field(..., description="Document name")
    document_url: HttpUrl = Field(..., description="Document URL (after upload to storage)")


class DocumentVerificationRequest(BaseCreateSchema):
    """Verify document request"""
    document_id: UUID = Field(..., description="Document ID")
    verified: bool = Field(..., description="Verification status")
    notes: Optional[str] = Field(None, description="Verification notes")


class StudentPreferences(BaseUpdateSchema):
    """Student preferences and settings"""
    # Meal preferences
    mess_subscribed: Optional[bool] = None
    dietary_preference: Optional[DietaryPreference] = None
    food_allergies: Optional[str] = None
    
    # Notification preferences
    email_notifications: bool = Field(True)
    sms_notifications: bool = Field(True)
    push_notifications: bool = Field(True)
    
    # Privacy
    show_profile_to_others: bool = Field(True, description="Show profile to other students")
    allow_roommate_contact: bool = Field(True, description="Allow roommates to contact")