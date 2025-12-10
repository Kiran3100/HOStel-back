"""
Hostel selector UI schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema


class HostelSelectorResponse(BaseSchema):
    """Hostel selector dropdown data"""
    admin_id: UUID
    total_hostels: int
    active_hostel_id: Optional[UUID]
    
    hostels: List["HostelSelectorItem"]
    recent_hostels: List[UUID] = Field(default_factory=list, description="Recently accessed hostel IDs")
    favorite_hostels: List[UUID] = Field(default_factory=list, description="Favorite hostel IDs")


class HostelSelectorItem(BaseSchema):
    """Individual hostel item in selector"""
    hostel_id: UUID
    hostel_name: str
    hostel_city: str
    hostel_type: str
    
    # Visual indicators
    is_active: bool = Field(False, description="Currently active hostel")
    is_primary: bool = Field(False, description="Primary hostel for admin")
    is_favorite: bool = Field(False, description="Marked as favorite")
    
    # Quick stats
    occupancy_percentage: Decimal
    pending_bookings: int
    pending_complaints: int
    
    # Permission
    permission_level: str
    
    # Activity
    last_accessed: Optional[datetime]


class RecentHostels(BaseSchema):
    """Recently accessed hostels"""
    admin_id: UUID
    hostels: List["RecentHostelItem"]


class RecentHostelItem(BaseSchema):
    """Recent hostel item"""
    hostel_id: UUID
    hostel_name: str
    hostel_city: str
    last_accessed: datetime
    access_count: int = Field(..., description="Number of times accessed")


class FavoriteHostels(BaseSchema):
    """Favorite hostels"""
    admin_id: UUID
    hostels: List["FavoriteHostelItem"]


class FavoriteHostelItem(BaseSchema):
    """Favorite hostel item"""
    hostel_id: UUID
    hostel_name: str
    hostel_city: str
    added_to_favorites: datetime
    notes: Optional[str] = None


class UpdateFavoriteRequest(BaseSchema):
    """Add/remove hostel from favorites"""
    hostel_id: UUID
    is_favorite: bool
    notes: Optional[str] = Field(None, max_length=500)