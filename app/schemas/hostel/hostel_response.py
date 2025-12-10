"""
Hostel response schemas
"""
from decimal import Decimal
from datetime import datetime, time
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import HostelType, HostelStatus


class HostelResponse(BaseResponseSchema):
    """Basic hostel response"""
    name: str = Field(..., description="Hostel name")
    slug: str = Field(..., description="URL slug")
    hostel_type: HostelType = Field(..., description="Hostel type")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    starting_price_monthly: Optional[Decimal] = Field(None, description="Starting price")
    average_rating: Decimal = Field(..., description="Average rating")
    total_reviews: int = Field(..., description="Total reviews")
    total_rooms: int = Field(..., description="Total rooms")
    available_beds: int = Field(..., description="Available beds")
    is_public: bool = Field(..., description="Public visibility")
    is_featured: bool = Field(..., description="Featured status")
    cover_image_url: Optional[str] = Field(None, description="Cover image")
    status: HostelStatus = Field(..., description="Operational status")


class HostelDetail(BaseResponseSchema):
    """Detailed hostel information"""
    name: str
    slug: str
    description: Optional[str]
    
    # Type and contact
    hostel_type: HostelType
    contact_email: Optional[str]
    contact_phone: str
    alternate_phone: Optional[str]
    website_url: Optional[str]
    
    # Address
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    pincode: str
    country: str
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    
    # Pricing
    starting_price_monthly: Optional[Decimal]
    currency: str
    
    # Capacity
    total_rooms: int
    total_beds: int
    occupied_beds: int
    available_beds: int
    
    # Ratings
    average_rating: Decimal
    total_reviews: int
    
    # Features
    amenities: List[str]
    facilities: List[str]
    security_features: List[str]
    
    # Policies
    rules: Optional[str]
    check_in_time: Optional[time]
    check_out_time: Optional[time]
    visitor_policy: Optional[str]
    late_entry_policy: Optional[str]
    
    # Location info
    nearby_landmarks: List[dict]
    connectivity_info: Optional[str]
    
    # Media
    cover_image_url: Optional[str]
    gallery_images: List[str]
    virtual_tour_url: Optional[str]
    
    # Status
    is_public: bool
    is_featured: bool
    is_verified: bool
    status: HostelStatus
    is_active: bool
    
    # SEO
    meta_title: Optional[str]
    meta_description: Optional[str]


class HostelListItem(BaseSchema):
    """Hostel list item (minimal info for lists)"""
    id: UUID
    name: str
    slug: str
    hostel_type: HostelType
    city: str
    state: str
    starting_price_monthly: Optional[Decimal]
    average_rating: Decimal
    total_reviews: int
    available_beds: int
    cover_image_url: Optional[str]
    is_featured: bool
    distance_km: Optional[Decimal] = Field(None, description="Distance from search location")


class HostelStats(BaseSchema):
    """Hostel statistics"""
    hostel_id: UUID
    
    # Occupancy
    total_rooms: int
    total_beds: int
    occupied_beds: int
    available_beds: int
    occupancy_percentage: Decimal
    
    # Revenue
    total_revenue_monthly: Decimal
    total_outstanding: Decimal
    
    # Students
    total_students: int
    active_students: int
    
    # Complaints
    open_complaints: int
    resolved_complaints: int
    
    # Bookings
    pending_bookings: int
    confirmed_bookings: int
    
    # Reviews
    average_rating: Decimal
    total_reviews: int
    
    # Last updated
    updated_at: datetime