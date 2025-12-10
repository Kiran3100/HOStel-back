"""
Review voting (helpful/not helpful) schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema
from app.schemas.common.enums import VoteType


class VoteRequest(BaseCreateSchema):
    """Vote on review helpfulness"""
    review_id: UUID = Field(..., description="Review ID")
    voter_id: UUID = Field(..., description="User voting")
    
    vote_type: VoteType = Field(..., description="helpful or not_helpful")


class VoteResponse(BaseSchema):
    """Vote response"""
    review_id: UUID
    vote_type: VoteType
    
    # Updated counts
    helpful_count: int
    not_helpful_count: int
    
    message: str


class HelpfulnessScore(BaseSchema):
    """Helpfulness score for review"""
    review_id: UUID
    
    helpful_count: int
    not_helpful_count: int
    total_votes: int
    
    helpfulness_percentage: Decimal = Field(
        ...,
        description="% of voters who found it helpful"
    )
    
    helpfulness_score: Decimal = Field(
        ...,
        ge=0,
        le=1,
        description="Wilson score for ranking"
    )


class VoteHistory(BaseSchema):
    """User's voting history"""
    user_id: UUID
    
    total_votes: int
    helpful_votes: int
    not_helpful_votes: int
    
    recent_votes: List["VoteHistoryItem"] = Field(default_factory=list, max_items=10)


class VoteHistoryItem(BaseSchema):
    """Individual vote in history"""
    review_id: UUID
    hostel_name: str
    vote_type: VoteType
    voted_at: datetime


class RemoveVote(BaseCreateSchema):
    """Remove vote (change mind)"""
    review_id: UUID
    voter_id: UUID