"""
Visitor schemas package
"""
from app.schemas.visitor.visitor_base import (
    VisitorBase,
    VisitorCreate,
    VisitorUpdate
)
from app.schemas.visitor.visitor_response import (
    VisitorResponse,
    VisitorProfile,
    VisitorDetail
)
from app.schemas.visitor.visitor_preferences import (
    VisitorPreferences,
    PreferenceUpdate,
    SearchPreferences
)
from app.schemas.visitor.visitor_dashboard import (
    VisitorDashboard,
    SavedHostels,
    BookingHistory
)
from app.schemas.visitor.visitor_favorites import (
    FavoriteRequest,
    FavoritesList,
    FavoriteHostelItem
)

__all__ = [
    # Base
    "VisitorBase",
    "VisitorCreate",
    "VisitorUpdate",
    
    # Response
    "VisitorResponse",
    "VisitorProfile",
    "VisitorDetail",
    
    # Preferences
    "VisitorPreferences",
    "PreferenceUpdate",
    "SearchPreferences",
    
    # Dashboard
    "VisitorDashboard",
    "SavedHostels",
    "BookingHistory",
    
    # Favorites
    "FavoriteRequest",
    "FavoritesList",
    "FavoriteHostelItem",
]