"""
Supervisor permission schemas
"""
from decimal import Decimal
from typing import Dict, Optional, Any
from pydantic import Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseUpdateSchema


class SupervisorPermissions(BaseSchema):
    """Supervisor permission configuration"""
    # Complaint management
    can_manage_complaints: bool = Field(True, description="Can view and manage complaints")
    can_assign_complaints: bool = Field(True, description="Can assign complaints to staff")
    can_resolve_complaints: bool = Field(True, description="Can mark complaints as resolved")
    
    # Attendance management
    can_record_attendance: bool = Field(True, description="Can record daily attendance")
    can_approve_leaves: bool = Field(True, description="Can approve leave applications")
    max_leave_days_approval: int = Field(3, ge=1, le=10, description="Max days of leave can approve independently")
    
    # Maintenance management
    can_manage_maintenance: bool = Field(True, description="Can create and manage maintenance requests")
    can_assign_maintenance: bool = Field(True, description="Can assign maintenance tasks")
    maintenance_approval_threshold: Decimal = Field(
        Decimal("5000.00"),
        ge=0,
        description="Maximum repair cost can approve independently (INR)"
    )
    
    # Mess menu management
    can_update_mess_menu: bool = Field(True, description="Can update daily mess menu")
    menu_requires_approval: bool = Field(False, description="Menu changes require admin approval")
    can_publish_special_menus: bool = Field(False, description="Can publish special occasion menus")
    
    # Announcements
    can_create_announcements: bool = Field(True, description="Can create announcements")
    urgent_announcement_requires_approval: bool = Field(
        True,
        description="Urgent announcements require admin approval"
    )
    can_send_push_notifications: bool = Field(False, description="Can send push notifications")
    
    # Student management
    can_view_student_profiles: bool = Field(True, description="Can view student profiles")
    can_update_student_contacts: bool = Field(True, description="Can update student contact info")
    can_view_student_payments: bool = Field(True, description="Can view payment status (read-only)")
    
    # Financial access
    can_view_financial_reports: bool = Field(False, description="Can view detailed financial reports")
    can_view_revenue_data: bool = Field(False, description="Can view revenue data")
    
    # Room management
    can_view_room_availability: bool = Field(True, description="Can view room availability")
    can_suggest_room_transfers: bool = Field(True, description="Can suggest room transfers (requires admin approval)")
    
    # Booking management (view only)
    can_view_bookings: bool = Field(True, description="Can view booking requests")
    can_contact_visitors: bool = Field(True, description="Can contact visitors for inquiries")


class PermissionUpdate(BaseUpdateSchema):
    """Update supervisor permissions"""
    permissions: Dict[str, Any] = Field(..., description="Permission key-value pairs to update")
    
    @field_validator('permissions')
    @classmethod
    def validate_permissions(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate permission values"""
        valid_keys = set(SupervisorPermissions.model_fields.keys())
        invalid_keys = set(v.keys()) - valid_keys
        if invalid_keys:
            raise ValueError(f"Invalid permission keys: {invalid_keys}")
        return v


class PermissionCheckRequest(BaseSchema):
    """Request to check specific permission"""
    supervisor_id: UUID = Field(..., description="Supervisor ID")
    permission_key: str = Field(..., description="Permission to check")
    
    # Context for threshold-based permissions
    context: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional context (e.g., {'amount': 7500} for maintenance threshold)"
    )


class PermissionCheckResponse(BaseSchema):
    """Response for permission check"""
    supervisor_id: UUID
    permission_key: str
    has_permission: bool = Field(..., description="Whether supervisor has permission")
    requires_approval: bool = Field(False, description="Whether action requires admin approval")
    threshold_exceeded: bool = Field(False, description="Whether threshold is exceeded")
    message: Optional[str] = Field(None, description="Explanation message")
    
    # Threshold details if applicable
    threshold_value: Optional[Decimal] = None
    actual_value: Optional[Decimal] = None


class BulkPermissionUpdate(BaseUpdateSchema):
    """Update permissions for multiple supervisors"""
    supervisor_ids: List[UUID] = Field(..., min_items=1, description="Supervisor IDs")
    permissions: Dict[str, Any] = Field(..., description="Permissions to update for all")


class PermissionTemplate(BaseSchema):
    """Permission template for quick assignment"""
    template_name: str = Field(..., description="Template name (e.g., 'Junior Supervisor', 'Senior Supervisor')")
    description: Optional[str] = None
    permissions: SupervisorPermissions = Field(..., description="Permission set")


class ApplyPermissionTemplate(BaseSchema):
    """Apply permission template to supervisor(s)"""
    supervisor_ids: List[UUID] = Field(..., min_items=1)
    template_name: str = Field(..., description="Template to apply")
    override_existing: bool = Field(True, description="Override existing permissions")