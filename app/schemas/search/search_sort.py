"""
Search sort option schemas
"""
from pydantic import Field

from app.schemas.common.base import BaseSchema


class SortCriteria(BaseSchema):
    """Sort criteria used by search"""
    sort_by: str = Field(
        ...,
        pattern="^(relevance|price|rating|distance|created_at)$",
        description="Field to sort by",
    )
    sort_order: str = Field(
        "asc",
        pattern="^(asc|desc)$",
        description="Sort direction",
    )