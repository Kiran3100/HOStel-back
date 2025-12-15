# --- File: app/schemas/payment/payment_filters.py ---
"""
Payment filter and search schemas.

This module defines schemas for filtering, searching, sorting,
and exporting payment data with comprehensive analytics support.
"""

from __future__ import annotations

from datetime import date as Date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.schemas.common.base import BaseFilterSchema
from app.schemas.common.enums import PaymentMethod, PaymentStatus, PaymentType

__all__ = [
    "PaymentFilterParams",
    "PaymentSearchRequest",
    "PaymentSortOptions",
    "PaymentReportRequest",
    "PaymentExportRequest",
    "PaymentAnalyticsRequest",
]


class PaymentFilterParams(BaseFilterSchema):
    """
    Comprehensive payment filter parameters.
    
    Supports filtering by various criteria including status, dates,
    amounts, payment methods, and entity relationships.
    """

    # Text Search
    search: Optional[str] = Field(
        None,
        max_length=255,
        description="Search in reference, payer name, transaction ID",
    )

    # Entity Filters
    hostel_id: Optional[UUID] = Field(
        None,
        description="Filter by specific hostel",
    )
    hostel_ids: Optional[List[UUID]] = Field(
        None,
        max_length=20,
        description="Filter by multiple hostels (max 20)",
    )
    student_id: Optional[UUID] = Field(
        None,
        description="Filter by specific student",
    )
    payer_id: Optional[UUID] = Field(
        None,
        description="Filter by specific payer",
    )

    # Payment Type Filters
    payment_type: Optional[PaymentType] = Field(
        None,
        description="Filter by specific payment type",
    )
    payment_types: Optional[List[PaymentType]] = Field(
        None,
        max_length=10,
        description="Filter by multiple payment types",
    )

    # Payment Method Filters
    payment_method: Optional[PaymentMethod] = Field(
        None,
        description="Filter by specific payment method",
    )
    payment_methods: Optional[List[PaymentMethod]] = Field(
        None,
        max_length=10,
        description="Filter by multiple payment methods",
    )

    # Status Filters
    payment_status: Optional[PaymentStatus] = Field(
        None,
        description="Filter by specific status",
    )
    payment_statuses: Optional[List[PaymentStatus]] = Field(
        None,
        max_length=10,
        description="Filter by multiple statuses",
    )

    # Amount Range Filters
    amount_min: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Minimum payment amount",
    )
    amount_max: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Maximum payment amount",
    )

    # Date Filters
    paid_date_from: Optional[Date] = Field(
        None,
        description="Filter payments paid from this Date",
    )
    paid_date_to: Optional[Date] = Field(
        None,
        description="Filter payments paid until this Date",
    )
    due_date_from: Optional[Date] = Field(
        None,
        description="Filter by due Date from",
    )
    due_date_to: Optional[Date] = Field(
        None,
        description="Filter by due Date to",
    )
    created_date_from: Optional[Date] = Field(
        None,
        description="Filter by creation Date from",
    )
    created_date_to: Optional[Date] = Field(
        None,
        description="Filter by creation Date to",
    )

    # Special Filters
    overdue_only: Optional[bool] = Field(
        None,
        description="Show only overdue payments",
    )
    pending_only: Optional[bool] = Field(
        None,
        description="Show only pending payments",
    )
    refunded_only: Optional[bool] = Field(
        None,
        description="Show only refunded payments",
    )

    # Gateway Filter
    payment_gateway: Optional[str] = Field(
        None,
        max_length=50,
        description="Filter by payment gateway",
    )

    @model_validator(mode="after")
    def validate_amount_range(self) -> "PaymentFilterParams":
        """Validate amount range."""
        if self.amount_min is not None and self.amount_max is not None:
            if self.amount_max < self.amount_min:
                raise ValueError(
                    f"Maximum amount (₹{self.amount_max}) must be greater than "
                    f"or equal to minimum amount (₹{self.amount_min})"
                )
        return self

    @model_validator(mode="after")
    def validate_paid_date_range(self) -> "PaymentFilterParams":
        """Validate paid Date range."""
        if self.paid_date_from is not None and self.paid_date_to is not None:
            if self.paid_date_to < self.paid_date_from:
                raise ValueError(
                    "paid_date_to must be after or equal to paid_date_from"
                )
        return self

    @model_validator(mode="after")
    def validate_due_date_range(self) -> "PaymentFilterParams":
        """Validate due Date range."""
        if self.due_date_from is not None and self.due_date_to is not None:
            if self.due_date_to < self.due_date_from:
                raise ValueError(
                    "due_date_to must be after or equal to due_date_from"
                )
        return self

    @model_validator(mode="after")
    def validate_created_date_range(self) -> "PaymentFilterParams":
        """Validate created Date range."""
        if self.created_date_from is not None and self.created_date_to is not None:
            if self.created_date_to < self.created_date_from:
                raise ValueError(
                    "created_date_to must be after or equal to created_date_from"
                )
        return self


