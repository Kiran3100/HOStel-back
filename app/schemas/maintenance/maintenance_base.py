"""
Maintenance base schemas
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import MaintenanceCategory, MaintenanceStatus, MaintenanceIssueType, Priority


class MaintenanceBase(BaseSchema):
    """Base maintenance schema"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    requested_by: UUID = Field(..., description="User who requested")
    room_id: Optional[UUID] = Field(None, description="Room where issue exists")
    
    # Request details
    title: str = Field(..., min_length=5, max_length=255, description="Issue title")
    description: str = Field(..., min_length=20, max_length=2000, description="Detailed description")
    
    category: MaintenanceCategory = Field(..., description="Maintenance category")
    priority: Priority = Field(Priority.MEDIUM, description="Priority level")
    issue_type: MaintenanceIssueType = Field(MaintenanceIssueType.ROUTINE, description="Issue type")
    
    # Location
    location: Optional[str] = Field(None, max_length=500, description="Location details")
    floor: Optional[int] = Field(None, ge=0, description="Floor number")
    specific_area: Optional[str] = Field(None, max_length=255, description="Specific area")
    
    # Attachments
    issue_photos: List[HttpUrl] = Field(default_factory=list, description="Issue photos")


class MaintenanceCreate(MaintenanceBase, BaseCreateSchema):
    """Create maintenance request"""
    pass


class MaintenanceUpdate(BaseUpdateSchema):
    """Update maintenance request"""
    title: Optional[str] = Field(None, min_length=5, max_length=255)
    description: Optional[str] = Field(None, min_length=20, max_length=2000)
    category: Optional[MaintenanceCategory] = None
    priority: Optional[Priority] = None
    location: Optional[str] = None
    
    # Status
    status: Optional[MaintenanceStatus] = None
    
    # Cost
    estimated_cost: Optional[Decimal] = Field(None, ge=0)
    actual_cost: Optional[Decimal] = Field(None, ge=0)


class MaintenanceStatusUpdate(BaseUpdateSchema):
    """Update maintenance status"""
    status: MaintenanceStatus = Field(..., description="New status")
    notes: Optional[str] = Field(None, max_length=500)