"""
Review response schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema


class ReviewResponse(BaseResponseSchema):
    """Review response"""
    hostel_id: UUID
    hostel_name: str
    
    reviewer_id: UUID
    reviewer_name: str
    
    overall_rating: Decimal
    title: str
    review_text: str
    
    is_verified_stay: bool
    verified_at: Optional[datetime]
    
    is_approved: bool
    
    helpful_count: int
    not_helpful_count: int
    
    created_at: datetime


class ReviewDetail(BaseResponseSchema):
    """Detailed review information"""
    hostel_id: UUID
    hostel_name: str
    
    # Reviewer
    reviewer_id: UUID
    reviewer_name: str
    reviewer_profile_image: Optional[str]
    
    student_id: Optional[UUID]
    booking_id: Optional[UUID]
    
    # Ratings
    overall_rating: Decimal
    cleanliness_rating: Optional[int]
    food_quality_rating: Optional[int]
    staff_behavior_rating: Optional[int]
    security_rating: Optional[int]
    value_for_money_rating: Optional[int]
    amenities_rating: Optional[int]
    
    # Content
    title: str
    review_text: str
    
    # Photos
    photos: List[str]
    
    # Verification
    is_verified_stay: bool
    verified_at: Optional[datetime]
    
    # Moderation
    is_approved: bool
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    
    is_flagged: bool
    flag_reason: Optional[str]
    flagged_by: Optional[UUID]
    flagged_at: Optional[datetime]
    
    # Engagement
    helpful_count: int
    not_helpful_count: int
    report_count: int
    
    # Hostel response
    hostel_response: Optional["HostelResponseDetail"]
    
    # Dates
    created_at: datetime
    updated_at: datetime
    
    # Visibility
    is_published: bool


class HostelResponseDetail(BaseSchema):
    """Hostel's response to review"""
    response_text: str
    responded_by: UUID
    responded_by_name: str
    responded_at: datetime


class ReviewListItem(BaseSchema):
    """Review list item"""
    id: UUID
    reviewer_name: str
    overall_rating: Decimal
    title: str
    review_excerpt: str = Field(..., description="First 150 characters")
    
    is_verified_stay: bool
    helpful_count: int
    
    created_at: datetime
    
    has_hostel_response: bool


class ReviewSummary(BaseSchema):
    """Review summary for hostel"""
    hostel_id: UUID
    hostel_name: str
    
    total_reviews: int
    average_rating: Decimal
    
    # Rating distribution
    rating_5_count: int
    rating_4_count: int
    rating_3_count: int
    rating_2_count: int
    rating_1_count: int
    
    # Verified reviews
    verified_reviews_count: int
    verified_reviews_percentage: Decimal
    
    # Recent reviews
    recent_reviews: List[ReviewListItem] = Field(default_factory=list, max_items=5)
    
    # Recommendation
    would_recommend_percentage: Decimal = Field(
        ...,
        description="% of reviewers who would recommend"
    )