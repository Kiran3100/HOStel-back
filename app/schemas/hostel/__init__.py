"""
Hostel schemas package
"""
from app.schemas.hostel.hostel_base import (
    HostelBase,
    HostelCreate,
    HostelUpdate
)
from app.schemas.hostel.hostel_response import (
    HostelResponse,
    HostelDetail,
    HostelListItem,
    HostelStats
)
from app.schemas.hostel.hostel_public import (
    PublicHostelProfile,
    PublicHostelList,
    PublicHostelCard
)
from app.schemas.hostel.hostel_admin import (
    HostelAdminView,
    HostelSettings,
    HostelVisibilityUpdate
)
from app.schemas.hostel.hostel_search import (
    HostelSearchRequest,
    HostelSearchResponse,
    HostelSearchFilters
)
from app.schemas.hostel.hostel_filter import (
    HostelFilterParams,
    HostelSortOptions,
    AdvancedFilters
)
from app.schemas.hostel.hostel_analytics import (
    HostelAnalytics,
    HostelOccupancyStats,
    HostelRevenueStats
)
from app.schemas.hostel.hostel_comparison import (
    HostelComparisonRequest,
    ComparisonResult,
    ComparisonItem
)

__all__ = [
    # Base
    "HostelBase",
    "HostelCreate",
    "HostelUpdate",
    
    # Response
    "HostelResponse",
    "HostelDetail",
    "HostelListItem",
    "HostelStats",
    
    # Public
    "PublicHostelProfile",
    "PublicHostelList",
    "PublicHostelCard",
    
    # Admin
    "HostelAdminView",
    "HostelSettings",
    "HostelVisibilityUpdate",
    
    # Search
    "HostelSearchRequest",
    "HostelSearchResponse",
    "HostelSearchFilters",
    
    # Filter
    "HostelFilterParams",
    "HostelSortOptions",
    "AdvancedFilters",
    
    # Analytics
    "HostelAnalytics",
    "HostelOccupancyStats",
    "HostelRevenueStats",
    
    # Comparison
    "HostelComparisonRequest",
    "ComparisonResult",
    "ComparisonItem",
]