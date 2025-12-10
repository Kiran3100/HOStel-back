"""
Admin schemas package
"""
from app.schemas.admin.admin_hostel_assignment import (
    AdminHostelAssignment,
    AssignmentCreate,
    AssignmentUpdate,
    BulkAssignment
)
from app.schemas.admin.hostel_context import (
    HostelContext,
    HostelSwitchRequest,
    ActiveHostelResponse
)
from app.schemas.admin.hostel_selector import (
    HostelSelectorResponse,
    HostelSelectorItem,
    RecentHostels,
    FavoriteHostels
)
from app.schemas.admin.multi_hostel_dashboard import (
    MultiHostelDashboard,
    AggregatedStats,
    HostelQuickStats,
    CrossHostelComparison
)
from app.schemas.admin.admin_override import (
    AdminOverrideRequest,
    OverrideLog,
    OverrideReason
)
from app.schemas.admin.admin_permissions import (
    AdminPermissions,
    PermissionMatrix,
    RolePermissions
)

__all__ = [
    # Hostel Assignment
    "AdminHostelAssignment",
    "AssignmentCreate",
    "AssignmentUpdate",
    "BulkAssignment",
    
    # Hostel Context
    "HostelContext",
    "HostelSwitchRequest",
    "ActiveHostelResponse",
    
    # Hostel Selector
    "HostelSelectorResponse",
    "HostelSelectorItem",
    "RecentHostels",
    "FavoriteHostels",
    
    # Multi-Hostel Dashboard
    "MultiHostelDashboard",
    "AggregatedStats",
    "HostelQuickStats",
    "CrossHostelComparison",
    
    # Admin Override
    "AdminOverrideRequest",
    "OverrideLog",
    "OverrideReason",
    
    # Permissions
    "AdminPermissions",
    "PermissionMatrix",
    "RolePermissions",
]