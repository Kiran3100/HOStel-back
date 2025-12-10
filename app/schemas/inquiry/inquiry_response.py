"""
Inquiry response schemas
"""
from datetime import datetime, date
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import InquiryStatus, RoomType


class InquiryResponse(BaseResponseSchema):
    """Basic inquiry response"""
    hostel_id: UUID
    hostel_name: str

    visitor_name: str
    visitor_email: str
    visitor_phone: str

    preferred_check_in_date: Optional[date]
    stay_duration_months: Optional[int]
    room_type_preference: Optional[RoomType]

    status: InquiryStatus
    created_at: datetime


class InquiryDetail(BaseResponseSchema):
    """Detailed inquiry view"""
    hostel_id: UUID
    hostel_name: str

    visitor_name: str
    visitor_email: str
    visitor_phone: str

    preferred_check_in_date: Optional[date]
    stay_duration_months: Optional[int]
    room_type_preference: Optional[RoomType]

    message: Optional[str]

    inquiry_source: str
    status: InquiryStatus

    contacted_by: Optional[UUID]
    contacted_by_name: Optional[str]
    contacted_at: Optional[datetime]

    notes: Optional[str]

    created_at: datetime
    updated_at: datetime


class InquiryListItem(BaseSchema):
    """List item for inquiries"""
    id: UUID
    hostel_name: str
    visitor_name: str
    visitor_phone: str
    preferred_check_in_date: Optional[date]
    stay_duration_months: Optional[int]
    room_type_preference: Optional[RoomType]
    status: InquiryStatus
    created_at: datetime