"""
Visitor favorites/wishlist schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class FavoriteRequest(BaseCreateSchema):
    """Add/remove hostel from favorites"""
    hostel_id: UUID = Field(..., description="Hostel ID")
    is_favorite: bool = Field(..., description="Add (true) or remove (false)")
    notes: Optional[str] = Field(None, max_length=500, description="Personal notes")


class FavoritesList(BaseSchema):
    """List of favorite hostels"""
    visitor_id: UUID
    total_favorites: int
    favorites: List["FavoriteHostelItem"]


class FavoriteHostelItem(BaseSchema):
    """Individual favorite hostel"""
    favorite_id: UUID
    hostel_id: UUID
    hostel_name: str
    hostel_slug: str
    hostel_city: str
    hostel_type: str
    
    # Pricing
    starting_price_monthly: Decimal
    price_when_saved: Decimal
    current_price: Decimal
    has_price_drop: bool
    price_drop_percentage: Optional[Decimal]
    
    # Availability
    available_beds: int
    has_availability: bool
    
    # Rating
    average_rating: Decimal
    total_reviews: int
    
    # Media
    cover_image_url: Optional[str]
    
    # Favorite metadata
    notes: Optional[str]
    added_to_favorites: datetime
    
    # Tracking
    times_viewed: int
    last_viewed: Optional[datetime]


class FavoriteUpdate(BaseCreateSchema):
    """Update favorite notes"""
    favorite_id: UUID
    notes: str = Field(..., max_length=500)


class FavoritesExport(BaseSchema):
    """Export favorites list"""
    format: str = Field("pdf", pattern="^(pdf|csv|json)$")
    include_prices: bool = Field(True)
    include_notes: bool = Field(True)


class FavoriteComparison(BaseSchema):
    """Compare favorite hostels"""
    favorite_ids: List[UUID] = Field(..., min_items=2, max_items=4, description="2-4 favorites to compare")