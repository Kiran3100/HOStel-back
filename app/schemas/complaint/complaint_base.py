"""
Complaint base schemas
"""
from typing import List, Optional
from pydantic import Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import ComplaintCategory, ComplaintStatus, Priority


class ComplaintBase(BaseSchema):
    """Base complaint schema"""
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
    attachments: List[HttpUrl] = Field(default_factory=list, description="Photo/document URLs")


class ComplaintCreate(ComplaintBase, BaseCreateSchema):
    """Create complaint schema"""
    pass


class ComplaintUpdate(BaseUpdateSchema):
    """Update complaint schema"""
    title: Optional[str] = Field(None, min_length=5, max_length=255)
    description: Optional[str] = Field(None, min_length=20, max_length=2000)
    category: Optional[ComplaintCategory] = None
    sub_category: Optional[str] = None
    priority: Optional[Priority] = None
    location_details: Optional[str] = None
    attachments: Optional[List[HttpUrl]] = None
    
    # Status updates
    status: Optional[ComplaintStatus] = None


class ComplaintStatusUpdate(BaseUpdateSchema):
    """Update complaint status"""
    status: ComplaintStatus = Field(..., description="New status")
    notes: Optional[str] = Field(None, max_length=500, description="Status change notes")