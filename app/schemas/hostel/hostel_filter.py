"""
Hostel filter and sort schemas
"""
from decimal import Decimal
from typing import List, Optional
from pydantic import Field

from app.schemas.common.base import BaseFilterSchema
from app.schemas.common.enums import HostelType, HostelStatus


class HostelFilterParams(BaseFilterSchema):
    """Hostel listing filter parameters"""
    # Text search
    search: Optional[str] = Field(None, description="Search in name, description")
    
    # Location
    city: Optional[str] = None
    state: Optional[str] = None
    cities: Optional[List[str]] = Field(None, description="Filter by multiple cities")
    
    # Type
    hostel_type: Optional[HostelType] = None
    hostel_types: Optional[List[HostelType]] = None
    
    # Status
    status: Optional[HostelStatus] = None
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_verified: Optional[bool] = None
    
    # Price range
    price_min: Optional[Decimal] = Field(None, ge=0)
    price_max: Optional[Decimal] = Field(None, ge=0)
    
    # Rating
    min_rating: Optional[Decimal] = Field(None, ge=0, le=5)
    
    # Availability
    has_availability: Optional[bool] = None
    min_available_beds: Optional[int] = Field(None, ge=0)
    
    # Amenities
    amenities: Optional[List[str]] = None
    
    # Admin filters
    admin_id: Optional[UUID] = Field(None, description="Filter by assigned admin")
    has_subscription: Optional[bool] = None


class HostelSortOptions(BaseFilterSchema):
    """Hostel sorting options"""
    sort_by: str = Field(
        "created_at",
        pattern="^(name|city|price|rating|occupancy|created_at|updated_at)$"
    )
    sort_order: str = Field("desc", pattern="^(asc|desc)$")


class AdvancedFilters(BaseFilterSchema):
    """Advanced filtering options"""
    # Date filters
    created_after: Optional[date] = None
    created_before: Optional[date] = None
    
    # Occupancy
    occupancy_min: Optional[Decimal] = Field(None, ge=0, le=100)
    occupancy_max: Optional[Decimal] = Field(None, ge=0, le=100)
    
    # Reviews
    min_reviews: Optional[int] = Field(None, ge=0)
    
    # Rooms
    min_rooms: Optional[int] = Field(None, ge=0)
    max_rooms: Optional[int] = Field(None, ge=0)
    
    # Revenue (admin only)
    revenue_min: Optional[Decimal] = Field(None, ge=0)
    revenue_max: Optional[Decimal] = Field(None, ge=0)


class BulkFilterParams(BaseFilterSchema):
    """Bulk operation filter parameters"""
    hostel_ids: List[UUID] = Field(..., min_items=1, description="List of hostel IDs")
    
    # Or use filters
    use_filters: bool = Field(False, description="Use filter criteria instead of IDs")
    filters: Optional[HostelFilterParams] = None