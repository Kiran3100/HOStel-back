# --- File: app/schemas/inquiry/__init__.py ---
"""
<<<<<<< Updated upstream
Visitor inquiry and contact schemas package.

This module exports all inquiry-related schemas for easy importing
across the application.
=======
Visitor inquiry & contact schemas package.

This package provides comprehensive schemas for managing visitor
inquiries throughout their lifecycle - from creation to conversion.

Modules:
    inquiry_base: Base schemas for creation and updates
    inquiry_response: Response schemas for API responses
    inquiry_status: Status management and timeline tracking

Example Usage:
    from app.schemas.inquiry import (
        InquiryCreate,
        InquiryResponse,
        InquiryStatusUpdate,
    )
    
    # Create new inquiry
    inquiry_data = InquiryCreate(
        hostel_id=hostel_uuid,
        visitor_name="John Doe",
        visitor_email="john@example.com",
        visitor_phone="+919876543210",
    )
    
    # Update inquiry status
    status_update = InquiryStatusUpdate(
        inquiry_id=inquiry_uuid,
        current_status=InquiryStatus.NEW,
        new_status=InquiryStatus.CONTACTED,
        updated_by=admin_uuid,
    )
>>>>>>> Stashed changes
"""

from __future__ import annotations

<<<<<<< Updated upstream
=======
# Base schemas
>>>>>>> Stashed changes
from app.schemas.inquiry.inquiry_base import (
    InquiryBase,
    InquiryContactUpdate,
    InquiryCreate,
<<<<<<< Updated upstream
    InquiryUpdate,
)
from app.schemas.inquiry.inquiry_filters import (
    InquiryExportRequest,
    InquiryFilterParams,
    InquirySearchRequest,
    InquirySortOptions,
=======
    InquiryFilter,
    InquiryUpdate,
>>>>>>> Stashed changes
)

# Response schemas
from app.schemas.inquiry.inquiry_response import (
<<<<<<< Updated upstream
=======
    HostelInquirySummary,
    InquiryConversionInfo,
>>>>>>> Stashed changes
    InquiryDetail,
    InquiryListItem,
    InquiryResponse,
    InquiryStats,
)

# Status and assignment schemas
from app.schemas.inquiry.inquiry_status import (
    BulkInquiryStatusUpdate,
    InquiryAssignment,
<<<<<<< Updated upstream
    InquiryConversion,
    InquiryFollowUp,
    InquiryStatusUpdate,
    InquiryTimelineEntry,
=======
    InquiryEscalation,
    InquiryStatusTransition,
    InquiryStatusUpdate,
    InquiryTimelineEntry,
    VALID_STATUS_TRANSITIONS,
>>>>>>> Stashed changes
)

__all__ = [
    # Base schemas
    "InquiryBase",
    "InquiryCreate",
    "InquiryUpdate",
<<<<<<< Updated upstream
    # Response
=======
    "InquiryFilter",
    "InquiryContactUpdate",
    
    # Response schemas
>>>>>>> Stashed changes
    "InquiryResponse",
    "InquiryDetail",
    "InquiryListItem",
    "InquiryStats",
<<<<<<< Updated upstream
    # Status Management
=======
    "InquiryConversionInfo",
    "HostelInquirySummary",
    
    # Status and assignment schemas
>>>>>>> Stashed changes
    "InquiryStatusUpdate",
    "InquiryStatusTransition",
    "InquiryAssignment",
<<<<<<< Updated upstream
    "InquiryFollowUp",
    "InquiryTimelineEntry",
    "InquiryConversion",
    "BulkInquiryStatusUpdate",
    # Filters
    "InquiryFilterParams",
    "InquirySearchRequest",
    "InquirySortOptions",
    "InquiryExportRequest",
]
=======
    "InquiryTimelineEntry",
    "BulkInquiryStatusUpdate",
    "InquiryEscalation",
    
    # Constants
    "VALID_STATUS_TRANSITIONS",
]

# Package version
__version__ = "1.0.0"
>>>>>>> Stashed changes
