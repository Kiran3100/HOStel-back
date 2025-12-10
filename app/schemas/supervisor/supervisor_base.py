"""
Supervisor base schemas
"""
from datetime import date
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import SupervisorStatus, EmploymentType


class SupervisorBase(BaseSchema):
    """Base supervisor schema"""
    user_id: UUID = Field(..., description="Associated user ID")
    assigned_hostel_id: UUID = Field(..., description="Assigned hostel ID")
    
    # Employment details
    employee_id: Optional[str] = Field(None, max_length=100, description="Employee ID")
    join_date: date = Field(..., description="Joining date")
    employment_type: EmploymentType = Field(EmploymentType.FULL_TIME, description="Employment type")
    shift_timing: Optional[str] = Field(None, max_length=100, description="Shift timing (e.g., '9 AM - 6 PM')")


class SupervisorCreate(SupervisorBase, BaseCreateSchema):
    """Create supervisor schema"""
    assigned_by: UUID = Field(..., description="Admin who is assigning the supervisor")
    
    # Initial permissions (can be customized later)
    permissions: Optional[dict] = Field(None, description="Initial permission settings")


class SupervisorUpdate(BaseUpdateSchema):
    """Update supervisor schema"""
    employee_id: Optional[str] = Field(None, max_length=100)
    employment_type: Optional[EmploymentType] = None
    shift_timing: Optional[str] = None
    
    # Status updates
    status: Optional[SupervisorStatus] = None
    is_active: Optional[bool] = None
    
    # Permissions update
    permissions: Optional[dict] = None


class SupervisorStatusUpdate(BaseUpdateSchema):
    """Update supervisor status"""
    status: SupervisorStatus = Field(..., description="New status")
    is_active: bool = Field(..., description="Active status")
    
    # If terminating
    termination_date: Optional[date] = Field(None, description="Termination date")
    termination_reason: Optional[str] = Field(None, description="Termination reason")
    
    # If suspending
    suspension_reason: Optional[str] = Field(None, description="Suspension reason")
    suspension_end_date: Optional[date] = Field(None, description="Expected end of suspension")


class SupervisorReassignment(BaseCreateSchema):
    """Reassign supervisor to different hostel"""
    supervisor_id: UUID = Field(..., description="Supervisor ID")
    new_hostel_id: UUID = Field(..., description="New hostel ID")
    effective_date: date = Field(..., description="Effective date of reassignment")
    reason: Optional[str] = Field(None, description="Reassignment reason")