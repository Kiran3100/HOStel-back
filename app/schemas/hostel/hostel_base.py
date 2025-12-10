"""
Hostel base schemas
"""
from decimal import Decimal
from datetime import time
from typing import List, Optional
from pydantic import Field, HttpUrl, field_validator
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import HostelType, HostelStatus
from app.schemas.common.mixins import AddressMixin, ContactMixin, LocationMixin


class HostelBase(BaseSchema, AddressMixin, ContactMixin, LocationMixin):
    """Base hostel schema with common fields"""
    name: str = Field(..., min_length=3, max_length=255, description="Hostel name")
    slug: str = Field(..., min_length=3, max_length=255, pattern=r'^[a-z0-9-]+$', description="URL-friendly slug")
    description: Optional[str] = Field(None, max_length=2000, description="Hostel description")
    
    # Type
    hostel_type: HostelType = Field(..., description="Hostel type (boys/girls/co-ed)")
    
    # Website
    website_url: Optional[HttpUrl] = Field(None, description="Hostel website URL")
    
    # Pricing
    starting_price_monthly: Optional[Decimal] = Field(
        None,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Starting monthly price"
    )
    currency: str = Field("INR", min_length=3, max_length=3, description="Currency code")
    
    # Amenities and facilities (JSON arrays)
    amenities: List[str] = Field(default_factory=list, description="List of amenities")
    facilities: List[str] = Field(default_factory=list, description="List of facilities")
    security_features: List[str] = Field(default_factory=list, description="Security features")
    
    # Policies
    rules: Optional[str] = Field(None, max_length=5000, description="Hostel rules and regulations")
    check_in_time: Optional[time] = Field(None, description="Standard check-in time")
    check_out_time: Optional[time] = Field(None, description="Standard check-out time")
    visitor_policy: Optional[str] = Field(None, max_length=1000, description="Visitor policy")
    late_entry_policy: Optional[str] = Field(None, max_length=1000, description="Late entry policy")
    
    # Location info
    nearby_landmarks: List[dict] = Field(
        default_factory=list,
        description="Nearby landmarks with name and distance"
    )
    connectivity_info: Optional[str] = Field(None, max_length=1000, description="Connectivity information")
    
    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Validate slug format"""
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('Slug can only contain lowercase letters, numbers, and hyphens')
        return v.lower()
    
    @field_validator('amenities', 'facilities', 'security_features')
    @classmethod
    def validate_lists_not_empty(cls, v: List[str]) -> List[str]:
        """Remove empty strings from lists"""
        return [item.strip() for item in v if item.strip()]


class HostelCreate(HostelBase, BaseCreateSchema):
    """Schema for creating a hostel"""
    # Override to make certain fields required
    name: str = Field(..., min_length=3, max_length=255)
    hostel_type: HostelType = Field(...)
    contact_phone: str = Field(...)


class HostelUpdate(BaseUpdateSchema):
    """Schema for updating a hostel (all fields optional)"""
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    slug: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    hostel_type: Optional[HostelType] = None
    
    # Address fields
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    country: Optional[str] = None
    
    # Contact
    contact_phone: Optional[str] = None
    alternate_phone: Optional[str] = None
    contact_email: Optional[str] = None
    
    # Location
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180)
    
    # Pricing
    starting_price_monthly: Optional[Decimal] = Field(None, ge=0)
    
    # Lists
    amenities: Optional[List[str]] = None
    facilities: Optional[List[str]] = None
    security_features: Optional[List[str]] = None
    
    # Policies
    rules: Optional[str] = None
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None
    
    # Media
    cover_image_url: Optional[str] = None
    gallery_images: Optional[List[str]] = None
    virtual_tour_url: Optional[str] = None
    
    # Status
    status: Optional[HostelStatus] = None
    is_active: Optional[bool] = None


class HostelMediaUpdate(BaseUpdateSchema):
    """Update hostel media (images, videos)"""
    cover_image_url: Optional[str] = Field(None, description="Cover image URL")
    gallery_images: List[str] = Field(default_factory=list, description="Gallery image URLs")
    virtual_tour_url: Optional[HttpUrl] = Field(None, description="Virtual tour URL")


class HostelSEOUpdate(BaseUpdateSchema):
    """Update hostel SEO metadata"""
    meta_title: Optional[str] = Field(None, max_length=255, description="SEO meta title")
    meta_description: Optional[str] = Field(None, max_length=500, description="SEO meta description")
    meta_keywords: Optional[str] = Field(None, max_length=500, description="SEO keywords (comma-separated)")