"""
Autocomplete / suggestion schemas
"""
from typing import List
from pydantic import Field

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class AutocompleteRequest(BaseCreateSchema):
    """Request for autocomplete suggestions"""
    prefix: str = Field(..., min_length=1, max_length=100)
    type: str = Field(
        "hostel",
        pattern="^(hostel|city|area)$",
        description="What to autocomplete",
    )
    limit: int = Field(10, ge=1, le=20)


class Suggestion(BaseSchema):
    """Single suggestion"""
    value: str
    label: str
    type: str
    extra: dict = Field(default_factory=dict)


class AutocompleteResponse(BaseSchema):
    """Autocomplete result set"""
    suggestions: List[Suggestion]