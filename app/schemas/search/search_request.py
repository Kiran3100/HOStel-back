"""
Search request schemas (hostels, rooms, etc.)
"""
from typing import List, Optional
from pydantic import Field
from uuid import UUID
from decimal import Decimal

from app.schemas.common.base import BaseSchema, BaseFilterSchema
from app.schemas.common.enums import HostelType, RoomType


class BasicSearchRequest(BaseFilterSchema):
    """Simple keyword search"""
    query: str = Field(..., min_length=1, max_length=255)


class AdvancedSearchRequest(BaseFilterSchema):
    """Advanced hostel search request (public)"""
    query: Optional[str] = Field(None, max_length=255)

    # Location
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = Field(None, pattern=r"^\d{6}$")

    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180)
    radius_km: Optional[Decimal] = Field(None, ge=0, le=100)

    # Filters
    hostel_type: Optional[HostelType] = None
    room_type: Optional[RoomType] = None

    min_price: Optional[Decimal] = Field(None, ge=0)
    max_price: Optional[Decimal] = Field(None, ge=0)

    amenities: Optional[List[str]] = None
    min_rating: Optional[Decimal] = Field(None, ge=0, le=5)

    verified_only: bool = Field(False)
    available_only: bool = Field(False)

    # Sorting
    sort_by: str = Field(
        "relevance",
        pattern="^(relevance|price_asc|price_desc|rating_desc|distance_asc|newest)$",
    )
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)