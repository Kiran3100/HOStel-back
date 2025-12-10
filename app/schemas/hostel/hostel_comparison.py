"""
Hostel comparison schemas
"""
from decimal import Decimal
from typing import List, Optional
from pydantic import Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.enums import HostelType


class HostelComparisonRequest(BaseCreateSchema):
    """Request to compare hostels"""
    hostel_ids: List[UUID] = Field(..., min_items=2, max_items=4, description="2-4 hostel IDs to compare")
    
    @field_validator('hostel_ids')
    @classmethod
    def validate_unique_ids(cls, v: List[UUID]) -> List[UUID]:
        """Ensure hostel IDs are unique"""
        if len(v) != len(set(v)):
            raise ValueError('Hostel IDs must be unique')
        return v


class ComparisonResult(BaseSchema):
    """Comparison result with all hostels"""
    hostels: List["ComparisonItem"] = Field(..., description="Hostels being compared")
    comparison_criteria: List[str] = Field(..., description="Criteria included in comparison")
    generated_at: datetime = Field(..., description="Comparison generation timestamp")


class ComparisonItem(BaseSchema):
    """Individual hostel comparison data"""
    id: UUID
    name: str
    slug: str
    hostel_type: HostelType
    
    # Location
    city: str
    state: str
    address: str
    distance_from_center_km: Optional[Decimal] = None
    
    # Pricing
    starting_price_monthly: Decimal
    price_range_monthly: str = Field(..., description="e.g., '₹5,000 - ₹15,000'")
    security_deposit: Optional[Decimal] = None
    
    # Capacity
    total_beds: int
    available_beds: int
    
    # Ratings
    average_rating: Decimal
    total_reviews: int
    rating_breakdown: Dict[str, int]
    
    # Amenities
    amenities: List[str]
    facilities: List[str]
    security_features: List[str]
    
    # Room types
    room_types_available: List[str]
    room_type_details: List["RoomTypeComparison"]
    
    # Policies
    check_in_time: Optional[str]
    check_out_time: Optional[str]
    visitor_allowed: bool
    
    # Media
    cover_image_url: Optional[str]
    total_images: int
    has_virtual_tour: bool
    
    # Highlights
    unique_features: List[str] = Field(default_factory=list)
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)


class RoomTypeComparison(BaseSchema):
    """Room type details for comparison"""
    room_type: str
    price_monthly: Decimal
    available_beds: int
    total_beds: int
    amenities: List[str]


class ComparisonSummary(BaseSchema):
    """Comparison summary with recommendations"""
    best_for_budget: UUID = Field(..., description="Best value for money")
    best_rated: UUID = Field(..., description="Highest rated")
    best_location: Optional[UUID] = Field(None, description="Best location")
    most_amenities: UUID = Field(..., description="Most amenities")
    best_availability: UUID = Field(..., description="Best availability")
    
    price_comparison: "PriceComparison"
    amenity_comparison: "AmenityComparison"


class PriceComparison(BaseSchema):
    """Price comparison summary"""
    lowest_price: Decimal
    highest_price: Decimal
    average_price: Decimal
    price_difference_percentage: Decimal


class AmenityComparison(BaseSchema):
    """Amenity comparison summary"""
    common_amenities: List[str] = Field(..., description="Amenities all hostels have")
    unique_to_hostel: Dict[UUID, List[str]] = Field(..., description="Unique amenities per hostel")
    total_unique_amenities: int