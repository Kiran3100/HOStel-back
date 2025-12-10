"""
Admin-hostel assignment schemas
"""
from datetime import date, datetime
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema
from app.schemas.common.enums import PermissionLevel


class AdminHostelAssignment(BaseResponseSchema):
    """Admin-hostel assignment"""
    admin_id: UUID
    admin_name: str
    admin_email: str
    
    hostel_id: UUID
    hostel_name: str
    hostel_city: str
    
    assigned_by: Optional[UUID]
    assigned_by_name: Optional[str]
    assigned_date: date
    
    permission_level: PermissionLevel
    permissions: dict = Field(default_factory=dict, description="Specific permissions for this hostel")
    
    is_active: bool
    is_primary: bool = Field(False, description="Primary hostel for this admin")
    
    revoked_date: Optional[date] = None
    revoked_by: Optional[UUID] = None
    revoke_reason: Optional[str] = None


class AssignmentCreate(BaseCreateSchema):
    """Create admin-hostel assignment"""
    admin_id: UUID = Field(..., description="Admin user ID")
    hostel_id: UUID = Field(..., description="Hostel ID to assign")
    
    permission_level: PermissionLevel = Field(
        PermissionLevel.FULL_ACCESS,
        description="Permission level for this hostel"
    )
    
    # Specific permissions (for limited_access level)
    permissions: Optional[dict] = Field(
        None,
        description="Specific permissions (required if permission_level is limited_access)"
    )
    
    is_primary: bool = Field(False, description="Set as primary hostel")


class AssignmentUpdate(BaseUpdateSchema):
    """Update admin-hostel assignment"""
    permission_level: Optional[PermissionLevel] = None
    permissions: Optional[dict] = None
    is_primary: Optional[bool] = None
    is_active: Optional[bool] = None


class BulkAssignment(BaseCreateSchema):
    """Bulk assign admin to multiple hostels"""
    admin_id: UUID = Field(..., description="Admin user ID")
    hostel_ids: List[UUID] = Field(..., min_items=1, description="List of hostel IDs")
    
    permission_level: PermissionLevel = Field(PermissionLevel.FULL_ACCESS)
    permissions: Optional[dict] = None
    
    primary_hostel_id: Optional[UUID] = Field(None, description="Which hostel should be primary")


class RevokeAssignment(BaseCreateSchema):
    """Revoke admin-hostel assignment"""
    assignment_id: UUID = Field(..., description="Assignment ID")
    revoke_reason: str = Field(..., min_length=10, max_length=500, description="Reason for revocation")


class AssignmentList(BaseSchema):
    """List of assignments for an admin"""
    admin_id: UUID
    admin_name: str
    total_hostels: int
    active_hostels: int
    primary_hostel_id: Optional[UUID]
    
    assignments: List[AdminHostelAssignment]


class HostelAdminList(BaseSchema):
    """List of admins for a hostel"""
    hostel_id: UUID
    hostel_name: str
    total_admins: int
    
    admins: List["HostelAdminItem"]


class HostelAdminItem(BaseSchema):
    """Admin item in hostel admin list"""
    admin_id: UUID
    admin_name: str
    admin_email: str
    permission_level: PermissionLevel
    is_primary: bool
    assigned_date: date
    last_active: Optional[datetime]