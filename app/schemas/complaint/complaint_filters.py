"""
Complaint filtering and search schemas.

Provides comprehensive filtering, searching, and sorting
capabilities for complaint queries.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import Field, field_validator

from app.schemas.common.base import BaseFilterSchema
from app.schemas.common.enums import ComplaintCategory, ComplaintStatus, Priority

__all__ = [
    "ComplaintFilterParams",
    "ComplaintSearchRequest",
    "ComplaintSortOptions",
    "ComplaintExportRequest",
]


class ComplaintFilterParams(BaseFilterSchema):
    """
    Comprehensive complaint filter parameters.
    
    Supports filtering by multiple dimensions for flexible queries.
    """

    # Text search
    search: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Search in title, description, complaint number",
    )

    # Hostel filters
    hostel_id: Optional[str] = Field(
        None,
        description="Filter by single hostel",
    )
    hostel_ids: Optional[List[str]] = Field(
        None,
        max_length=50,
        description="Filter by multiple hostels (max 50)",
    )

    # User filters
    raised_by: Optional[str] = Field(
        None,
        description="Filter by complainant user ID",
    )
    student_id: Optional[str] = Field(
        None,
        description="Filter by student ID",
    )

    # Assignment filters
    assigned_to: Optional[str] = Field(
        None,
        description="Filter by assigned staff member",
    )
    unassigned_only: Optional[bool] = Field(
        None,
        description="Show only unassigned complaints",
    )

    # Category filters
    category: Optional[ComplaintCategory] = Field(
        None,
        description="Filter by single category",
    )
    categories: Optional[List[ComplaintCategory]] = Field(
        None,
        max_length=20,
        description="Filter by multiple categories",
    )

    # Priority filters
    priority: Optional[Priority] = Field(
        None,
        description="Filter by single priority",
    )
    priorities: Optional[List[Priority]] = Field(
        None,
        max_length=10,
        description="Filter by multiple priorities",
    )

    # Status filters
    status: Optional[ComplaintStatus] = Field(
        None,
        description="Filter by single status",
    )
    statuses: Optional[List[ComplaintStatus]] = Field(
        None,
        max_length=10,
        description="Filter by multiple statuses",
    )

    # Date range filters
    opened_date_from: Optional[date] = Field(
        None,
        description="Opened date range start (inclusive)",
    )
    opened_date_to: Optional[date] = Field(
        None,
        description="Opened date range end (inclusive)",
    )
    resolved_date_from: Optional[date] = Field(
        None,
        description="Resolved date range start",
    )
    resolved_date_to: Optional[date] = Field(
        None,
        description="Resolved date range end",
    )

    # Special filters
    sla_breached_only: Optional[bool] = Field(
        None,
        description="Show only SLA breached complaints",
    )
    escalated_only: Optional[bool] = Field(
        None,
        description="Show only escalated complaints",
    )

    # Location filters
    room_id: Optional[str] = Field(
        None,
        description="Filter by specific room",
    )

    # Age filters
    age_hours_min: Optional[int] = Field(
        None,
        ge=0,
        description="Minimum complaint age in hours",
    )
    age_hours_max: Optional[int] = Field(
        None,
        ge=0,
        description="Maximum complaint age in hours",
    )

    @field_validator("search")
    @classmethod
    def validate_search(cls, v: Optional[str]) -> Optional[str]:
        """Normalize search query."""
        if v is not None:
            v = v.strip()
            if not v:
                return None
        return v

    @field_validator("hostel_ids", "categories", "priorities", "statuses")
    @classmethod
    def validate_list_length(cls, v: Optional[List]) -> Optional[List]:
        """Ensure filter lists don't exceed reasonable limits."""
        if v is not None and len(v) > 50:
            raise ValueError("Too many items in filter list (max 50)")
        return v

    @field_validator("opened_date_to")
    @classmethod
    def validate_opened_date_range(cls, v: Optional[date], info) -> Optional[date]:
        """Validate opened date range is logical."""
        opened_date_from = info.data.get("opened_date_from")
        if v is not None and opened_date_from is not None:
            if v < opened_date_from:
                raise ValueError(
                    "opened_date_to must be >= opened_date_from"
                )
        return v

    @field_validator("resolved_date_to")
    @classmethod
    def validate_resolved_date_range(cls, v: Optional[date], info) -> Optional[date]:
        """Validate resolved date range is logical."""
        resolved_date_from = info.data.get("resolved_date_from")
        if v is not None and resolved_date_from is not None:
            if v < resolved_date_from:
                raise ValueError(
                    "resolved_date_to must be >= resolved_date_from"
                )
        return v

    @field_validator("age_hours_max")
    @classmethod
    def validate_age_range(cls, v: Optional[int], info) -> Optional[int]:
        """Validate age range is logical."""
        age_hours_min = info.data.get("age_hours_min")
        if v is not None and age_hours_min is not None:
            if v < age_hours_min:
                raise ValueError(
                    "age_hours_max must be >= age_hours_min"
                )
        return v


class ComplaintSearchRequest(BaseFilterSchema):
    """
    Full-text search request for complaints.
    
    Supports configurable search fields and filters.
    """

    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Search query string",
    )
    hostel_id: Optional[str] = Field(
        None,
        description="Limit search to specific hostel",
    )

    # Search scope configuration
    search_in_title: bool = Field(
        default=True,
        description="Include title in search",
    )
    search_in_description: bool = Field(
        default=True,
        description="Include description in search",
    )
    search_in_number: bool = Field(
        default=True,
        description="Include complaint number in search",
    )

    # Optional filters
    status: Optional[ComplaintStatus] = Field(
        None,
        description="Filter by status",
    )
    priority: Optional[Priority] = Field(
        None,
        description="Filter by priority",
    )

    # Pagination
    page: int = Field(
        default=1,
        ge=1,
        description="Page number",
    )
    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Results per page (1-100)",
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Normalize search query."""
        v = v.strip()
        if not v:
            raise ValueError("Search query cannot be empty")
        return v


class ComplaintSortOptions(BaseFilterSchema):
    """
    Sorting options for complaint queries.
    
    Defines available sort fields and order.
    """

    sort_by: str = Field(
        default="opened_at",
        pattern=r"^(opened_at|priority|status|category|age|updated_at|resolved_at)$",
        description="Field to sort by",
    )
    sort_order: str = Field(
        default="desc",
        pattern=r"^(asc|desc)$",
        description="Sort order: ascending or descending",
    )

    @field_validator("sort_by", "sort_order")
    @classmethod
    def normalize_sort_params(cls, v: str) -> str:
        """Normalize sort parameters to lowercase."""
        return v.lower().strip()


class ComplaintExportRequest(BaseFilterSchema):
    """
    Export complaints to various formats.
    
    Supports CSV, Excel, and PDF exports with configurable fields.
    """

    hostel_id: Optional[str] = Field(
        None,
        description="Limit export to specific hostel",
    )
    filters: Optional[ComplaintFilterParams] = Field(
        None,
        description="Apply filters to export",
    )

    format: str = Field(
        default="csv",
        pattern=r"^(csv|excel|pdf)$",
        description="Export format: csv, excel, or pdf",
    )

    # Export options
    include_comments: bool = Field(
        default=False,
        description="Include comments in export",
    )
    include_resolution_details: bool = Field(
        default=True,
        description="Include resolution details",
    )
    include_feedback: bool = Field(
        default=True,
        description="Include student feedback",
    )

    @field_validator("format")
    @classmethod
    def normalize_format(cls, v: str) -> str:
        """Normalize export format to lowercase."""
        return v.lower().strip()