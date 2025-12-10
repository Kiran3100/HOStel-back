"""
Review submission schemas
"""
from decimal import Decimal
from typing import List, Optional
from pydantic import Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema


class ReviewSubmissionRequest(BaseCreateSchema):
    """Submit review request"""
    hostel_id: UUID = Field(..., description="Hostel to review")
    
    # Verification (optional, helps verify stay)
    booking_id: Optional[UUID] = Field(None, description="Related booking ID")
    student_id: Optional[UUID] = Field(None, description="Student profile ID")
    
    # Basic review
    overall_rating: Decimal = Field(..., ge=1, le=5, description="Overall rating")
    title: str = Field(..., min_length=5, max_length=255)
    review_text: str = Field(..., min_length=50, max_length=5000)
    
    # Detailed ratings
    detailed_ratings: "DetailedRatings"
    
    # Media
    photos: List[HttpUrl] = Field(default_factory=list, max_items=10)
    
    # Recommendations
    would_recommend: bool = Field(..., description="Would recommend this hostel?")
    
    # Stay details (helps verification)
    stay_duration_months: Optional[int] = Field(None, ge=1, le=24)
    check_in_date: Optional[date] = None
    
    # Terms
    agree_to_guidelines: bool = Field(..., description="Agrees to review guidelines")


class DetailedRatings(BaseSchema):
    """Detailed aspect ratings"""
    cleanliness: int = Field(..., ge=1, le=5, description="Cleanliness rating")
    food_quality: Optional[int] = Field(None, ge=1, le=5, description="Food quality (if applicable)")
    staff_behavior: int = Field(..., ge=1, le=5, description="Staff behavior")
    security: int = Field(..., ge=1, le=5, description="Security")
    value_for_money: int = Field(..., ge=1, le=5, description="Value for money")
    amenities: int = Field(..., ge=1, le=5, description="Amenities quality")
    location: Optional[int] = Field(None, ge=1, le=5, description="Location convenience")
    wifi_quality: Optional[int] = Field(None, ge=1, le=5, description="WiFi quality")
    maintenance: Optional[int] = Field(None, ge=1, le=5, description="Maintenance responsiveness")


class VerifiedReview(BaseSchema):
    """Verified review marker"""
    review_id: UUID
    
    is_verified: bool
    verification_method: str = Field(
        ...,
        pattern="^(booking_verified|student_verified|admin_verified|auto_verified)$"
    )
    
    verified_by: Optional[UUID] = None
    verified_at: datetime
    
    verification_details: Optional[dict] = Field(
        None,
        description="Additional verification information"
    )


class ReviewGuidelines(BaseSchema):
    """Review guidelines"""
    guidelines: List[str] = Field(
        default_factory=lambda: [
            "Be honest and fair",
            "Focus on your experience",
            "Avoid offensive language",
            "Don't include personal information",
            "Be specific and constructive",
            "Reviews are public and visible to all"
        ]
    )
    
    prohibited_content: List[str] = Field(
        default_factory=lambda: [
            "Offensive or abusive language",
            "Personal attacks",
            "Spam or promotional content",
            "Fake or fraudulent reviews",
            "Reviews for competing businesses"
        ]
    )


class ReviewEligibility(BaseSchema):
    """Check if user can review hostel"""
    user_id: UUID
    hostel_id: UUID
    
    can_review: bool
    reason: str
    
    # Details
    has_stayed: bool
    has_booking: bool
    already_reviewed: bool
    
    # If already reviewed
    existing_review_id: Optional[UUID] = None
    can_edit: bool = Field(False, description="Can edit existing review")