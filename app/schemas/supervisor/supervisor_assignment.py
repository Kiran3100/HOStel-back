"""
Supervisor assignment schemas
"""
from datetime import date
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema
from app.schemas.common.enums import PermissionLevel


class SupervisorAssignment(BaseResponseSchema):
    """Supervisor-hostel assignment"""
    supervisor_id: UUID
    supervisor_name: str
    hostel_id: UUID
    hostel_name: str
    assigned_by: UUID
    assigned_by_name: str
    assigned_date: date
    is_active: bool
    
    # Permissions summary
    permission_level: str = Field(..., description="Summary of permission level")
    
    # Activity
    last_active: Optional[datetime]


class AssignmentRequest(BaseCreateSchema):
    """Assign supervisor to hostel"""
    user_id: UUID = Field(..., description="User ID to assign as supervisor")
    hostel_id: UUID = Field(..., description="Hostel ID")
    
    # Employment details
    employee_id: Optional[str] = None
    join_date: date = Field(..., description="Joining date")
    employment_type: str = Field("full_time", pattern="^(full_time|part_time|contract)$")
    shift_timing: Optional[str] = None
    
    # Permissions (optional, will use defaults if not provided)
    permissions: Optional[dict] = Field(None, description="Custom permissions")


class AssignmentUpdate(BaseUpdateSchema):
    """Update supervisor assignment"""
    employee_id: Optional[str] = None
    employment_type: Optional[str] = Field(None, pattern="^(full_time|part_time|contract)$")
    shift_timing: Optional[str] = None
    is_active: Optional[bool] = None


class RevokeAssignmentRequest(BaseCreateSchema):
    """Revoke supervisor assignment"""
    supervisor_id: UUID = Field(..., description="Supervisor ID")
    revoke_date: date = Field(..., description="Effective revocation date")
    reason: str = Field(..., min_length=10, max_length=500, description="Reason for revocation")
    
    # Handover
    handover_to_supervisor_id: Optional[UUID] = Field(
        None,
        description="Transfer responsibilities to another supervisor"
    )
    handover_notes: Optional[str] = None


class AssignmentTransfer(BaseCreateSchema):
    """Transfer supervisor to different hostel"""
    supervisor_id: UUID = Field(..., description="Supervisor ID")
    from_hostel_id: UUID = Field(..., description="Current hostel")
    to_hostel_id: UUID = Field(..., description="New hostel")
    transfer_date: date = Field(..., description="Transfer effective date")
    reason: str = Field(..., description="Transfer reason")
    
    # Whether to retain same permissions
    retain_permissions: bool = Field(True, description="Keep same permission set")
    
    # New permissions if not retaining
    new_permissions: Optional[dict] = None