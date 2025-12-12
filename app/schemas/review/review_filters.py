# --- File: app/schemas/review/review_filters.py ---
"""
Review filter and search schemas with advanced filtering options.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import List, Optional

from pydantic import Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseFilterSchema

__all__ = [
    "ReviewFilterParams",
    "ReviewSearchRequest",
    "ReviewSortOptions",
    "ReviewExportRequest",
]


class ReviewFilterParams(BaseFilterSchema):
    """
    Comprehensive review filtering parameters.
    
    Supports filtering by hostel, ratings, verification, dates, and more.
    """
    
    # Hostel filters
    hostel_id: Optional[UUID] = Field(
        None,
        description="Filter by specific hostel",
    )
    hostel_ids: Optional[List[UUID]] = Field(
        None,
        max_length=50,
        description="Filter by multiple hostels (max 50)",
    )
    
    # Rating filters
    min_rating: Optional[Decimal] = Field(
        None,
        ge=Decimal("1.0"),
        le=Decimal("5.0"),
        description="Minimum overall rating",
    )
    max_rating: Optional[Decimal] = Field(
        None,
        ge=Decimal("1.0"),
        le=Decimal("5.0"),
        description="Maximum overall rating",
    )
    rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Exact rating (1-5 stars)",
    )
    
    # Verification filters
    verified_only: Optional[bool] = Field(
        None,
        description="Show only verified stay reviews",
    )
    
    # Date filters
    posted_date_from: Optional[date] = Field(
        None,
        description="Reviews posted on or after this date",
    )
    posted_date_to: Optional[date] = Field(
        None,
        description="Reviews posted on or before this date",
    )
    
    # Status filters
    approved_only: bool = Field(
        True,
        description="Show only approved/published reviews",
    )
    flagged_only: Optional[bool] = Field(
        None,
        description="Show only flagged reviews",
    )
    
    # Response filter
    with_hostel_response: Optional[bool] = Field(
        None,
        description="Filter by presence of hostel response",
    )
    
    # Engagement filters
    min_helpful_count: Optional[int] = Field(
        None,
        ge=0,
        description="Minimum helpful vote count",
    )
    
    # Media filter
    with_photos_only: Optional[bool] = Field(
        None,
        description="Show only reviews with photos",
    )
    
    @field_validator("hostel_ids")
    @classmethod
    def validate_hostel_ids(cls, v: Optional[List[UUID]]) -> Optional[List[UUID]]:
        """Validate hostel IDs list."""
        if v is not None and len(v) > 50:
            raise ValueError("Maximum 50 hostel IDs allowed")
        return v
    
    @field_validator("max_rating")
    @classmethod
    def validate_rating_range(cls, v: Optional[Decimal], info) -> Optional[Decimal]:
        """Validate that max_rating >= min_rating."""
        min_rating = info.data.get("min_rating")
        if v is not None and min_rating is not None and v < min_rating:
            raise ValueError("max_rating must be greater than or equal to min_rating")
        return v
    
    @field_validator("posted_date_to")
    @classmethod
    def validate_date_range(cls, v: Optional[date], info) -> Optional[date]:
        """Validate that posted_date_to >= posted_date_from."""
        posted_date_from = info.data.get("posted_date_from")
        if v is not None and posted_date_from is not None and v < posted_date_from:
            raise ValueError(
                "posted_date_to must be on or after posted_date_from"
            )
        return v


class ReviewSearchRequest(BaseFilterSchema):
    """
    Full-text search request for reviews.
    
    Supports searching in titles and content with advanced options.
    """
    
    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Search query",
        examples=["clean rooms", "friendly staff"],
    )
    hostel_id: Optional[UUID] = Field(
        None,
        description="Limit search to specific hostel",
    )
    
    # Search scope
    search_in_title: bool = Field(
        True,
        description="Include review titles in search",
    )
    search_in_content: bool = Field(
        True,
        description="Include review text in search",
    )
    
    # Additional filters
    min_rating: Optional[Decimal] = Field(
        None,
        ge=Decimal("1.0"),
        le=Decimal("5.0"),
        description="Filter by minimum rating",
    )
    verified_only: Optional[bool] = Field(
        None,
        description="Show only verified reviews",
    )
    
    # Pagination
    page: int = Field(
        1,
        ge=1,
        description="Page number",
    )
    page_size: int = Field(
        20,
        ge=1,
        le=100,
        description="Results per page",
    )
    
    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Validate and clean search query."""
        v = v.strip()
        if not v:
            raise ValueError("Search query cannot be empty")
        return v
    
    @model_validator(mode="after")
    def validate_search_scope(self) -> "ReviewSearchRequest":
        """Ensure at least one search scope is selected."""
        if not self.search_in_title and not self.search_in_content:
            raise ValueError(
                "At least one search scope must be enabled "
                "(title or content)"
            )
        return self


class ReviewSortOptions(BaseFilterSchema):
    """
    Review sorting options with multiple strategies.
    
    Supports various sorting methods including helpful votes and recency.
    """
    
    sort_by: str = Field(
        "helpful",
        pattern=r"^(helpful|recent|rating_high|rating_low|verified|oldest)$",
        description="Sort method",
    )
    
    # Priority options
    verified_first: bool = Field(
        True,
        description="Prioritize verified reviews in results",
    )
    with_photos_first: bool = Field(
        False,
        description="Prioritize reviews with photos",
    )
    with_response_first: bool = Field(
        False,
        description="Prioritize reviews with hostel responses",
    )
    
    @field_validator("sort_by")
    @classmethod
    def normalize_sort_by(cls, v: str) -> str:
        """Normalize sort_by value to lowercase."""
        return v.lower().strip()


class ReviewExportRequest(BaseFilterSchema):
    """
    Export reviews to various formats.
    
    Supports CSV, Excel, and PDF exports with customizable content.
    """
    
    hostel_id: UUID = Field(
        ...,
        description="Hostel to export reviews for",
    )
    filters: Optional[ReviewFilterParams] = Field(
        None,
        description="Additional filters to apply",
    )
    
    # Export format
    format: str = Field(
        "csv",
        pattern=r"^(csv|excel|pdf|json)$",
        description="Export format",
    )
    
    # Content options
    include_detailed_ratings: bool = Field(
        True,
        description="Include aspect-specific ratings",
    )
    include_hostel_responses: bool = Field(
        True,
        description="Include hostel responses to reviews",
    )
    include_voter_stats: bool = Field(
        False,
        description="Include helpful vote statistics",
    )
    include_reviewer_info: bool = Field(
        True,
        description="Include reviewer name and verification status",
    )
    
    # Date range for export
    date_from: Optional[date] = Field(
        None,
        description="Export reviews from this date onwards",
    )
    date_to: Optional[date] = Field(
        None,
        description="Export reviews up to this date",
    )
    
    @field_validator("format")
    @classmethod
    def normalize_format(cls, v: str) -> str:
        """Normalize format to lowercase."""
        return v.lower().strip()
    
    @field_validator("date_to")
    @classmethod
    def validate_date_range(cls, v: Optional[date], info) -> Optional[date]:
        """Validate export date range."""
        date_from = info.data.get("date_from")
        if v is not None and date_from is not None and v < date_from:
            raise ValueError("date_to must be on or after date_from")
        return v