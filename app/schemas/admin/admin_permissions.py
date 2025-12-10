"""
Admin permission schemas
"""
from typing import Dict, List, Optional
from pydantic import Field

from app.schemas.common.base import BaseSchema
from app.schemas.common.enums import UserRole


class AdminPermissions(BaseSchema):
    """Admin-specific permissions for a hostel"""
    # Room management
    can_manage_rooms: bool = Field(True, description="Can create/edit/delete rooms")
    can_manage_beds: bool = Field(True, description="Can manage bed assignments")
    
    # Student management
    can_manage_students: bool = Field(True, description="Can add/edit/remove students")
    can_check_in_students: bool = Field(True, description="Can check-in students")
    can_check_out_students: bool = Field(True, description="Can check-out students")
    
    # Booking management
    can_approve_bookings: bool = Field(True, description="Can approve/reject bookings")
    can_manage_waitlist: bool = Field(True, description="Can manage waitlist")
    
    # Fee management
    can_manage_fees: bool = Field(True, description="Can configure fee structures")
    can_process_payments: bool = Field(True, description="Can process manual payments")
    can_issue_refunds: bool = Field(True, description="Can issue refunds")
    
    # Supervisor management
    can_manage_supervisors: bool = Field(True, description="Can assign/remove supervisors")
    can_configure_supervisor_permissions: bool = Field(True, description="Can modify supervisor permissions")
    can_override_supervisor_actions: bool = Field(True, description="Can override supervisor decisions")
    
    # Financial access
    can_view_financials: bool = Field(True, description="Can view financial reports")
    can_export_financial_data: bool = Field(True, description="Can export financial data")
    
    # Hostel configuration
    can_manage_hostel_settings: bool = Field(True, description="Can modify hostel settings")
    can_manage_hostel_profile: bool = Field(True, description="Can edit public hostel profile")
    can_toggle_public_visibility: bool = Field(True, description="Can make hostel public/private")
    
    # Data management
    can_delete_records: bool = Field(False, description="Can permanently delete records")
    can_export_data: bool = Field(True, description="Can export data")
    can_import_data: bool = Field(True, description="Can bulk import data")


class PermissionMatrix(BaseSchema):
    """Permission matrix showing what each role can do"""
    permissions: Dict[UserRole, List[str]] = Field(
        ...,
        description="Map of role to list of permission keys"
    )


class RolePermissions(BaseSchema):
    """Permissions for a specific role"""
    role: UserRole
    permissions: List[str] = Field(..., description="List of permission keys")
    description: str = Field(..., description="Role description")


class PermissionCheck(BaseSchema):
    """Check if user has specific permission"""
    user_id: UUID
    hostel_id: UUID
    permission_key: str
    
    has_permission: bool
    reason: Optional[str] = Field(None, description="Reason if permission denied")