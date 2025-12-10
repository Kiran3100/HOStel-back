"""
Hostel search schemas
"""
from decimal import Decimal
from typing import List, Optional
from pydantic import Field

from app.schemas.common.base import BaseSchema, BaseFilterSchema
from app.schemas.common.enums import HostelType, RoomType
from app.schemas.hostel.hostel_public import PublicHostelCard


class HostelSearchRequest(BaseFilterSchema):
    """Hostel search request"""
    # Text search
    query: Optional[str] = Field(None, min_length=1, max_length=255, description="Search query")
    
    # Location filters
    city: Optional[str] = Field(None, description="City name")
    state: Optional[str] = Field(None, description="State name")
    pincode: Optional[str] = Field(None, pattern=r'^\d{6}$', description="Pincode")
    
    # Location-based search
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90, description="Latitude for radius search")
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180, description="Longitude for radius search")
    radius_km: Optional[Decimal] = Field(None, ge=0, le=50, description="Search radius in km")
    
    # Type filter
    hostel_type: Optional[HostelType] = Field(None, description="Hostel type filter")
    
    # Price filter
    min_price: Optional[Decimal] = Field(None, ge=0, description="Minimum monthly price")
    max_price: Optional[Decimal] = Field(None, ge=0, description="Maximum monthly price")
    
    # Room type
    room_type: Optional[RoomType] = Field(None, description="Preferred room type")
    
    # Amenities filter
    amenities: Optional[List[str]] = Field(None, description="Required amenities")
    
    # Availability
    available_beds_min: Optional[int] = Field(None, ge=0, description="Minimum available beds")
    
    # Rating filter
    min_rating: Optional[Decimal] = Field(None, ge=0, le=5, description="Minimum rating")
    
    # Features
    verified_only: bool = Field(False, description="Show only verified hostels")
    featured_only: bool = Field(False, description="Show only featured hostels")
    
    # Sort
    sort_by: str = Field(
        "relevance",
        pattern="^(relevance|price_low|price_high|rating|distance|newest)$",
        description="Sort criteria"
    )
    
    # Pagination
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Results per page")


class HostelSearchResponse(BaseSchema):
    """Hostel search response"""
    results: List[PublicHostelCard] = Field(..., description="Search results")
    total_results: int = Field(..., description="Total matching hostels")
    total_pages: int = Field(..., description="Total pages")
    current_page: int = Field(..., description="Current page")
    filters_applied: dict = Field(..., description="Applied filters summary")
    facets: "SearchFacets" = Field(..., description="Available filter facets")


class SearchFacets(BaseSchema):
    """Search facets for filtering"""
    cities: List["FacetItem"] = Field(default_factory=list, description="Available cities with counts")
    hostel_types: List["FacetItem"] = Field(default_factory=list, description="Hostel types with counts")
    price_ranges: List["PriceRangeFacet"] = Field(default_factory=list, description="Price ranges")
    amenities: List["FacetItem"] = Field(default_factory=list, description="Available amenities")
    ratings: List["RatingFacet"] = Field(default_factory=list, description="Rating distribution")


class FacetItem(BaseSchema):
    """Facet item with count"""
    value: str = Field(..., description="Facet value")
    label: str = Field(..., description="Display label")
    count: int = Field(..., description="Number of results")


class PriceRangeFacet(BaseSchema):
    """Price range facet"""
    min_price: Decimal
    max_price: Decimal
    label: str
    count: int


class RatingFacet(BaseSchema):
    """Rating facet"""
    min_rating: Decimal
    label: str
    count: int


class HostelSearchFilters(BaseFilterSchema):
    """Advanced search filters"""
    # Gender
    gender: Optional[str] = Field(None, pattern="^(boys|girls|co_ed)$", description="Gender preference")
    
    # Facilities
    has_wifi: Optional[bool] = None
    has_ac: Optional[bool] = None
    has_laundry: Optional[bool] = None
    has_parking: Optional[bool] = None
    has_gym: Optional[bool] = None
    has_mess: Optional[bool] = None
    
    # Security
    has_cctv: Optional[bool] = None
    has_security_guard: Optional[bool] = None
    
    # Rules
    allow_visitors: Optional[bool] = None
    
    # Availability
    check_in_date: Optional[date] = Field(None, description="Desired check-in date")