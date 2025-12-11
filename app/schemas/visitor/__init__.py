"""
Visitor schemas package

This package contains all Pydantic schemas related to visitor operations,
preferences, dashboard, favorites, and responses. All schemas have been
enhanced with comprehensive validation, computed fields, and helper methods.

The package is organized into:
- Base schemas: Core visitor models (create, update)
- Response schemas: API response models
- Preferences: User preference management
- Dashboard: Dashboard and overview data
- Favorites: Saved/favorite hostel management
"""

from app.schemas.visitor.visitor_base import (
    VisitorBase,
    VisitorCreate,
    VisitorUpdate
)
from app.schemas.visitor.visitor_response import (
    VisitorResponse,
    VisitorProfile,
    VisitorDetail,
    VisitorStats
)
from app.schemas.visitor.visitor_preferences import (
    VisitorPreferences,
    PreferenceUpdate,
    SearchPreferences,
    SavedSearch
)
from app.schemas.visitor.visitor_dashboard import (
    VisitorDashboard,
    SavedHostels,
    SavedHostelItem,
    BookingHistory,
    BookingHistoryItem,
    RecentSearch,
    RecentlyViewedHostel,
    RecommendedHostel,
    PriceDropAlert,
    AvailabilityAlert
)
from app.schemas.visitor.visitor_favorites import (
    FavoriteRequest,
    FavoritesList,
    FavoriteHostelItem,
    FavoriteUpdate,
    FavoritesExport,
    FavoriteComparison
)

__all__ = [
    # Base schemas
    "VisitorBase",
    "VisitorCreate",
    "VisitorUpdate",
    
    # Response schemas
    "VisitorResponse",
    "VisitorProfile",
    "VisitorDetail",
    "VisitorStats",
    
    # Preferences
    "VisitorPreferences",
    "PreferenceUpdate",
    "SearchPreferences",
    "SavedSearch",
    
    # Dashboard
    "VisitorDashboard",
    "SavedHostels",
    "SavedHostelItem",
    "BookingHistory",
    "BookingHistoryItem",
    "RecentSearch",
    "RecentlyViewedHostel",
    "RecommendedHostel",
    "PriceDropAlert",
    "AvailabilityAlert",
    
    # Favorites
    "FavoriteRequest",
    "FavoritesList",
    "FavoriteHostelItem",
    "FavoriteUpdate",
    "FavoritesExport",
    "FavoriteComparison",
]

