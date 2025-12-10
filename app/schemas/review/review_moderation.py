"""
Review moderation schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class ModerationRequest(BaseCreateSchema):
    """Submit review for moderation"""
    review_id: UUID
    
    action: str = Field(..., pattern="^(approve|reject|flag|unflag)$")
    
    # If rejecting
    rejection_reason: Optional[str] = Field(None, min_length=20, max_length=500)
    
    # If flagging
    flag_reason: Optional[str] = Field(
        None,
        pattern="^(inappropriate|spam|fake|offensive|other)$"
    )
    flag_details: Optional[str] = Field(None, max_length=1000)
    
    # Moderator notes (internal)
    moderator_notes: Optional[str] = Field(None, max_length=500)


class ModerationResponse(BaseSchema):
    """Moderation response"""
    review_id: UUID
    
    action_taken: str
    moderated_by: UUID
    moderated_by_name: str
    moderated_at: datetime
    
    # Notification sent
    reviewer_notified: bool
    
    message: str


class ModerationQueue(BaseSchema):
    """Moderation queue for reviews"""
    hostel_id: Optional[UUID] = None
    
    total_pending: int
    flagged_reviews: int
    auto_approved: int
    
    pending_reviews: List["PendingReview"]


class PendingReview(BaseSchema):
    """Pending review in moderation queue"""
    review_id: UUID
    hostel_id: UUID
    hostel_name: str
    
    reviewer_name: str
    overall_rating: Decimal
    
    title: str
    review_excerpt: str
    
    is_verified_stay: bool
    
    # Flags
    is_flagged: bool
    flag_count: int
    
    submitted_at: datetime
    
    # Auto-moderation score
    spam_score: Optional[Decimal] = Field(None, ge=0, le=1, description="AI spam detection score")
    sentiment_score: Optional[Decimal] = Field(None, ge=-1, le=1, description="Sentiment analysis")


class ApprovalWorkflow(BaseSchema):
    """Review approval workflow"""
    review_id: UUID
    
    requires_moderation: bool
    moderation_status: str = Field(
        ...,
        pattern="^(pending|approved|rejected|flagged)$"
    )
    
    # Timeline
    submitted_at: datetime
    moderated_at: Optional[datetime]
    
    # Moderator
    moderated_by: Optional[UUID]
    moderated_by_name: Optional[str]
    
    # Reason (if rejected)
    rejection_reason: Optional[str]


class BulkModeration(BaseCreateSchema):
    """Moderate multiple reviews"""
    review_ids: List[UUID] = Field(..., min_items=1, max_items=50)
    
    action: str = Field(..., pattern="^(approve|reject)$")
    
    # Common reason
    reason: Optional[str] = None


class ModerationStats(BaseSchema):
    """Moderation statistics"""
    hostel_id: Optional[UUID]
    period_start: date
    period_end: date
    
    total_reviews: int
    auto_approved: int
    manually_approved: int
    rejected: int
    flagged: int
    
    average_moderation_time_hours: Decimal
    
    # By moderator
    moderations_by_user: dict = Field(default_factory=dict)