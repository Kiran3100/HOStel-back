"""
Complaint resolution schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class ResolutionRequest(BaseCreateSchema):
    """Mark complaint as resolved"""
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
    follow_up_notes: Optional[str] = None


class ResolutionResponse(BaseSchema):
    """Resolution response"""
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


class ResolutionUpdate(BaseCreateSchema):
    """Update resolution details"""
    complaint_id: UUID
    
    resolution_notes: Optional[str] = Field(None, min_length=20, max_length=2000)
    resolution_attachments: Optional[List[HttpUrl]] = None
    follow_up_notes: Optional[str] = None


class ReopenRequest(BaseCreateSchema):
    """Reopen resolved complaint"""
    complaint_id: UUID
    
    reopen_reason: str = Field(..., min_length=20, max_length=500)
    
    # Additional details
    additional_issues: Optional[str] = Field(None, max_length=1000)
    new_attachments: List[HttpUrl] = Field(default_factory=list)


class CloseRequest(BaseCreateSchema):
    """Close complaint (final)"""
    complaint_id: UUID
    
    closure_notes: Optional[str] = Field(None, max_length=500)
    
    # Require student confirmation
    student_confirmed: bool = Field(False, description="Student confirmed resolution")