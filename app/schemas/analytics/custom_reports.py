"""
Custom report builder schemas
"""
from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.filters import DateRangeFilter


class CustomReportFilter(BaseSchema):
    """Filter definition for custom report"""
    field_name: str
    operator: str = Field(
        ..., description="eq, ne, gt, lt, gte, lte, in, contains, between, etc."
    )
    value: Any
    value_to: Optional[Any] = Field(None, description="Second value for between, range")


class CustomReportField(BaseSchema):
    """Field included in custom report"""
    field_name: str
    display_label: Optional[str] = None
    aggregation: Optional[str] = Field(
        None, description="sum, avg, min, max, count, none"
    )


class CustomReportRequest(BaseCreateSchema):
    """Generate a custom report"""
    report_name: str = Field(..., min_length=3, max_length=255)
    module: str = Field(
        ...,
        description="Which module: bookings, payments, complaints, attendance, etc.",
    )

    period: Optional[DateRangeFilter] = None

    # Fields
    fields: List[CustomReportField] = Field(..., min_items=1)

    # Filters
    filters: List[CustomReportFilter] = Field(default_factory=list)

    # Grouping
    group_by: Optional[List[str]] = Field(
        None, description="List of field names to group by"
    )

    # Sorting
    sort_by: Optional[str] = None
    sort_order: Optional[str] = Field("asc", pattern="^(asc|desc)$")

    # Output
    format: str = Field("table", pattern="^(table|csv|excel|json)$")
    include_summary: bool = Field(True)
    include_charts: bool = Field(False)


class CustomReportDefinition(BaseSchema):
    """Saved custom report definition"""
    id: UUID
    owner_id: UUID
    report_name: str
    module: str

    period: Optional[DateRangeFilter] = None
    fields: List[CustomReportField]
    filters: List[CustomReportFilter]
    group_by: Optional[List[str]] = None

    # Sharing
    is_public: bool = Field(False)
    shared_with_user_ids: List[UUID] = Field(default_factory=list)

    created_at: datetime
    updated_at: datetime


class CustomReportResult(BaseSchema):
    """Result of running custom report"""
    report_id: Optional[UUID] = None
    report_name: str

    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Data
    rows: List[Dict[str, Any]] = Field(default_factory=list)
    total_rows: int

    # Summary (aggregations)
    summary: Optional[Dict[str, Any]] = None

    # Charts data (if requested)
    charts: Optional[Dict[str, Any]] = None