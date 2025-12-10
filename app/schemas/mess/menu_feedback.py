"""
Mess menu feedback schemas
"""
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional, Dict
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema
from app.schemas.common.enums import MealType


class FeedbackRequest(BaseCreateSchema):
    """Submit menu feedback"""
    menu_id: UUID = Field(..., description="Menu ID")
    student_id: UUID = Field(..., description="Student ID")
    
    meal_type: MealType = Field(..., description="Which meal")
    rating: int = Field(..., ge=1, le=5, description="Rating 1-5")
    
    comments: Optional[str] = Field(None, max_length=1000)
    
    # Specific aspects
    taste_rating: Optional[int] = Field(None, ge=1, le=5)
    quantity_rating: Optional[int] = Field(None, ge=1, le=5)
    quality_rating: Optional[int] = Field(None, ge=1, le=5)
    hygiene_rating: Optional[int] = Field(None, ge=1, le=5)


class FeedbackResponse(BaseResponseSchema):
    """Feedback response"""
    menu_id: UUID
    student_id: UUID
    student_name: str
    
    meal_type: MealType
    rating: int
    comments: Optional[str]
    
    submitted_at: datetime


class RatingsSummary(BaseSchema):
    """Ratings summary for menu"""
    menu_id: UUID
    menu_date: date
    
    total_feedbacks: int
    average_rating: Decimal
    
    # By meal
    breakfast_rating: Optional[Decimal]
    lunch_rating: Optional[Decimal]
    snacks_rating: Optional[Decimal]
    dinner_rating: Optional[Decimal]
    
    # Rating distribution
    rating_5_count: int
    rating_4_count: int
    rating_3_count: int
    rating_2_count: int
    rating_1_count: int
    
    # Aspect ratings
    average_taste_rating: Decimal
    average_quantity_rating: Decimal
    average_quality_rating: Decimal
    average_hygiene_rating: Decimal


class QualityMetrics(BaseSchema):
    """Menu quality metrics"""
    hostel_id: UUID
    period_start: date
    period_end: date
    
    # Overall
    overall_average_rating: Decimal
    total_feedbacks: int
    
    # Trends
    rating_trend: str = Field(..., pattern="^(improving|declining|stable)$")
    trend_percentage: Optional[Decimal]
    
    # Best and worst
    best_rated_items: List["ItemRating"]
    worst_rated_items: List["ItemRating"]
    
    # By day of week
    ratings_by_day: Dict[str, Decimal]


class ItemRating(BaseSchema):
    """Rating for specific menu item"""
    item_name: str
    average_rating: Decimal
    feedback_count: int


class FeedbackAnalysis(BaseSchema):
    """Feedback analysis and insights"""
    hostel_id: UUID
    analysis_period: DateRangeFilter
    
    # Sentiment
    positive_feedback_percentage: Decimal
    negative_feedback_percentage: Decimal
    
    # Common themes
    common_complaints: List[str]
    common_compliments: List[str]
    
    # Recommendations
    items_to_keep: List[str]
    items_to_improve: List[str]
    items_to_remove: List[str]