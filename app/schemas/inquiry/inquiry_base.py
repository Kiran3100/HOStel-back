"""
Base visitor inquiry schemas
"""
from datetime import date, datetime
from typing import Optional
from pydantic import Field, EmailStr
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.enums import InquiryStatus, RoomType


class InquiryBase(BaseSchema):
    """Base visitor inquiry fields"""
    hostel_id: UUID = Field(..., description="Hostel being inquired about")

    visitor_name: str = Field(..., min_length=2, max_length=255)
    visitor_email: EmailStr = Field(..., description="Visitor email")
    visitor_phone: str = Field(..., pattern=r"^\+?[1-9]\d{9,14}$")

    preferred_check_in_date: Optional[date] = None
    stay_duration_months: Optional[int] = Field(None, ge=1, le=36)
    room_type_preference: Optional[RoomType] = None

    message: Optional[str] = Field(None, max_length=2000)

    inquiry_source: str = Field(
        "website",
        pattern=r"^(website|mobile_app|referral|social_media|other)$",
        description="Source of inquiry",
    )

    status: InquiryStatus = Field(InquiryStatus.NEW)


class InquiryCreate(InquiryBase, BaseCreateSchema):
    """Create visitor inquiry"""
    pass