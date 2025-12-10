"""
Visitor dashboard schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema


class VisitorDashboard(BaseSchema):
    """Visitor dashboard overview"""
    visitor_id: UUID
    visitor_name: str
    
    # Saved hostels
    saved_hostels: "SavedHostels"
    
    # Booking history
    booking_history: "BookingHistory"
    
    # Recent activity
    recent_searches: List["RecentSearch"] = Field(default_factory=list, max_items=5)
    recently_viewed: List["RecentlyViewedHostel"] = Field(default_factory=list, max_items=10)
    
    # Recommendations
    recommended_hostels: List["RecommendedHostel"] = Field(default_factory=list, max_items=5)
    
    # Alerts
    price_drop_alerts: List["PriceDropAlert"] = Field(default_factory=list)
    availability_alerts: List["AvailabilityAlert"] = Field(default_factory=list)
    
    # Stats
    total_searches: int
    total_hostel_views: int
    total_bookings: int


class SavedHostels(BaseSchema):
    """Saved/favorite hostels"""
    total_saved: int
    hostels: List["SavedHostelItem"] = Field(default_factory=list)


class SavedHostelItem(BaseSchema):
    """Individual saved hostel"""
    hostel_id: UUID
    hostel_name: str
    hostel_city: str
    starting_price: Decimal
    average_rating: Decimal
    available_beds: int
    cover_image_url: Optional[str]
    
    saved_at: datetime
    notes: Optional[str] = Field(None, description="Personal notes about this hostel")
    
    # Price tracking
    price_when_saved: Decimal
    current_price: Decimal
    price_changed: bool
    price_change_percentage: Optional[Decimal]


class BookingHistory(BaseSchema):
    """Booking history summary"""
    total_bookings: int
    active_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    
    bookings: List["BookingHistoryItem"] = Field(default_factory=list)


class BookingHistoryItem(BaseSchema):
    """Individual booking in history"""
    booking_id: UUID
    booking_reference: str
    hostel_id: UUID
    hostel_name: str
    room_type: str
    
    booking_date: datetime
    check_in_date: date
    duration_months: int
    
    status: str
    total_amount: Decimal
    
    # Actions
    can_cancel: bool
    can_modify: bool
    can_review: bool


class RecentSearch(BaseSchema):
    """Recent search item"""
    search_id: UUID
    search_query: Optional[str]
    filters_applied: dict
    results_count: int
    searched_at: datetime


class RecentlyViewedHostel(BaseSchema):
    """Recently viewed hostel"""
    hostel_id: UUID
    hostel_name: str
    hostel_city: str
    starting_price: Decimal
    average_rating: Decimal
    cover_image_url: Optional[str]
    
    viewed_at: datetime
    view_count: int = Field(..., description="Number of times viewed")


class RecommendedHostel(BaseSchema):
    """Recommended hostel based on preferences"""
    hostel_id: UUID
    hostel_name: str
    hostel_city: str
    starting_price: Decimal
    average_rating: Decimal
    available_beds: int
    cover_image_url: Optional[str]
    
    match_score: Decimal = Field(..., ge=0, le=100, description="How well it matches preferences")
    match_reasons: List[str] = Field(..., description="Why it's recommended")


class PriceDropAlert(BaseSchema):
    """Price drop alert"""
    alert_id: UUID
    hostel_id: UUID
    hostel_name: str
    
    previous_price: Decimal
    new_price: Decimal
    discount_percentage: Decimal
    
    alert_created: datetime
    is_read: bool


class AvailabilityAlert(BaseSchema):
    """Availability alert"""
    alert_id: UUID
    hostel_id: UUID
    hostel_name: str
    room_type: str
    
    message: str
    
    alert_created: datetime
    is_read: bool