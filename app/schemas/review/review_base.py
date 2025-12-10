"""
Review base schemas
"""
from decimal import Decimal
from typing import List, Optional
from pydantic import Field, HttpUrl, field_validator
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema


class ReviewBase(BaseSchema):
    """Base review schema"""
    hostel_id: UUID = Field(..., description="Hostel being reviewed")
    reviewer_id: UUID = Field(..., description="User writing review")
    student_id: Optional[UUID] = Field(None, description="Student profile (if verified stay)")
    booking_id: Optional[UUID] = Field(None, description="Related booking")
    
    # Overall rating
    overall_rating: Decimal = Field(..., ge=1, le=5, description="Overall rating 1-5")
    
    # Review content
    title: str = Field(..., min_length=5, max_length=255, description="Review title")
    review_text: str = Field(..., min_length=50, max_length=5000, description="Review text")
    
    # Detailed ratings
    cleanliness_rating: Optional[int] = Field(None, ge=1, le=5)
    food_quality_rating: Optional[int] = Field(None, ge=1, le=5)
    staff_behavior_rating: Optional[int] = Field(None, ge=1, le=5)
    security_rating: Optional[int] = Field(None, ge=1, le=5)
    value_for_money_rating: Optional[int] = Field(None, ge=1, le=5)
    amenities_rating: Optional[int] = Field(None, ge=1, le=5)
    
    # Photos
    photos: List[HttpUrl] = Field(default_factory=list, max_items=10, description="Review photos")
    
    @field_validator('overall_rating')
    @classmethod
    def round_rating(cls, v: Decimal) -> Decimal:
        """Round rating to 0.5"""
        return round(v * 2) / 2


class ReviewCreate(ReviewBase, BaseCreateSchema):
    """Create review"""
    pass


class ReviewUpdate(BaseUpdateSchema):
    """Update review (limited time after posting)"""
    title: Optional[str] = Field(None, min_length=5, max_length=255)
    review_text: Optional[str] = Field(None, min_length=50, max_length=5000)
    
    overall_rating: Optional[Decimal] = Field(None, ge=1, le=5)
    
    cleanliness_rating: Optional[int] = Field(None, ge=1, le=5)
    food_quality_rating: Optional[int] = Field(None, ge=1, le=5)
    staff_behavior_rating: Optional[int] = Field(None, ge=1, le=5)
    security_rating: Optional[int] = Field(None, ge=1, le=5)
    value_for_money_rating: Optional[int] = Field(None, ge=1, le=5)
    amenities_rating: Optional[int] = Field(None, ge=1, le=5)
    
    photos: Optional[List[HttpUrl]] = None