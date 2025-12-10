"""
Reusable search filter schemas (common for advanced search)
"""
from typing import List, Optional
from pydantic import Field
from decimal import Decimal

from app.schemas.common.base import BaseFilterSchema


class PriceFilter(BaseFilterSchema):
    min_price: Optional[Decimal] = Field(None, ge=0)
    max_price: Optional[Decimal] = Field(None, ge=0)


class RatingFilter(BaseFilterSchema):
    min_rating: Optional[Decimal] = Field(None, ge=0, le=5)
    max_rating: Optional[Decimal] = Field(None, ge=0, le=5)


class AmenityFilter(BaseFilterSchema):
    amenities: Optional[List[str]] = Field(None)