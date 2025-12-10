"""
Review filter schemas
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseFilterSchema


class ReviewFilterParams(BaseFilterSchema):
    """Review filter parameters"""
    # Hostel filter
    hostel_id: Optional[UUID] = None
    hostel_ids: Optional[List[UUID]] = None
    
    # Rating filter
    min_rating: Optional[Decimal] = Field(None, ge=1, le=5)
    max_rating: Optional[Decimal] = Field(None, ge=1, le=5)
    rating: Optional[int] = Field(None, ge=1, le=5, description="Exact rating")
    
    # Verification
    verified_only: Optional[bool] = None
    
    # Date filter
    posted_date_from: Optional[date] = None
    posted_date_to: Optional[date] = None
    
    # Status
    approved_only: bool = Field(True, description="Show only approved reviews")
    flagged_only: Optional[bool] = None
    
    # Response
    with_hostel_response: Optional[bool] = None
    
    # Helpfulness
    min_helpful_count: Optional[int] = Field(None, ge=0)
    
    # Photos
    with_photos_only: Optional[bool] = None


class SearchRequest(BaseFilterSchema):
    """Search reviews"""
    query: str = Field(..., min_length=1)
    hostel_id: Optional[UUID] = None
    
    search_in_title: bool = Field(True)
    search_in_content: bool = Field(True)
    
    min_rating: Optional[Decimal] = None
    
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class SortOptions(BaseFilterSchema):
    """Review sorting options"""
    sort_by: str = Field(
        "helpful",
        pattern="^(helpful|recent|rating_high|rating_low|verified)$"
    )
    
    # Additional sort logic
    verified_first: bool = Field(True, description="Show verified reviews first")
    with_photos_first: bool = Field(False, description="Prioritize reviews with photos")


class ReviewExportRequest(BaseFilterSchema):
    """Export reviews"""
    hostel_id: UUID
    filters: Optional[ReviewFilterParams] = None
    
    format: str = Field("csv", pattern="^(csv|excel|pdf)$")
    
    include_detailed_ratings: bool = Field(True)
    include_hostel_responses: bool = Field(True)
    include_voter_stats: bool = Field(False)