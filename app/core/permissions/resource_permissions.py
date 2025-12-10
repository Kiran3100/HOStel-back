"""
Resource-Level Permission Checks.

This module handles "Horizontal Privilege Escalation" protection.
It ensures users can only access data instances they own or manage.
"""

from typing import Any, Optional, Union
from app.core.enums import UserType
from app.core.exceptions.permission_exceptions import (
    HostelAccessDeniedException,
    UnauthorizedAccessException
)


class ResourcePermission:
    """
    Validates access to specific instances of resources.
    """

    def check_hostel_access(self, user: Any, target_hostel_id: str) -> bool:
        """
        Verify if the user is allowed to access/manage the specific hostel.
        """
        # Super Admins can access any hostel
        if user.user_type == UserType.SUPER_ADMIN:
            return True

        # Hostel Admins: Check if mapped to this hostel
        if user.user_type == UserType.HOSTEL_ADMIN:
            # Check direct assignment or many-to-many mapping
            if hasattr(user, "admin_hostel_mappings"):
                return any(str(m.hostel_id) == str(target_hostel_id) for m in user.admin_hostel_mappings)
            # Fallback for simple schema
            return str(getattr(user, "hostel_id", "")) == str(target_hostel_id)

        # Supervisors/Students: Must belong to the hostel
        user_hostel_id = getattr(user, "hostel_id", None)
        return str(user_hostel_id) == str(target_hostel_id)

    def check_user_access(self, requesting_user: Any, target_user_id: str, target_user_hostel_id: Optional[str] = None) -> bool:
        """
        Verify if requesting_user can access target_user's data.
        """
        # Accessing own data
        if str(requesting_user.id) == str(target_user_id):
            return True

        if requesting_user.user_type == UserType.SUPER_ADMIN:
            return True

        # If accessing another user, requester must have admin privileges over that user's hostel
        if target_user_hostel_id:
            return self.check_hostel_access(requesting_user, target_user_hostel_id)
            
        return False

    def check_booking_access(self, user: Any, booking: Any) -> bool:
        """
        Verify access to a booking.
        """
        # Owner of the booking
        if getattr(booking, "user_id", None) and str(booking.user_id) == str(user.id):
            return True
            
        # Visitor who made the booking
        if getattr(booking, "visitor_id", None) and str(booking.visitor_id) == str(user.id):
            return True

        # Admin of the hostel involved in the booking
        if hasattr(booking, "hostel_id"):
            return self.check_hostel_access(user, str(booking.hostel_id))
            
        return False

    def check_complaint_access(self, user: Any, complaint: Any) -> bool:
        """
        Verify access to a complaint.
        """
        # Student who filed it
        if str(complaint.student_id) == str(user.id):
            return True
            
        # Admin/Supervisor of the hostel
        return self.check_hostel_access(user, str(complaint.hostel_id))

    def validate_supervisor_scope(self, supervisor: Any, target_hostel_id: str):
        """
        Strict check to ensure supervisors don't act outside their hostel.
        Raises exception if invalid.
        """
        if supervisor.user_type != UserType.SUPERVISOR:
            return 
            
        if str(supervisor.hostel_id) != str(target_hostel_id):
            raise HostelAccessDeniedException(
                "Supervisor cannot perform actions outside their assigned hostel"
            )


# Global instance
resource_permission = ResourcePermission()