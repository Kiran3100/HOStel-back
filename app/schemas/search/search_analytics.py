"""
Search analytics & popular queries schemas
"""
from datetime import date, datetime
from typing import List, Dict
from pydantic import Field

from app.schemas.common.base import BaseSchema
from app.schemas.common.filters import DateRangeFilter


class SearchTermStats(BaseSchema):
    """Statistics for a single search term"""
    term: str
    search_count: int
    avg_results: float
    zero_result_count: int
    last_searched_at: datetime


class SearchAnalytics(BaseSchema):
    """Search analytics summary"""
    period: DateRangeFilter

    total_searches: int
    unique_terms: int
    zero_result_searches: int

    top_terms: List[SearchTermStats] = Field(default_factory=list)
    zero_result_terms: List[SearchTermStats] = Field(default_factory=list)

    # Aggregated metrics
    avg_results_per_search: float