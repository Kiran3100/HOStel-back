"""
Maintenance request submission schemas
"""
from datetime import date
from typing import List, Optional
from pydantic import Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema
from app.schemas.common.enums import MaintenanceCategory, Priority


class MaintenanceRequest(BaseCreateSchema):
    """Submit maintenance request"""
    hostel_id: UUID
    room_id: Optional[UUID] = None
    
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=20, max_length=2000)
    
    category: MaintenanceCategory
    priority: Priority = Field(Priority.MEDIUM)
    
    location: Optional[str] = None
    issue_photos: List[HttpUrl] = Field(default_factory=list)


class RequestSubmission(BaseCreateSchema):
    """Detailed request submission with supervisor context"""
    hostel_id: UUID
    room_id: Optional[UUID] = None
    
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=20, max_length=2000)
    
    category: MaintenanceCategory
    priority: Priority
    
    # Cost estimation (supervisor)
    estimated_cost: Optional[Decimal] = Field(None, ge=0, description="Estimated repair cost")
    
    # Preferred vendor
    preferred_vendor: Optional[str] = None
    
    # Timeline
    estimated_days: Optional[int] = Field(None, ge=1, description="Estimated days to complete")
    
    # Urgency
    requires_immediate_attention: bool = Field(False)


class EmergencyRequest(BaseCreateSchema):
    """Emergency maintenance request"""
    hostel_id: UUID
    
    emergency_type: str = Field(
        ...,
        pattern="^(fire|flood|electrical_hazard|gas_leak|structural_damage|other)$"
    )
    
    description: str = Field(..., min_length=20)
    location: str = Field(..., description="Exact location of emergency")
    
    # Immediate actions taken
    immediate_actions_taken: Optional[str] = None
    
    # Safety
    evacuated: bool = Field(False, description="Area evacuated")
    authorities_notified: bool = Field(False, description="Emergency services notified")
    
    contact_person: str
    contact_phone: str