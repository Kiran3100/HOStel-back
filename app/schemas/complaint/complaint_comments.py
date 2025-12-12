"""
Complaint comments/discussion schemas with threading support.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field, HttpUrl, field_validator, computed_field

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class CommentCreate(BaseCreateSchema):
    """Create comment on complaint with validation."""
    
    complaint_id: UUID = Field(..., description="Complaint ID")
    
    comment_text: str = Field(..., min_length=5, max_length=1000, description="Comment text")
    
    # Internal or public
    is_internal: bool = Field(False, description="Internal note vs public comment")
    
    # Attachments
    attachments: List[HttpUrl] = Field(default_factory=list, max_items=5)

    @field_validator("comment_text")
    @classmethod
    def validate_comment_text(cls, v: str) -> str:
        """Validate comment text is meaningful."""
        v = v.strip()
        if len(v.split()) < 2:
            raise ValueError("Comment must contain at least 2 words")
        return v


class CommentResponse(BaseResponseSchema):
    """Comment response with user information."""
    
    complaint_id: UUID
    
    commented_by: UUID
    commented_by_name: str
    commented_by_role: str
    
    comment_text: str
    is_internal: bool
    
    attachments: List[str]
    
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def is_edited(self) -> bool:
        """Check if comment was edited."""
        return self.updated_at > self.created_at

    @computed_field
    @property
    def time_ago(self) -> str:
        """Get human-readable time since comment."""
        delta = datetime.utcnow() - self.created_at
        
        if delta.days > 365:
            return f"{delta.days // 365} year{'s' if delta.days // 365 > 1 else ''} ago"
        elif delta.days > 30:
            return f"{delta.days // 30} month{'s' if delta.days // 30 > 1 else ''} ago"
        elif delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"


class CommentList(BaseSchema):
    """List of comments with metadata."""
    
    complaint_id: UUID
    complaint_number: str
    
    total_comments: int = Field(..., ge=0)
    public_comments: int = Field(..., ge=0)
    internal_notes: int = Field(..., ge=0)
    
    comments: List[CommentResponse]

    @computed_field
    @property
    def has_internal_notes(self) -> bool:
        """Check if there are any internal notes."""
        return self.internal_notes > 0

    @computed_field
    @property
    def last_comment_at(self) -> Optional[datetime]:
        """Get timestamp of last comment."""
        if self.comments:
            return max(comment.created_at for comment in self.comments)
        return None


class CommentUpdate(BaseCreateSchema):
    """Update comment with validation."""
    
    comment_id: UUID
    comment_text: str = Field(..., min_length=5, max_length=1000)

    @field_validator("comment_text")
    @classmethod
    def validate_updated_text(cls, v: str) -> str:
        """Validate updated comment text."""
        v = v.strip()
        if len(v.split()) < 2:
            raise ValueError("Updated comment must contain at least 2 words")
        return v


class CommentDelete(BaseCreateSchema):
    """Delete comment with optional reason."""
    
    comment_id: UUID
    reason: Optional[str] = Field(None, max_length=200)

    @field_validator("reason")
    @classmethod
    def validate_deletion_reason(cls, v: Optional[str]) -> Optional[str]:
        """Validate deletion reason if provided."""
        if v:
            v = v.strip()
            if len(v) < 5:
                raise ValueError("Deletion reason must be at least 5 characters")
        return v


class MentionNotification(BaseSchema):
    """Notification when mentioned in comment."""
    
    comment_id: UUID
    complaint_id: UUID
    complaint_number: str
    
    mentioned_by: UUID
    mentioned_by_name: str
    
    comment_excerpt: str
    
    comment_url: str

    @computed_field
    @property
    def notification_title(self) -> str:
        """Generate notification title."""
        return f"{self.mentioned_by_name} mentioned you in complaint {self.complaint_number}"