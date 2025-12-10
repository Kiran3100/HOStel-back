"""
Visitor inquiry & contact schemas package
"""

from app.schemas.inquiry.inquiry_base import (
    InquiryBase,
    InquiryCreate,
)
from app.schemas.inquiry.inquiry_response import (
    InquiryResponse,
    InquiryDetail,
    InquiryListItem,
)
from app.schemas.inquiry.inquiry_status import (
    InquiryStatusUpdate,
    InquiryAssignment,
)

__all__ = [
    # Base
    "InquiryBase",
    "InquiryCreate",
    # Response
    "InquiryResponse",
    "InquiryDetail",
    "InquiryListItem",
    # Status/assignment
    "InquiryStatusUpdate",
    "InquiryAssignment",
]