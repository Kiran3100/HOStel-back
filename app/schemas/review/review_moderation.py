# --- File: app/schemas/review/review_moderation.py ---
"""
Review moderation and approval workflow schemas.

Handles review moderation queue, approval/rejection, and flagging.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import Field, field_validator
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema

__all__ = [
    "ModerationRequest",
    "ModerationResponse",
    "ModerationQueue",
    "PendingReview",
    "ApprovalWorkflow",
    "BulkModeration",
    "ModerationStats",
    "FlagReview",
]


class ModerationRequest(BaseCreateSchema):
    """
    Review moderation action request.
    
    Supports approval, rejection, and flagging of reviews.
    """
    
    review_id: UUID = Field(..., description="Review to moderate")
    
    action: str = Field(
        ...,
        pattern=r"^(approve|reject|flag|unflag|hold)$",
        description="Moderation action to take",
    )
    
    # Rejection details
    rejection_reason: Optional[str] = Field(
        None,
        min_length=20,
        max_length=500,
        description="Reason for rejection (required if action=reject)",
    )
    
    # Flagging details
    flag_reason: Optional[str] = Field(
        None,
        pattern=r"^(inappropriate|spam|fake|offensive|profanity|other)$",
        description="Reason for flagging (required if action=flag)",
    )
    flag_details: Optional[str] = Field(
        None,
        max_length=1000,
        description="Additional flagging details",
    )
    
    # Internal notes
    moderator_notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Internal moderator notes (not visible to reviewer)",
    )
    
    # Notification control
    notify_reviewer: bool = Field(
        True,
        description="Send notification to reviewer about moderation action",
    )
    
    @field_validator("action")
    @classmethod
    def normalize_action(cls, v: str) -> str:
        """Normalize action to lowercase."""
        return v.lower().strip()
    
    @model_validator(mode="after")
    def validate_action_requirements(self) -> "ModerationRequest":
        """Validate that required fields are provided for specific actions."""
        if self.action == "reject" and not self.rejection_reason:
            raise ValueError(
                "rejection_reason is required when action is 'reject'"
            )
        
        if self.action == "flag" and not self.flag_reason:
            raise ValueError(
                "flag_reason is required when action is 'flag'"
            )
        
        return self


class FlagReview(BaseCreateSchema):
    """
    User-initiated review flagging.
    
    Allows users to report inappropriate or problematic reviews.
    """
    
    review_id: UUID = Field(..., description="Review to flag")
    reporter_id: UUID = Field(..., description="User reporting the review")
    
    flag_reason: str = Field(
        ...,
        pattern=r"^(inappropriate|spam|fake|offensive|profanity|not_relevant|other)$",
        description="Reason for flagging",
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Detailed description of the issue",
    )
    
    @field_validator("flag_reason")
    @classmethod
    def normalize_flag_reason(cls, v: str) -> str:
        """Normalize flag reason to lowercase."""
        return v.lower().strip()


class ModerationResponse(BaseSchema):
    """Response after moderation action."""
    
    review_id: UUID = Field(..., description="Moderated review ID")
    
    action_taken: str = Field(
        ...,
        description="Action that was performed",
    )
    moderated_by: UUID = Field(..., description="Moderator user ID")
    moderated_by_name: str = Field(..., description="Moderator name")
    moderated_at: datetime = Field(..., description="Moderation timestamp")
    
    # Notification status
    reviewer_notified: bool = Field(
        ...,
        description="Whether reviewer was notified",
    )
    
    message: str = Field(
        ...,
        description="Result message",
        examples=["Review approved successfully"],
    )


class PendingReview(BaseSchema):
    """
    Review pending moderation.
    
    Represents a review in the moderation queue.
    """
    
    review_id: UUID = Field(..., description="Review ID")
    hostel_id: UUID = Field(..., description="Hostel ID")
    hostel_name: str = Field(..., description="Hostel name")
    
    # Reviewer info
    reviewer_id: UUID = Field(..., description="Reviewer ID")
    reviewer_name: str = Field(..., description="Reviewer name")
    overall_rating: Decimal = Field(
        ...,
        ge=Decimal("1.0"),
        le=Decimal("5.0"),
        description="Overall rating",
    )
    
    # Content preview
    title: str = Field(..., description="Review title")
    review_excerpt: str = Field(
        ...,
        max_length=200,
        description="Review text excerpt (first 200 chars)",
    )
    
    # Verification
    is_verified_stay: bool = Field(
        ...,
        description="Whether stay is verified",
    )
    
    # Flags and issues
    is_flagged: bool = Field(..., description="Whether review is flagged")
    flag_count: int = Field(
        ...,
        ge=0,
        description="Number of times review has been flagged",
    )
    flag_reasons: List[str] = Field(
        default_factory=list,
        description="Reasons for flagging",
    )
    
    # Timestamps
    submitted_at: datetime = Field(..., description="Review submission time")
    
    # AI moderation scores
    spam_score: Optional[Decimal] = Field(
        None,
        ge=Decimal("0"),
        le=Decimal("1"),
        description="AI spam detection score (0-1, higher = more likely spam)",
    )
    sentiment_score: Optional[Decimal] = Field(
        None,
        ge=Decimal("-1"),
        le=Decimal("1"),
        description="Sentiment analysis score (-1 to 1)",
    )
    toxicity_score: Optional[Decimal] = Field(
        None,
        ge=Decimal("0"),
        le=Decimal("1"),
        description="Content toxicity score (0-1, higher = more toxic)",
    )
    
    # Priority indicators
    requires_immediate_attention: bool = Field(
        default=False,
        description="Whether review needs urgent moderation",
    )


class ModerationQueue(BaseSchema):
    """
    Moderation queue overview.
    
    Summary of reviews pending moderation.
    """
    
    hostel_id: Optional[UUID] = Field(
        None,
        description="Filter by specific hostel (None = all hostels)",
    )
    
    # Queue statistics
    total_pending: int = Field(..., ge=0, description="Total pending reviews")
    flagged_reviews: int = Field(..., ge=0, description="Flagged reviews count")
    auto_approved: int = Field(..., ge=0, description="Auto-approved count")
    high_priority: int = Field(
        ...,
        ge=0,
        description="High priority items needing attention",
    )
    
    # Reviews in queue
    pending_reviews: List[PendingReview] = Field(
        default_factory=list,
        description="List of pending reviews",
    )
    
    # Queue health
    average_wait_time_hours: Optional[Decimal] = Field(
        None,
        ge=Decimal("0"),
        description="Average time reviews spend in queue",
    )
    oldest_review_age_hours: Optional[Decimal] = Field(
        None,
        ge=Decimal("0"),
        description="Age of oldest pending review",
    )


class ApprovalWorkflow(BaseSchema):
    """
    Review approval workflow status.
    
    Tracks the complete moderation lifecycle of a review.
    """
    
    review_id: UUID = Field(..., description="Review ID")
    
    # Workflow status
    requires_moderation: bool = Field(
        ...,
        description="Whether review requires manual moderation",
    )
    moderation_status: str = Field(
        ...,
        pattern=r"^(pending|approved|rejected|flagged|on_hold)$",
        description="Current moderation status",
    )
    
    # Timeline
    submitted_at: datetime = Field(..., description="Submission timestamp")
    moderated_at: Optional[datetime] = Field(
        None,
        description="Moderation completion timestamp",
    )
    published_at: Optional[datetime] = Field(
        None,
        description="Publication timestamp (if approved)",
    )
    
    # Moderator info
    moderated_by: Optional[UUID] = Field(None, description="Moderator user ID")
    moderated_by_name: Optional[str] = Field(None, description="Moderator name")
    
    # Rejection/flagging details
    rejection_reason: Optional[str] = Field(
        None,
        description="Reason for rejection",
    )
    flag_reasons: List[str] = Field(
        default_factory=list,
        description="List of flag reasons",
    )
    
    # Auto-moderation
    auto_moderation_score: Optional[Decimal] = Field(
        None,
        ge=Decimal("0"),
        le=Decimal("1"),
        description="Automated moderation confidence score",
    )
    auto_approved: bool = Field(
        default=False,
        description="Whether review was auto-approved",
    )


class BulkModeration(BaseCreateSchema):
    """
    Bulk moderation of multiple reviews.
    
    Allows moderators to process multiple reviews at once.
    """
    
    review_ids: List[UUID] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Reviews to moderate (max 50)",
    )
    
    action: str = Field(
        ...,
        pattern=r"^(approve|reject|flag)$",
        description="Action to apply to all reviews",
    )
    
    # Common reason/notes
    reason: Optional[str] = Field(
        None,
        max_length=500,
        description="Common reason for all reviews",
    )
    
    notify_reviewers: bool = Field(
        True,
        description="Send notifications to all affected reviewers",
    )
    
    @field_validator("review_ids")
    @classmethod
    def validate_review_ids(cls, v: List[UUID]) -> List[UUID]:
        """Validate review IDs list."""
        if len(v) > 50:
            raise ValueError("Maximum 50 reviews can be moderated at once")
        
        # Remove duplicates
        unique_ids = list(set(v))
        if len(unique_ids) != len(v):
            raise ValueError("Duplicate review IDs found")
        
        return v
    
    @field_validator("action")
    @classmethod
    def normalize_action(cls, v: str) -> str:
        """Normalize action to lowercase."""
        return v.lower().strip()


class ModerationStats(BaseSchema):
    """
    Moderation statistics and metrics.
    
    Provides insights into moderation performance and volume.
    """
    
    hostel_id: Optional[UUID] = Field(
        None,
        description="Hostel filter (None = all hostels)",
    )
    period_start: date = Field(..., description="Statistics period start")
    period_end: date = Field(..., description="Statistics period end")
    
    # Volume metrics
    total_reviews: int = Field(..., ge=0, description="Total reviews received")
    auto_approved: int = Field(..., ge=0, description="Auto-approved count")
    manually_approved: int = Field(
        ...,
        ge=0,
        description="Manually approved count",
    )
    rejected: int = Field(..., ge=0, description="Rejected count")
    flagged: int = Field(..., ge=0, description="Flagged count")
    
    # Performance metrics
    average_moderation_time_hours: Decimal = Field(
        ...,
        ge=Decimal("0"),
        description="Average time to moderate (in hours)",
    )
    median_moderation_time_hours: Optional[Decimal] = Field(
        None,
        ge=Decimal("0"),
        description="Median moderation time",
    )
    
    # By moderator
    moderations_by_user: Dict[str, int] = Field(
        default_factory=dict,
        description="Moderator ID/name to moderation count mapping",
    )
    
    # Quality metrics
    approval_rate: Decimal = Field(
        ...,
        ge=Decimal("0"),
        le=Decimal("100"),
        description="Percentage of reviews approved",
    )
    rejection_rate: Decimal = Field(
        ...,
        ge=Decimal("0"),
        le=Decimal("100"),
        description="Percentage of reviews rejected",
    )
    auto_approval_accuracy: Optional[Decimal] = Field(
        None,
        ge=Decimal("0"),
        le=Decimal("100"),
        description="Accuracy of auto-approval system",
    )
    
    @field_validator("period_end")
    @classmethod
    def validate_period(cls, v: date, info) -> date:
        """Validate period end is after start."""
        period_start = info.data.get("period_start")
        if period_start and v < period_start:
            raise ValueError("period_end must be on or after period_start")
        return v