class PaymentSearchRequest(BaseFilterSchema):
    """
    Payment search request with pagination.
    
    Supports full-text search across payment fields.
    """

    query: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Search query string",
    )
    hostel_id: Optional[UUID] = Field(
        None,
        description="Limit search to specific hostel",
    )

    # Search Fields
    search_in_reference: bool = Field(
        True,
        description="Search in payment reference",
    )
    search_in_payer_name: bool = Field(
        True,
        description="Search in payer name",
    )
    search_in_transaction_id: bool = Field(
        True,
        description="Search in transaction ID",
    )

    # Status Filter
    payment_status: Optional[PaymentStatus] = Field(
        None,
        description="Limit search to specific status",
    )

    # Pagination
    page: int = Field(
        1,
        ge=1,
        description="Page number (1-indexed)",
    )
    page_size: int = Field(
        20,
        ge=1,
        le=100,
        description="Items per page (max 100)",
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Validate and clean search query."""
        v = v.strip()
        if len(v) == 0:
            raise ValueError("Search query cannot be empty")
        return v


class PaymentSortOptions(BaseFilterSchema):
    """
    Payment sorting options.
    
    Defines how to sort payment results.
    """

    sort_by: str = Field(
        "created_at",
        pattern=r"^(created_at|paid_at|due_date|amount|payment_reference|payer_name|status)$",
        description="Field to sort by",
    )
    sort_order: str = Field(
        "desc",
        pattern=r"^(asc|desc)$",
        description="Sort order: ascending or descending",
    )

    @field_validator("sort_by", "sort_order")
    @classmethod
    def normalize_sort_fields(cls, v: str) -> str:
        """Normalize sort field values."""
        return v.lower()


class PaymentReportRequest(BaseFilterSchema):
    """
    Payment report generation request.
    
    Generates comprehensive payment reports with analytics.
    """

    hostel_id: Optional[UUID] = Field(
        None,
        description="Generate report for specific hostel (or all)",
    )

    # Date Range (Required)
    date_from: Date = Field(
        ...,
        description="Report start Date",
    )
    date_to: Date = Field(
        ...,
        description="Report end Date",
    )

    # Filters
    payment_types: Optional[List[PaymentType]] = Field(
        None,
        max_length=10,
        description="Include specific payment types",
    )
    payment_methods: Optional[List[PaymentMethod]] = Field(
        None,
        max_length=10,
        description="Include specific payment methods",
    )

    # Grouping
    group_by: str = Field(
        "day",
        pattern=r"^(day|week|month|payment_type|payment_method)$",
        description="How to group report data",
    )

    # Format
    format: str = Field(
        "pdf",
        pattern=r"^(pdf|excel|csv)$",
        description="Report format",
    )

    # Include Details
    include_transaction_details: bool = Field(
        True,
        description="Include detailed transaction list",
    )
    include_student_details: bool = Field(
        True,
        description="Include student information",
    )
    include_charts: bool = Field(
        True,
        description="Include charts and visualizations",
    )

    @field_validator("date_to")
    @classmethod
    def validate_date_range(cls, v: Date, info) -> Date:
        """Validate Date range."""
        # In Pydantic v2, info.data contains the other validated fields
        date_from = info.data.get("date_from")
        if date_from is not None:
            if v < date_from:
                raise ValueError("date_to must be after or equal to date_from")
            
            # Limit report period to reasonable range
            days_diff = (v - date_from).days
            if days_diff > 365:
                raise ValueError(
                    f"Report period cannot exceed 365 days (got {days_diff} days)"
                )
        
        return v

    @field_validator("format", "group_by")
    @classmethod
    def normalize_enum_fields(cls, v: str) -> str:
        """Normalize enum fields."""
        return v.lower()


class PaymentExportRequest(BaseFilterSchema):
    """
    Export payments data request.
    
    Supports multiple export formats with customizable fields.
    """

    filters: PaymentFilterParams = Field(
        ...,
        description="Filter criteria for export",
    )

    # Format
    format: str = Field(
        "csv",
        pattern=r"^(csv|excel|pdf)$",
        description="Export format",
    )

    # Fields to Include
    include_payer_details: bool = Field(
        True,
        description="Include payer personal details",
    )
    include_gateway_details: bool = Field(
        False,
        description="Include payment gateway response data",
    )
    include_refund_details: bool = Field(
        True,
        description="Include refund information",
    )
    include_receipt_urls: bool = Field(
        True,
        description="Include receipt download URLs",
    )

    # Export Options
    split_by_status: bool = Field(
        False,
        description="Create separate sheets/files for each status",
    )
    include_summary_sheet: bool = Field(
        True,
        description="Include summary/analytics sheet (for Excel)",
    )

    @field_validator("format")
    @classmethod
    def normalize_format(cls, v: str) -> str:
        """Normalize format."""
        return v.lower()


class PaymentAnalyticsRequest(BaseFilterSchema):
    """
    Payment analytics request.
    
    Generates analytics and insights for payments within
    a specified Date range.
    """

    hostel_id: Optional[UUID] = Field(
        None,
        description="Generate analytics for specific hostel (or all)",
    )

    # Date Range (Required)
    date_from: Date = Field(
        ...,
        description="Analytics start Date",
    )
    date_to: Date = Field(
        ...,
        description="Analytics end Date",
    )

    # Grouping/Aggregation
    group_by: str = Field(
        "day",
        pattern=r"^(day|week|month)$",
        description="Aggregate analytics by: day, week, or month",
    )

    # Metrics to Include
    include_revenue_metrics: bool = Field(
        True,
        description="Include revenue and collection metrics",
    )
    include_method_breakdown: bool = Field(
        True,
        description="Breakdown by payment method",
    )
    include_type_breakdown: bool = Field(
        True,
        description="Breakdown by payment type",
    )
    include_trends: bool = Field(
        True,
        description="Include trend analysis",
    )
    include_comparisons: bool = Field(
        False,
        description="Compare with previous period",
    )

    @field_validator("date_to")
    @classmethod
    def validate_date_range(cls, v: Date, info) -> Date:
        """Validate analytics Date range."""
        date_from = info.data.get("date_from")
        if date_from is not None:
            if v < date_from:
                raise ValueError("date_to must be after or equal to date_from")
            
            # Limit to reasonable range (e.g., max 2 years)
            days_diff = (v - date_from).days
            if days_diff > 730:
                raise ValueError(
                    f"Analytics period cannot exceed 730 days (got {days_diff} days)"
                )
        
        return v

    @field_validator("group_by")
    @classmethod
    def normalize_group_by(cls, v: str) -> str:
        """Normalize group_by value."""
        return v.lower()