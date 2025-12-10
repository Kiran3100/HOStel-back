"""
Complaint feedback schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class FeedbackRequest(BaseCreateSchema):
    """Submit feedback on resolved complaint"""
    complaint_id: UUID = Field(..., description="Complaint ID")
    
    rating: int = Field(..., ge=1, le=5, description="Rating 1-5")
    
    feedback: Optional[str] = Field(None, max_length=1000, description="Detailed feedback")
    
    # Satisfaction questions
    issue_resolved_satisfactorily: bool = Field(..., description="Was issue resolved well?")
    response_time_satisfactory: bool = Field(..., description="Was response time good?")
    staff_helpful: bool = Field(..., description="Was staff helpful?")
    
    # Would recommend
    would_recommend: Optional[bool] = Field(None, description="Would recommend complaint system")


class FeedbackResponse(BaseResponseSchema):
    """Feedback response"""
    complaint_id: UUID
    complaint_number: str
    
    rating: int
    feedback: Optional[str]
    
    submitted_by: UUID
    submitted_at: datetime
    
    message: str


class FeedbackSummary(BaseSchema):
    """Feedback summary for hostel/supervisor"""
    entity_id: UUID
    entity_type: str = Field(..., pattern="^(hostel|supervisor)$")
    
    # Period
    period_start: date
    period_end: date
    
    # Overall stats
    total_feedbacks: int
    average_rating: Decimal
    
    # Rating distribution
    rating_5_count: int
    rating_4_count: int
    rating_3_count: int
    rating_2_count: int
    rating_1_count: int
    
    # Satisfaction metrics
    resolution_satisfaction_rate: Decimal = Field(..., description="% satisfied with resolution")
    response_time_satisfaction_rate: Decimal
    staff_helpfulness_rate: Decimal
    
    # Recommendation
    recommendation_rate: Decimal = Field(..., description="% who would recommend")
    
    # Comments analysis
    positive_feedback_count: int
    negative_feedback_count: int
    common_themes: List[str] = Field(default_factory=list)


class FeedbackAnalysis(BaseSchema):
    """Detailed feedback analysis"""
    hostel_id: UUID
    period_start: date
    period_end: date
    
    # Trend
    rating_trend: List["RatingTrendPoint"]
    
    # By category
    feedback_by_category: dict = Field(..., description="Average rating by complaint category")
    
    # By priority
    feedback_by_priority: dict
    
    # Response time impact
    avg_rating_quick_response: Decimal
    avg_rating_slow_response: Decimal


class RatingTrendPoint(BaseSchema):
    """Rating trend data point"""
    period: str = Field(..., description="Date or week")
    average_rating: Decimal
    feedback_count: int