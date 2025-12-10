"""
Permission Matrix Definition.

This module acts as the Single Source of Truth for static role capabilities.
It uses a 'Resource:Action' string format (e.g., 'booking:create').
"""

from typing import Set, Dict
from app.core.enums import UserType

# ==================== Action Constants ====================
ACTION_CREATE = "create"
ACTION_READ = "read"
ACTION_UPDATE = "update"
ACTION_DELETE = "delete"
ACTION_LIST = "list"
ACTION_APPROVE = "approve"
ACTION_REJECT = "reject"
ACTION_EXPORT = "export"
ACTION_IMPORT = "import"
ACTION_MANAGE = "manage"  # Grants all actions for a resource

# ==================== Resource Constants ====================
RESOURCE_SYSTEM = "system"
RESOURCE_HOSTEL = "hostel"
RESOURCE_ROOM = "room"
RESOURCE_BED = "bed"
RESOURCE_STUDENT = "student"
RESOURCE_STAFF = "staff"
RESOURCE_VISITOR = "visitor"
RESOURCE_BOOKING = "booking"
RESOURCE_PAYMENT = "payment"
RESOURCE_COMPLAINT = "complaint"
RESOURCE_MAINTENANCE = "maintenance"
RESOURCE_ATTENDANCE = "attendance"
RESOURCE_NOTICE = "notice"
RESOURCE_MENU = "menu"
RESOURCE_REVIEW = "review"
RESOURCE_REPORT = "report"
RESOURCE_AUDIT = "audit"
RESOURCE_SETTINGS = "settings"


class PermissionMatrix:
    """
    Defines the default permission sets for each UserType.
    """

    # Super Admin has access to everything via wildcards
    SUPER_ADMIN_PERMISSIONS: Set[str] = {"*:*"}

    # Hostel Admin: Full control over their specific hostel operations
    HOSTEL_ADMIN_PERMISSIONS: Set[str] = {
        # Hostel Info
        f"{RESOURCE_HOSTEL}:{ACTION_READ}",
        f"{RESOURCE_HOSTEL}:{ACTION_UPDATE}",
        
        # Infrastructure
        f"{RESOURCE_ROOM}:{ACTION_MANAGE}",
        f"{RESOURCE_BED}:{ACTION_MANAGE}",
        
        # User Management (within their hostel)
        f"{RESOURCE_STUDENT}:{ACTION_MANAGE}",
        f"{RESOURCE_STAFF}:{ACTION_MANAGE}",
        
        # Operations
        f"{RESOURCE_BOOKING}:{ACTION_MANAGE}",
        f"{RESOURCE_PAYMENT}:{ACTION_MANAGE}",
        f"{RESOURCE_COMPLAINT}:{ACTION_MANAGE}",
        f"{RESOURCE_MAINTENANCE}:{ACTION_MANAGE}",
        f"{RESOURCE_ATTENDANCE}:{ACTION_MANAGE}",
        f"{RESOURCE_NOTICE}:{ACTION_MANAGE}",
        f"{RESOURCE_MENU}:{ACTION_MANAGE}",
        
        # Analytics & Reports
        f"{RESOURCE_REPORT}:{ACTION_MANAGE}",
        f"{RESOURCE_AUDIT}:{ACTION_READ}",
        f"{RESOURCE_REVIEW}:{ACTION_READ}",
        f"{RESOURCE_REVIEW}:{ACTION_UPDATE}",  # Reply to reviews
    }

    # Supervisor: Operational management, but limited administrative power
    SUPERVISOR_PERMISSIONS: Set[str] = {
        # Read Infrastructure
        f"{RESOURCE_HOSTEL}:{ACTION_READ}",
        f"{RESOURCE_ROOM}:{ACTION_READ}",
        f"{RESOURCE_BED}:{ACTION_READ}",
        
        # Student Operations
        f"{RESOURCE_STUDENT}:{ACTION_READ}",
        f"{RESOURCE_STUDENT}:{ACTION_LIST}",
        
        # Complaints & Maintenance (Core duties)
        f"{RESOURCE_COMPLAINT}:{ACTION_MANAGE}",
        f"{RESOURCE_MAINTENANCE}:{ACTION_CREATE}",
        f"{RESOURCE_MAINTENANCE}:{ACTION_READ}",
        f"{RESOURCE_MAINTENANCE}:{ACTION_UPDATE}",
        f"{RESOURCE_MAINTENANCE}:{ACTION_APPROVE}",  # Subject to cost thresholds
        
        # Attendance
        f"{RESOURCE_ATTENDANCE}:{ACTION_MANAGE}",
        
        # Notices
        f"{RESOURCE_NOTICE}:{ACTION_CREATE}",
        f"{RESOURCE_NOTICE}:{ACTION_READ}",
        
        # Menu
        f"{RESOURCE_MENU}:{ACTION_READ}",
    }

    # Student: Self-service portal access
    STUDENT_PERMISSIONS: Set[str] = {
        # Self Profile
        f"{RESOURCE_STUDENT}:{ACTION_READ}",
        
        # Payments
        f"{RESOURCE_PAYMENT}:{ACTION_READ}",
        f"{RESOURCE_PAYMENT}:{ACTION_CREATE}",
        
        # Complaints
        f"{RESOURCE_COMPLAINT}:{ACTION_CREATE}",
        f"{RESOURCE_COMPLAINT}:{ACTION_READ}",
        
        # Services
        f"{RESOURCE_ATTENDANCE}:{ACTION_READ}",
        f"{RESOURCE_MENU}:{ACTION_READ}",
        f"{RESOURCE_NOTICE}:{ACTION_READ}",
        f"{RESOURCE_ROOM}:{ACTION_READ}",  # View own room details
        
        # Reviews
        f"{RESOURCE_REVIEW}:{ACTION_CREATE}",
        f"{RESOURCE_REVIEW}:{ACTION_READ}",
    }

    # Visitor: Public access and booking creation
    VISITOR_PERMISSIONS: Set[str] = {
        f"{RESOURCE_HOSTEL}:{ACTION_LIST}",
        f"{RESOURCE_HOSTEL}:{ACTION_READ}",
        f"{RESOURCE_BOOKING}:{ACTION_CREATE}",
        f"{RESOURCE_BOOKING}:{ACTION_READ}",
        f"{RESOURCE_REVIEW}:{ACTION_READ}",
    }

    @classmethod
    def get_permissions_for_role(cls, role: UserType) -> Set[str]:
        """
        Retrieve the set of static permissions for a given role.
        """
        mapping = {
            UserType.SUPER_ADMIN: cls.SUPER_ADMIN_PERMISSIONS,
            UserType.HOSTEL_ADMIN: cls.HOSTEL_ADMIN_PERMISSIONS,
            UserType.SUPERVISOR: cls.SUPERVISOR_PERMISSIONS,
            UserType.STUDENT: cls.STUDENT_PERMISSIONS,
            UserType.VISITOR: cls.VISITOR_PERMISSIONS,
        }
        return mapping.get(role, set())