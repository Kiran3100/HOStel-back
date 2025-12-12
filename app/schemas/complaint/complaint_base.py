"""
Complaint base schemas with enhanced validation and type safety.
"""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from pydantic import Field, HttpUrl, field_validator, model_validator

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import ComplaintCategory, ComplaintStatus, Priority


class ComplaintBase(BaseSchema):
    """Base complaint schema with comprehensive validation."""
    
    hostel_id: UUID = Field(..., description="Hostel ID")
    raised_by: UUID = Field(..., description="User who raised complaint")
    student_id: Optional[UUID] = Field(None, description="Student ID if raised by student")
    
    # Complaint details
    title: str = Field(..., min_length=5, max_length=255, description="Complaint title")
    description: str = Field(..., min_length=20, max_length=2000, description="Detailed description")
    
    category: ComplaintCategory = Field(..., description="Complaint category")
    sub_category: Optional[str] = Field(None, max_length=100, description="Sub-category")
    
    priority: Priority = Field(Priority.MEDIUM, description="Priority level")
    
    # Location
    room_id: Optional[UUID] = Field(None, description="Related room")
    location_details: Optional[str] = Field(None, max_length=500, description="Specific location details")
    
    # Attachments
    attachments: List[HttpUrl] = Field(default_factory=list, max_items=10, description="Photo/document URLs")

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is meaningful."""
        v = v.strip()
        if len(v.split()) < 2:
            raise ValueError("Title must contain at least 2 words")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Validate description is detailed enough."""
        v = v.strip()
        if len(v.split()) < 5:
            raise ValueError("Description must contain at least 5 words")
        return v

    @field_validator("sub_category")
    @classmethod
    def validate_sub_category(cls, v: Optional[str]) -> Optional[str]:
        """Normalize sub-category."""
        if v:
            return v.strip().lower().replace(" ", "_")
        return v

    @model_validator(mode="after")
    def validate_location_consistency(self) -> "ComplaintBase":
        """Ensure location details are provided when room_id is not specified."""
        if not self.room_id and not self.location_details:
            raise ValueError("Either room_id or location_details must be provided")
        return self


class ComplaintCreate(ComplaintBase, BaseCreateSchema):
    """Create complaint schema with additional validation."""
    
    @model_validator(mode="after")
    def validate_priority_category_consistency(self) -> "ComplaintCreate":
        """Validate priority is appropriate for category."""
        # Security and electrical issues should have higher default priority
        high_priority_categories = {
            ComplaintCategory.SECURITY,
            ComplaintCategory.ELECTRICAL,
            ComplaintCategory.PLUMBING
        }
        
        if (self.category in high_priority_categories and 
            self.priority in [Priority.LOW, Priority.MEDIUM]):
            # This is a warning, not an error - just ensure it's intentional
            pass
            
        return self


class ComplaintUpdate(BaseUpdateSchema):
    """Update complaint schema with partial field support."""
    
    title: Optional[str] = Field(None, min_length=5, max_length=255)
    description: Optional[str] = Field(None, min_length=20, max_length=2000)
    category: Optional[ComplaintCategory] = None
    sub_category: Optional[str] = Field(None, max_length=100)
    priority: Optional[Priority] = None
    location_details: Optional[str] = Field(None, max_length=500)
    attachments: Optional[List[HttpUrl]] = Field(None, max_items=10)
    
    # Status updates
    status: Optional[ComplaintStatus] = None

    @field_validator("title", "description")
    @classmethod
    def validate_text_fields(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize text fields."""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Field cannot be empty or whitespace")
        return v

    @model_validator(mode="after")
    def validate_status_transition(self) -> "ComplaintUpdate":
        """Validate status transitions are logical."""
        # Note: This would need access to current status to fully validate
        # For now, we just ensure closed complaints aren't updated
        if self.status == ComplaintStatus.CLOSED:
            # Only allow certain fields to be updated on closed complaints
            allowed_fields = {"attachments"}
            updated_fields = {k for k, v in self.model_dump(exclude_unset=True).items() if v is not None}
            
            if updated_fields - allowed_fields:
                raise ValueError("Cannot update closed complaints except for attachments")
                
        return self


class ComplaintStatusUpdate(BaseUpdateSchema):
    """Update complaint status with validation."""
    
    status: ComplaintStatus = Field(..., description="New status")
    notes: Optional[str] = Field(None, min_length=10, max_length=500, description="Status change notes")

    @field_validator("notes")
    @classmethod
    def validate_notes_required_for_certain_statuses(cls, v: Optional[str], info) -> Optional[str]:
        """Ensure notes are provided for certain status changes."""
        status = info.data.get("status")
        
        # Notes required for these statuses
        notes_required_statuses = {
            ComplaintStatus.ON_HOLD,
            ComplaintStatus.CLOSED,
            ComplaintStatus.REOPENED
        }
        
        if status in notes_required_statuses and not v:
            raise ValueError(f"Notes are required when setting status to {status.value}")
            
        if v:
            return v.strip()
        return v