"""
Visitor response schemas
"""
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import RoomType


class VisitorResponse(BaseResponseSchema):
    """Visitor response schema"""
    user_id: UUID
    full_name: str
    email: str
    phone: str
    
    # Preferences
    preferred_room_type: Optional[RoomType]
    budget_min: Optional[Decimal]
    budget_max: Optional[Decimal]
    preferred_cities: List[str]
    
    # Stats
    total_bookings: int = Field(0, description="Total bookings made")
    saved_hostels_count: int = Field(0, description="Number of saved hostels")
    
    # Notification preferences
    email_notifications: bool
    sms_notifications: bool
    push_notifications: bool


class VisitorProfile(BaseSchema):
    """Visitor public profile"""
    id: UUID
    user_id: UUID
    full_name: str
    profile_image_url: Optional[str]
    member_since: datetime


class VisitorDetail(BaseResponseSchema):
    """Detailed visitor information"""
    # User info
    user_id: UUID
    full_name: str
    email: str
    phone: str
    profile_image_url: Optional[str]
    
    # Preferences
    preferred_room_type: Optional[RoomType]
    budget_min: Optional[Decimal]
    budget_max: Optional[Decimal]
    preferred_cities: List[str]
    preferred_amenities: List[str]
    
    # Saved hostels
    favorite_hostel_ids: List[UUID]
    total_saved_hostels: int
    
    # Activity
    total_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    total_inquiries: int
    
    # Reviews
    total_reviews_written: int
    average_rating_given: Optional[Decimal]
    
    # Notification preferences
    email_notifications: bool
    sms_notifications: bool
    push_notifications: bool
    
    # Account info
    created_at: datetime
    last_login: Optional[datetime]


class VisitorStats(BaseSchema):
    """Visitor statistics"""
    visitor_id: UUID
    
    # Search activity
    total_searches: int
    unique_hostels_viewed: int
    average_search_filters_used: Decimal
    
    # Engagement
    total_hostel_views: int
    total_comparisons: int
    total_inquiries: int
    
    # Bookings
    total_bookings: int
    booking_conversion_rate: Decimal = Field(..., description="% of views that became bookings")
    
    # Preferences insight
    most_searched_city: Optional[str]
    most_viewed_room_type: Optional[RoomType]
    average_budget: Optional[Decimal]