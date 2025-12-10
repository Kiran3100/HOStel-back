"""
Search response schemas
"""
from typing import List, Dict, Any
from pydantic import Field
from decimal import Decimal
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.hostel.hostel_public import PublicHostelCard


class SearchResultItem(BaseSchema):
    """Generic search result wrapper (for hostels now, extensible later)"""
    hostel: PublicHostelCard
    score: Decimal = Field(..., description="Relevance score from search engine")


class FacetBucket(BaseSchema):
    """Facet value & count"""
    value: str
    count: int
    label: str


class FacetedSearchResponse(BaseSchema):
    """Response for advanced faceted search"""
    results: List[SearchResultItem]
    total_results: int
    page: int
    page_size: int
    total_pages: int

    # Facets
    facets: Dict[str, List[FacetBucket]] = Field(
        default_factory=dict, description="FacetName -> bucket list"
    )

    # Debug / meta
    query_time_ms: int = Field(..., description="Search execution time (ms)")
    raw_query: Dict[str, Any] = Field(
        default_factory=dict,
        description="Raw search engine query (optional, for debugging)",
    )