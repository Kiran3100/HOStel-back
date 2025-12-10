"""
Approval Authority & Threshold Management.

This module enforces financial and operational limits on roles.
"""

from typing import Any
from app.core.config import settings
from app.core.enums import UserType


class ApprovalAuthority:
    """
    Determines if a user has sufficient authority to approve specific requests
    based on cost or impact thresholds.
    """

    def can_approve_complaint_cost(self, user: Any, estimated_cost: float) -> bool:
        """
        Check if user can approve a complaint resolution based on cost.
        """
        # Admins have no limits (or very high limits)
        if user.user_type in [UserType.SUPER_ADMIN, UserType.HOSTEL_ADMIN]:
            return True
            
        # Supervisors have limits defined in settings
        if user.user_type == UserType.SUPERVISOR:
            limit = settings.SUPERVISOR_COMPLAINT_APPROVAL_THRESHOLD
            return estimated_cost <= limit
            
        return False

    def can_approve_maintenance_cost(self, user: Any, estimated_cost: float) -> bool:
        """
        Check if user can approve a maintenance request based on cost.
        """
        if user.user_type in [UserType.SUPER_ADMIN, UserType.HOSTEL_ADMIN]:
            return True
            
        if user.user_type == UserType.SUPERVISOR:
            limit = settings.SUPERVISOR_MAINTENANCE_APPROVAL_THRESHOLD
            return estimated_cost <= limit
            
        return False

    def requires_escalation(self, user: Any, cost: float, context: str) -> bool:
        """
        Helper to determine if a request needs to go up the chain.
        
        Args:
            user: The user attempting to approve
            cost: The monetary value
            context: 'complaint' or 'maintenance'
        """
        if context == "complaint":
            return not self.can_approve_complaint_cost(user, cost)
        elif context == "maintenance":
            return not self.can_approve_maintenance_cost(user, cost)
        return True


# Global instance
approval_authority = ApprovalAuthority()