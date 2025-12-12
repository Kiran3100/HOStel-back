"""
Complaint resolution schemas with comprehensive validation.
"""
from __future__ import annotations

from datetime import datetime, date
from typing import List, Optional
from uuid import UUID

from pydantic import Field, HttpUrl, field_validator, model_validator

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class ResolutionRequest(BaseCreateSchema):
    """Mark complaint as resolved with detailed information."""
    
    complaint_id: UUID = Field(..., description="Complaint ID")
    
    resolution_notes: str = Field(
        ...,
        min_length=20,
        max_length=2000,
        description="Resolution details"
    )
    
    # Attachments (proof of resolution)
    resolution_attachments: List[HttpUrl] = Field(
        default_factory=list,
        max_items=10,
        description="Photos/documents of resolved issue"
    )
    
    # Time tracking
    actual_resolution_time: Optional[datetime] = Field(
        None,
        description="Actual time taken to resolve"
    )
    
    # Follow-up required
    follow_up_required: bool = Field(False)
    follow_up_date: Optional[date] = None
    follow_up_notes: Optional[str] = Field(None, max_length=500)

    @field_validator("resolution_notes")
    @classmethod
    def validate_resolution_notes(cls, v: str) -> str:
        """Ensure resolution notes are detailed."""
        v = v.strip()
        if len(v.split()) < 5:
            raise ValueError("Resolution notes must contain at least 5 words")
        return v

    @model_validator(mode="after")
    def validate_follow_up_consistency(self) -> "ResolutionRequest":
        """Validate follow-up fields consistency."""
        if self.follow_up_required:
            if not self.follow_up_date:
                raise ValueError("Follow-up date is required when follow-up is needed")
            if self.follow_up_date <= date.today():
                raise ValueError("Follow-up date must be in the future")
        elif self.follow_up_date or self.follow_up_notes:
            raise ValueError("Follow-up details provided but follow-up not required")
        return self


class ResolutionResponse(BaseSchema):
    """Resolution response with calculated metrics."""
    
    complaint_id: UUID
    complaint_number: str
    
    resolved: bool
    resolved_at: datetime
    resolved_by: UUID
    resolved_by_name: str
    
    resolution_notes: str
    
    # Time taken
    time_to_resolve_hours: int
    sla_met: bool
    
    message: str

    @classmethod
    def create(
        cls,
        complaint_id: UUID,
        complaint_number: str,
        resolved_by: UUID,
        resolved_by_name: str,
        resolution_notes: str,
        opened_at: datetime,
        priority_sla_hours: int
    ) -> "ResolutionResponse":
        """Factory method to create resolution response with calculations."""
        resolved_at = datetime.utcnow()
        time_to_resolve = int((resolved_at - opened_at).total_seconds() / 3600)
        
        return cls(
            complaint_id=complaint_id,
            complaint_number=complaint_number,
            resolved=True,
            resolved_at=resolved_at,
            resolved_by=resolved_by,
            resolved_by_name=resolved_by_name,
            resolution_notes=resolution_notes,
            time_to_resolve_hours=time_to_resolve,
            sla_met=time_to_resolve <= priority_sla_hours,
            message=f"Complaint {complaint_number} resolved successfully"
        )


class ResolutionUpdate(BaseCreateSchema):
    """Update resolution details after initial resolution."""
    
    complaint_id: UUID
    
    resolution_notes: Optional[str] = Field(None, min_length=20, max_length=2000)
    resolution_attachments: Optional[List[HttpUrl]] = Field(None, max_items=10)
    follow_up_notes: Optional[str] = Field(None, max_length=500)

    @field_validator("resolution_notes", "follow_up_notes")
    @classmethod
    def validate_text_fields(cls, v: Optional[str]) -> Optional[str]:
        """Validate text fields are not empty."""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Field cannot be empty or whitespace")
        return v


class ReopenRequest(BaseCreateSchema):
    """Reopen resolved complaint with validation."""
    
    complaint_id: UUID
    
    reopen_reason: str = Field(..., min_length=20, max_length=500)
    
    # Additional details
    additional_issues: Optional[str] = Field(None, max_length=1000)
    new_attachments: List[HttpUrl] = Field(default_factory=list, max_items=5)

    @field_validator("reopen_reason")
    @classmethod
    def validate_reopen_reason(cls, v: str) -> str:
        """Ensure reopen reason is detailed."""
        v = v.strip()
        if len(v.split()) < 5:
            raise ValueError("Reopen reason must contain at least 5 words")
        return v


class CloseRequest(BaseCreateSchema):
    """Close complaint (final) with optional confirmation."""
    
    complaint_id: UUID
    
    closure_notes: Optional[str] = Field(None, max_length=500)
    
    # Require student confirmation
    student_confirmed: bool = Field(False, description="Student confirmed resolution")

    @field_validator("closure_notes")
    @classmethod
    def validate_closure_notes(cls, v: Optional[str]) -> Optional[str]:
        """Validate closure notes if provided."""
        if v:
            v = v.strip()
            if len(v) < 10:
                raise ValueError("Closure notes must be at least 10 characters")
        return v