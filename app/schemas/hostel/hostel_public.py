"""
Public hostel profile schemas (for visitors)
"""
from decimal import Decimal
from datetime import time
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.enums import HostelType


class PublicHostelCard(BaseSchema):
    """Hostel card for public listing"""
    id: UUID
    name: str
    slug: str
    hostel_type: HostelType
    city: str
    state: str
    starting_price_monthly: Decimal
    currency: str
    average_rating: Decimal
    total_reviews: int
    available_beds: int
    cover_image_url: Optional[str]
    is_featured: bool
    amenities: List[str] = Field(default_factory=list, max_items=5, description="Top 5 amenities")
    distance_km: Optional[Decimal] = Field(None, description="Distance from search location")


class PublicHostelProfile(BaseSchema):
    """Complete public hostel profile"""
    id: UUID
    name: str
    slug: str
    description: Optional[str]
    hostel_type: HostelType
    
    # Contact (public)
    contact_phone: str
    contact_email: Optional[str]
    website_url: Optional[str]
    
    # Address
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    pincode: str
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    
    # Pricing
    starting_price_monthly: Decimal
    currency: str
    
    # Availability
    available_beds: int
    
    # Ratings
    average_rating: Decimal
    total_reviews: int
    rating_breakdown: dict = Field(
        ...,
        description="Rating distribution {1: count, 2: count, ...}"
    )
    
    # Features
    amenities: List[str]
    facilities: List[str]
    security_features: List[str]
    
    # Policies
    rules: Optional[str]
    check_in_time: Optional[time]
    check_out_time: Optional[time]
    visitor_policy: Optional[str]
    
    # Location
    nearby_landmarks: List[dict]
    connectivity_info: Optional[str]
    
    # Media
    cover_image_url: Optional[str]
    gallery_images: List[str]
    virtual_tour_url: Optional[str]
    
    # Room types available
    room_types: List["PublicRoomType"]


class PublicRoomType(BaseSchema):
    """Public room type information"""
    room_type: str
    price_monthly: Decimal
    price_quarterly: Optional[Decimal]
    price_yearly: Optional[Decimal]
    available_beds: int
    total_beds: int
    room_amenities: List[str]
    room_images: List[str]


class PublicHostelList(BaseSchema):
    """List of public hostels"""
    hostels: List[PublicHostelCard]
    total_count: int
    filters_applied: dict