"""
Payment filter and search schemas
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseFilterSchema
from app.schemas.common.enums import PaymentType, PaymentMethod, PaymentStatus


class PaymentFilterParams(BaseFilterSchema):
    """Payment filter parameters"""
    # Text search
    search: Optional[str] = Field(None, description="Search in reference, payer name, transaction ID")
    
    # Entity filters
    hostel_id: Optional[UUID] = None
    hostel_ids: Optional[List[UUID]] = None
    student_id: Optional[UUID] = None
    payer_id: Optional[UUID] = None
    
    # Payment type
    payment_type: Optional[PaymentType] = None
    payment_types: Optional[List[PaymentType]] = None
    
    # Payment method
    payment_method: Optional[PaymentMethod] = None
    payment_methods: Optional[List[PaymentMethod]] = None
    
    # Status
    payment_status: Optional[PaymentStatus] = None
    payment_statuses: Optional[List[PaymentStatus]] = None
    
    # Amount range
    amount_min: Optional[Decimal] = Field(None, ge=0)
    amount_max: Optional[Decimal] = Field(None, ge=0)
    
    # Date filters
    paid_date_from: Optional[date] = None
    paid_date_to: Optional[date] = None
    due_date_from: Optional[date] = None
    due_date_to: Optional[date] = None
    created_date_from: Optional[date] = None
    created_date_to: Optional[date] = None
    
    # Overdue filter
    overdue_only: Optional[bool] = None
    
    # Gateway
    payment_gateway: Optional[str] = None


class PaymentSearchRequest(BaseFilterSchema):
    """Payment search request"""
    query: str = Field(..., min_length=1, description="Search query")
    hostel_id: Optional[UUID] = None
    
    # Search fields
    search_in_reference: bool = Field(True)
    search_in_payer_name: bool = Field(True)
    search_in_transaction_id: bool = Field(True)
    
    # Filters
    payment_status: Optional[PaymentStatus] = None
    
    # Pagination
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class PaymentReportRequest(BaseFilterSchema):
    """Payment report generation request"""
    hostel_id: Optional[UUID] = None
    
    # Date range (required)
    date_from: date = Field(..., description="Report start date")
    date_to: date = Field(..., description="Report end date")
    
    # Filters
    payment_types: Optional[List[PaymentType]] = None
    payment_methods: Optional[List[PaymentMethod]] = None
    
    # Grouping
    group_by: str = Field("day", pattern="^(day|week|month|payment_type|payment_method)$")
    
    # Format
    format: str = Field("pdf", pattern="^(pdf|excel|csv)$")
    
    # Include details
    include_transaction_details: bool = Field(True)
    include_student_details: bool = Field(True)
    include_charts: bool = Field(True, description="Include charts/graphs")


class PaymentExportRequest(BaseFilterSchema):
    """Export payments data"""
    filters: PaymentFilterParams = Field(..., description="Filter criteria")
    
    format: str = Field("csv", pattern="^(csv|excel|pdf)$")
    
    # Fields to include
    include_payer_details: bool = Field(True)
    include_gateway_details: bool = Field(False)
    include_refund_details: bool = Field(True)