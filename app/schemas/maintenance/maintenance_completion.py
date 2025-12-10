"""
Maintenance completion schemas
"""
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from pydantic import Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class CompletionRequest(BaseCreateSchema):
    """Mark maintenance as completed"""
    maintenance_id: UUID
    
    # Completion details
    work_notes: str = Field(..., min_length=20, max_length=2000, description="Work performed")
    
    # Materials used
    materials_used: List["MaterialItem"] = Field(default_factory=list)
    
    # Labor
    labor_hours: Decimal = Field(..., ge=0, description="Labor hours spent")
    
    # Cost
    actual_cost: Decimal = Field(..., ge=0, description="Actual cost incurred")
    cost_breakdown: Optional[dict] = None
    
    # Photos
    completion_photos: List[HttpUrl] = Field(default_factory=list, description="After photos")
    
    # Timeline
    actual_completion_date: date = Field(..., description="Actual completion date")
    
    # Follow-up
    follow_up_required: bool = Field(False)
    follow_up_notes: Optional[str] = None


class MaterialItem(BaseSchema):
    """Material used in maintenance"""
    material_name: str = Field(..., min_length=2, max_length=255)
    quantity: Decimal = Field(..., ge=0)
    unit: str = Field(..., description="Unit of measurement (pcs, kg, liters, etc.)")
    unit_cost: Decimal = Field(..., ge=0)
    total_cost: Decimal = Field(..., ge=0)
    
    supplier: Optional[str] = None


class QualityCheck(BaseCreateSchema):
    """Quality check for completed work"""
    maintenance_id: UUID
    
    # Inspection
    quality_check_passed: bool = Field(..., description="Quality check result")
    
    # Checklist
    checklist_items: List["ChecklistItem"] = Field(default_factory=list)
    
    # Notes
    quality_check_notes: Optional[str] = Field(None, max_length=1000)
    
    # Inspector
    checked_by: UUID
    
    # Follow-up actions
    rework_required: bool = Field(False)
    rework_details: Optional[str] = None


class ChecklistItem(BaseSchema):
    """Quality check checklist item"""
    item_description: str
    status: str = Field(..., pattern="^(pass|fail|na)$")
    notes: Optional[str] = None


class CompletionResponse(BaseSchema):
    """Completion response"""
    maintenance_id: UUID
    request_number: str
    
    completed: bool
    completed_at: datetime
    completed_by: UUID
    completed_by_name: str
    
    # Cost summary
    estimated_cost: Decimal
    actual_cost: Decimal
    cost_variance: Decimal
    within_budget: bool
    
    # Quality
    quality_checked: bool
    quality_check_passed: Optional[bool]
    
    message: str


class CompletionCertificate(BaseSchema):
    """Work completion certificate"""
    maintenance_id: UUID
    request_number: str
    certificate_number: str
    
    # Work details
    work_description: str
    materials_used: List[MaterialItem]
    labor_hours: Decimal
    
    # Cost
    total_cost: Decimal
    
    # Parties
    completed_by: str
    verified_by: str
    approved_by: str
    
    # Dates
    completion_date: date
    verification_date: date
    certificate_issue_date: date
    
    # Warranty
    warranty_period_months: Optional[int] = None
    warranty_terms: Optional[str] = None