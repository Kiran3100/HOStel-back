# --- File: app/schemas/inquiry/__init__.py ---
"""
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
Visitor inquiry and contact schemas package.

This module exports all inquiry-related schemas for easy importing
across the application.
<<<<<<< Updated upstream
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
=======
>>>>>>> Stashed changes
"""

from __future__ import annotations

<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
# Base schemas
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
from app.schemas.inquiry.inquiry_base import (
    InquiryBase,
    InquiryContactUpdate,
    InquiryCreate,
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    InquiryUpdate,
=======
    InquiryUpdate,
)
from app.schemas.inquiry.inquiry_filters import (
    InquiryExportRequest,
    InquiryFilterParams,
    InquirySearchRequest,
    InquirySortOptions,
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
=======
    HostelInquirySummary,
    InquiryConversionInfo,
>>>>>>> Stashed changes
=======
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
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
    InquiryConversion,
    InquiryFollowUp,
    InquiryStatusUpdate,
    InquiryTimelineEntry,
<<<<<<< Updated upstream
=======
    InquiryEscalation,
    InquiryStatusTransition,
    InquiryStatusUpdate,
    InquiryTimelineEntry,
    VALID_STATUS_TRANSITIONS,
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
)

__all__ = [
    # Base schemas
    "InquiryBase",
    "InquiryCreate",
    "InquiryUpdate",
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    # Status Management
=======
    "InquiryConversionInfo",
    "HostelInquirySummary",
    
    # Status and assignment schemas
>>>>>>> Stashed changes
=======
    # Status Management
>>>>>>> Stashed changes
    "InquiryStatusUpdate",
    "InquiryStatusTransition",
    "InquiryAssignment",
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
    "InquiryFollowUp",
    "InquiryTimelineEntry",
    "InquiryConversion",
    "BulkInquiryStatusUpdate",
    # Filters
    "InquiryFilterParams",
    "InquirySearchRequest",
    "InquirySortOptions",
    "InquiryExportRequest",
<<<<<<< Updated upstream
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
=======
]
>>>>>>> Stashed changes
