# --- File: app/schemas/common/filters.py ---
"""
Common filter schemas used for query/filter parameters across the API.
"""

from __future__ import annotations

from datetime import date, datetime, time
from typing import Dict, List, Optional

from pydantic import Field, field_validator

from app.schemas.common.base import BaseFilterSchema, BaseSchema

__all__ = [
    "DateRangeFilter",
    "DateTimeRangeFilter",
    "TimeRangeFilter",
    "PriceRangeFilter",
    "SearchFilter",
    "SortOptions",
    "StatusFilter",
    "NumericRangeFilter",
    "LocationFilter",
    "MultiSelectFilter",
    "BooleanFilter",
    "TextSearchFilter",
]


class DateRangeFilter(BaseFilterSchema):
    """Date range filter."""

    start_date: Optional[date] = Field(None, description="Start date (inclusive)")
    end_date: Optional[date] = Field(None, description="End date (inclusive)")

    @field_validator("end_date")
    @classmethod
    def validate_date_range(cls, v: Optional[date], info) -> Optional[date]:
        """Validate end_date is after or equal to start_date."""
        start_date = info.data.get("start_date")
        if v is not None and start_date is not None and v < start_date:
            raise ValueError("end_date must be after or equal to start_date")
        return v


class DateTimeRangeFilter(BaseFilterSchema):
    """Datetime range filter."""

    start_datetime: Optional[datetime] = Field(
        None,
        description="Start datetime (inclusive)",
    )
    end_datetime: Optional[datetime] = Field(
        None,
        description="End datetime (inclusive)",
    )

    @field_validator("end_datetime")
    @classmethod
    def validate_datetime_range(
        cls,
        v: Optional[datetime],
        info,
    ) -> Optional[datetime]:
        """Validate end_datetime is after or equal to start_datetime."""
        start_datetime = info.data.get("start_datetime")
        if v is not None and start_datetime is not None and v < start_datetime:
            raise ValueError(
                "end_datetime must be after or equal to start_datetime",
            )
        return v


class TimeRangeFilter(BaseFilterSchema):
    """Time range filter."""

    start_time: Optional[time] = Field(None, description="Start time")
    end_time: Optional[time] = Field(None, description="End time")


class PriceRangeFilter(BaseFilterSchema):
    """Price range filter."""

    min_price: Optional[float] = Field(
        None,
        ge=0,
        description="Minimum price",
    )
    max_price: Optional[float] = Field(
        None,
        ge=0,
        description="Maximum price",
    )

    @field_validator("max_price")
    @classmethod
    def validate_price_range(cls, v: Optional[float], info) -> Optional[float]:
        """Validate max_price is greater than or equal to min_price."""
        min_price = info.data.get("min_price")
        if v is not None and min_price is not None and v < min_price:
            raise ValueError(
                "max_price must be greater than or equal to min_price",
            )
        return v


class SearchFilter(BaseFilterSchema):
    """Generic search filter."""

    search_query: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Search query string",
    )


class SortOptions(BaseFilterSchema):
    """Sorting options."""

    sort_by: str = Field(..., description="Field to sort by")
    sort_order: str = Field(
        "asc",
        pattern=r"^(asc|desc)$",
        description="Sort order: asc or desc (case-insensitive input allowed)",
    )

    @field_validator("sort_order")
    @classmethod
    def validate_sort_order(cls, v: str) -> str:
        """Validate and normalize sort order."""
        return v.lower()


class StatusFilter(BaseFilterSchema):
    """Status filter."""

    statuses: Optional[List[str]] = Field(
        None,
        description="Filter by status values",
    )
    exclude_statuses: Optional[List[str]] = Field(
        None,
        description="Exclude status values",
    )


class NumericRangeFilter(BaseFilterSchema):
    """Generic numeric range filter."""

    min_value: Optional[float] = Field(None, description="Minimum value")
    max_value: Optional[float] = Field(None, description="Maximum value")

    @field_validator("max_value")
    @classmethod
    def validate_range(cls, v: Optional[float], info) -> Optional[float]:
        """Validate max_value is greater than or equal to min_value."""
        min_value = info.data.get("min_value")
        if v is not None and min_value is not None and v < min_value:
            raise ValueError(
                "max_value must be greater than or equal to min_value",
            )
        return v


class LocationFilter(BaseFilterSchema):
    """Location-based filter."""

    latitude: Optional[float] = Field(
        None,
        ge=-90,
        le=90,
        description="Latitude",
    )
    longitude: Optional[float] = Field(
        None,
        ge=-180,
        le=180,
        description="Longitude",
    )
    radius_km: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Search radius in kilometers",
    )
    city: Optional[str] = Field(None, description="City name")
    state: Optional[str] = Field(None, description="State name")
    pincode: Optional[str] = Field(
        None,
        pattern=r"^\d{6}$",
        description="Pincode",
    )


class MultiSelectFilter(BaseFilterSchema):
    """Multi-select filter with include/exclude."""

    include: Optional[List[str]] = Field(
        None,
        description="Include these values",
    )
    exclude: Optional[List[str]] = Field(
        None,
        description="Exclude these values",
    )


class BooleanFilter(BaseFilterSchema):
    """Boolean filter (yes/no/all)."""

    value: Optional[bool] = Field(
        None,
        description="Boolean filter value",
    )


class TextSearchFilter(BaseFilterSchema):
    """Full-text search filter."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Search query",
    )
    fields: Optional[List[str]] = Field(
        None,
        description="Fields to search in",
    )
    fuzzy: bool = Field(False, description="Enable fuzzy search")
    boost: Optional[Dict[str, float]] = Field(
        None,
        description="Field boost weights",
    )