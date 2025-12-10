"""
Complaint comments/discussion schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class CommentCreate(BaseCreateSchema):
    """Create comment on complaint"""
    complaint_id: UUID = Field(..., description="Complaint ID")
    
    comment_text: str = Field(..., min_length=5, max_length=1000, description="Comment text")
    
    # Internal or public
    is_internal: bool = Field(False, description="Internal note vs public comment")
    
    # Attachments
    attachments: List[HttpUrl] = Field(default_factory=list)


class CommentResponse(BaseResponseSchema):
    """Comment response"""
    complaint_id: UUID
    
    commented_by: UUID
    commented_by_name: str
    commented_by_role: str
    
    comment_text: str
    is_internal: bool
    
    attachments: List[str]
    
    created_at: datetime
    updated_at: datetime


class CommentList(BaseSchema):
    """List of comments for complaint"""
    complaint_id: UUID
    complaint_number: str
    
    total_comments: int
    public_comments: int
    internal_notes: int
    
    comments: List[CommentResponse]


class CommentUpdate(BaseCreateSchema):
    """Update comment"""
    comment_id: UUID
    comment_text: str = Field(..., min_length=5, max_length=1000)


class CommentDelete(BaseCreateSchema):
    """Delete comment"""
    comment_id: UUID
    reason: Optional[str] = Field(None, max_length=200)


class MentionNotification(BaseSchema):
    """Notification when mentioned in comment"""
    comment_id: UUID
    complaint_id: UUID
    complaint_number: str
    
    mentioned_by: UUID
    mentioned_by_name: str
    
    comment_excerpt: str
    
    comment_url: str