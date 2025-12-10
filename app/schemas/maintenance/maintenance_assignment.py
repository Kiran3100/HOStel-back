"""
Maintenance assignment schemas
"""
from datetime import datetime, date
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class TaskAssignment(BaseSchema):
    """Assign maintenance task to staff/vendor"""
    maintenance_id: UUID
    request_number: str
    
    assigned_to: UUID
    assigned_to_name: str
    assigned_by: UUID
    assigned_by_name: str
    
    assigned_at: datetime
    
    # Deadline
    deadline: Optional[date] = None
    
    # Instructions
    instructions: Optional[str] = None


class VendorAssignment(BaseCreateSchema):
    """Assign to external vendor"""
    maintenance_id: UUID
    
    vendor_name: str = Field(..., min_length=2, max_length=255)
    vendor_contact: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$')
    vendor_email: Optional[str] = None
    
    # Quote
    quoted_amount: Decimal = Field(..., ge=0)
    payment_terms: Optional[str] = None
    
    # Timeline
    estimated_completion_date: date
    
    # Contract
    work_order_number: Optional[str] = None
    contract_details: Optional[str] = None


class AssignmentUpdate(BaseCreateSchema):
    """Update assignment"""
    maintenance_id: UUID
    
    # Reassignment
    new_assigned_to: Optional[UUID] = None
    reassignment_reason: Optional[str] = None
    
    # Deadline change
    new_deadline: Optional[date] = None
    
    # Additional instructions
    additional_instructions: Optional[str] = None


class BulkAssignment(BaseCreateSchema):
    """Assign multiple requests to same person"""
    maintenance_ids: List[UUID] = Field(..., min_items=1)
    assigned_to: UUID
    
    common_deadline: Optional[date] = None
    instructions: Optional[str] = None


class AssignmentHistory(BaseSchema):
    """Assignment history for request"""
    maintenance_id: UUID
    assignments: List["AssignmentEntry"]


class AssignmentEntry(BaseSchema):
    """Individual assignment entry"""
    assigned_to: UUID
    assigned_to_name: str
    assigned_by: UUID
    assigned_by_name: str
    assigned_at: datetime
    
    # Completion
    completed: bool = Field(False)
    completed_at: Optional[datetime] = None
    
    # If reassigned
    reassigned: bool = Field(False)
    reassignment_reason: Optional[str] = None