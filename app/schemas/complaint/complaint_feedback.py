"""
Complaint feedback schemas with analytics support.
"""
from __future__ import annotations

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from pydantic import Field, field_validator, computed_field

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class FeedbackRequest(BaseCreateSchema):
    """Submit feedback on resolved complaint with validation."""
    
    complaint_id: UUID = Field(..., description="Complaint ID")
    
    rating: int = Field(..., ge=1, le=5, description="Rating 1-5")
    
    feedback: Optional[str] = Field(None, max_length=1000, description="Detailed feedback")
    
    # Satisfaction questions
    issue_resolved_satisfactorily: bool = Field(..., description="Was issue resolved well?")
    response_time_satisfactory: bool = Field(..., description="Was response time good?")
    staff_helpful: bool = Field(..., description="Was staff helpful?")
    
    # Would recommend
    would_recommend: Optional[bool] = Field(None, description="Would recommend complaint system")

    @field_validator("feedback")
    @classmethod
    def validate_feedback(cls, v: Optional[str]) -> Optional[str]:
        """Validate feedback if provided."""
        if v:
            v = v.strip()
            if len(v) < 10:
                raise ValueError("Feedback must be at least 10 characters if provided")
        return v

    @field_validator("rating")
    @classmethod
    def validate_rating_with_feedback(cls, v: int, info) -> int:
        """Ensure low ratings have feedback."""
        feedback = info.data.get("feedback")
        if v <= 2 and not feedback:
            raise ValueError("Please provide feedback for ratings 2 or below")
        return v


class FeedbackResponse(BaseResponseSchema):
    """Feedback response with confirmation."""
    
    complaint_id: UUID
    complaint_number: str
    
    rating: int
    feedback: Optional[str]
    
    submitted_by: UUID
    submitted_at: datetime
    
    message: str

    @classmethod
    def create(
        cls,
        complaint_id: UUID,
        complaint_number: str,
        rating: int,
        feedback: Optional[str],
        submitted_by: UUID
    ) -> "FeedbackResponse":
        """Factory method to create feedback response."""
        return cls(
            complaint_id=complaint_id,
            complaint_number=complaint_number,
            rating=rating,
            feedback=feedback,
            submitted_by=submitted_by,
            submitted_at=datetime.utcnow(),
            message="Thank you for your feedback!"
        )


class FeedbackSummary(BaseSchema):
    """Feedback summary with calculated metrics."""
    
    entity_id: UUID
    entity_type: str = Field(..., pattern="^(hostel|supervisor)$")
    
    # Period
    period_start: date
    period_end: date
    
    # Overall stats
    total_feedbacks: int = Field(..., ge=0)
    average_rating: Decimal = Field(..., ge=1, le=5)
    
    # Rating distribution
    rating_5_count: int = Field(..., ge=0)
    rating_4_count: int = Field(..., ge=0)
    rating_3_count: int = Field(..., ge=0)
    rating_2_count: int = Field(..., ge=0)
    rating_1_count: int = Field(..., ge=0)
    
    # Satisfaction metrics
    resolution_satisfaction_rate: Decimal = Field(..., ge=0, le=100, description="% satisfied with resolution")
    response_time_satisfaction_rate: Decimal = Field(..., ge=0, le=100)
    staff_helpfulness_rate: Decimal = Field(..., ge=0, le=100)
    
    # Recommendation
    recommendation_rate: Decimal = Field(..., ge=0, le=100, description="% who would recommend")
    
    # Comments analysis
    positive_feedback_count: int = Field(..., ge=0)
    negative_feedback_count: int = Field(..., ge=0)
    common_themes: List[str] = Field(default_factory=list, max_items=10)

    @computed_field
    @property
    def satisfaction_score(self) -> Decimal:
        """Calculate overall satisfaction score."""
        weights = {
            "rating": Decimal("0.4"),
            "resolution": Decimal("0.3"),
            "response": Decimal("0.2"),
            "staff": Decimal("0.1")
        }
        
        score = (
            (self.average_rating / 5) * 100 * weights["rating"] +
            self.resolution_satisfaction_rate * weights["resolution"] +
            self.response_time_satisfaction_rate * weights["response"] +
            self.staff_helpfulness_rate * weights["staff"]
        )
        
        return round(score, 2)

    @computed_field
    @property
    def performance_grade(self) -> str:
        """Get performance grade based on satisfaction score."""
        score = self.satisfaction_score
        
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        else:
            return "D"


class FeedbackAnalysis(BaseSchema):
    """Detailed feedback analysis with trends."""
    
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
    avg_rating_quick_response: Decimal = Field(..., ge=1, le=5)
    avg_rating_slow_response: Decimal = Field(..., ge=1, le=5)

    @computed_field
    @property
    def response_time_impact(self) -> Decimal:
        """Calculate impact of response time on ratings."""
        return self.avg_rating_quick_response - self.avg_rating_slow_response

    @computed_field
    @property
    def trend_direction(self) -> str:
        """Determine if ratings are improving or declining."""
        if len(self.rating_trend) < 2:
            return "stable"
            
        # Compare first and last periods
        first_avg = self.rating_trend[0].average_rating
        last_avg = self.rating_trend[-1].average_rating
        
        if last_avg > first_avg + Decimal("0.2"):
            return "improving"
        elif last_avg < first_avg - Decimal("0.2"):
            return "declining"
        else:
            return "stable"


class RatingTrendPoint(BaseSchema):
    """Rating trend data point."""
    
    period: str = Field(..., description="Date or week")
    average_rating: Decimal = Field(..., ge=1, le=5)
    feedback_count: int = Field(..., ge=0)

    @computed_field
    @property
    def is_significant(self) -> bool:
        """Check if this data point has enough feedback to be significant."""
        return self.feedback_count >= 5