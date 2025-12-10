"""
Review analytics schemas
"""
from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.filters import DateRangeFilter


class ReviewAnalytics(BaseSchema):
    """Comprehensive review analytics"""
    hostel_id: UUID
    hostel_name: str
    
    analysis_period: Optional[DateRangeFilter] = None
    generated_at: datetime
    
    # Summary
    total_reviews: int
    average_rating: Decimal
    
    # Rating distribution
    rating_distribution: "RatingDistribution"
    
    # Detailed ratings
    detailed_ratings_average: Dict[str, Decimal] = Field(
        ...,
        description="Aspect -> average rating"
    )
    
    # Trends
    rating_trend: "TrendAnalysis"
    
    # Sentiment
    sentiment_analysis: Optional["SentimentAnalysis"] = None
    
    # Verification
    verified_reviews_count: int
    verification_rate: Decimal
    
    # Engagement
    average_helpful_votes: Decimal
    response_rate: Decimal


class RatingDistribution(BaseSchema):
    """Rating distribution breakdown"""
    rating_5_count: int
    rating_4_count: int
    rating_3_count: int
    rating_2_count: int
    rating_1_count: int
    
    rating_5_percentage: Decimal
    rating_4_percentage: Decimal
    rating_3_percentage: Decimal
    rating_2_percentage: Decimal
    rating_1_percentage: Decimal
    
    # Aggregated
    positive_reviews: int = Field(..., description="4-5 star reviews")
    neutral_reviews: int = Field(..., description="3 star reviews")
    negative_reviews: int = Field(..., description="1-2 star reviews")
    
    positive_percentage: Decimal
    neutral_percentage: Decimal
    negative_percentage: Decimal


class TrendAnalysis(BaseSchema):
    """Rating trend analysis"""
    trend_direction: str = Field(..., pattern="^(improving|declining|stable)$")
    trend_percentage: Optional[Decimal] = Field(None, description="% change")
    
    # Monthly trend
    monthly_ratings: List["MonthlyRating"] = Field(default_factory=list)
    
    # Recent vs older
    last_30_days_rating: Decimal
    last_90_days_rating: Decimal
    all_time_rating: Decimal


class MonthlyRating(BaseSchema):
    """Monthly rating data"""
    month: str  # YYYY-MM
    average_rating: Decimal
    review_count: int


class SentimentAnalysis(BaseSchema):
    """Sentiment analysis of reviews"""
    overall_sentiment: str = Field(..., pattern="^(positive|neutral|negative)$")
    
    sentiment_score: Decimal = Field(..., ge=-1, le=1, description="Sentiment score")
    
    # Distribution
    positive_count: int
    neutral_count: int
    negative_count: int
    
    # Common themes
    positive_themes: List[str] = Field(default_factory=list, description="Common positive mentions")
    negative_themes: List[str] = Field(default_factory=list, description="Common complaints")
    
    # Keywords
    most_mentioned_positive: List[str] = Field(default_factory=list)
    most_mentioned_negative: List[str] = Field(default_factory=list)


class AspectAnalysis(BaseSchema):
    """Analysis by specific aspects"""
    aspect: str = Field(..., description="cleanliness, food, staff, etc.")
    
    average_rating: Decimal
    total_ratings: int
    
    # Distribution
    rating_distribution: Dict[int, int] = Field(..., description="Rating -> count")
    
    # Trend
    trend: str = Field(..., pattern="^(improving|declining|stable)$")
    
    # Mentions
    mention_count: int
    positive_mentions: int
    negative_mentions: int
    
    # Top comments
    top_positive_comments: List[str] = Field(default_factory=list, max_items=5)
    top_negative_comments: List[str] = Field(default_factory=list, max_items=5)


class CompetitorComparison(BaseSchema):
    """Compare reviews with competitors (if data available)"""
    hostel_id: UUID
    hostel_name: str
    
    this_hostel_rating: Decimal
    competitor_average_rating: Decimal
    
    rating_difference: Decimal
    percentile_rank: Decimal = Field(..., description="Percentile among competitors")
    
    # Strengths
    competitive_advantages: List[str] = Field(
        default_factory=list,
        description="Aspects rated higher than competitors"
    )
    
    # Weaknesses
    improvement_areas: List[str] = Field(
        default_factory=list,
        description="Aspects rated lower than competitors"
    )