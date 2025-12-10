"""
Announcement filter schemas
"""
from datetime import date, datetime
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseFilterSchema
from app.schemas.common.enums import AnnouncementCategory, Priority


class AnnouncementFilterParams(BaseFilterSchema):
    """Announcement filter parameters"""
    # Text search
    search: Optional[str] = Field(None, description="Search in title, content")
    
    # Hostel filter
    hostel_id: Optional[UUID] = None
    hostel_ids: Optional[List[UUID]] = None
    
    # Category
    category: Optional[AnnouncementCategory] = None
    categories: Optional[List[AnnouncementCategory]] = None
    
    # Priority
    priority: Optional[Priority] = None
    priorities: Optional[List[Priority]] = None
    
    # Status
    is_published: Optional[bool] = None
    is_urgent: Optional[bool] = None
    is_pinned: Optional[bool] = None
    
    # Creator
    created_by: Optional[UUID] = None
    created_by_role: Optional[str] = None
    
    # Date filters
    published_date_from: Optional[date] = None
    published_date_to: Optional[date] = None
    created_date_from: Optional[date] = None
    created_date_to: Optional[date] = None
    
    # Expiry
    active_only: Optional[bool] = Field(None, description="Only non-expired announcements")
    expired_only: Optional[bool] = None
    
    # Approval
    approval_pending: Optional[bool] = None


class SearchRequest(BaseFilterSchema):
    """Announcement search"""
    query: str = Field(..., min_length=1)
    hostel_id: Optional[UUID] = None
    
    search_in_title: bool = Field(True)
    search_in_content: bool = Field(True)
    
    category: Optional[AnnouncementCategory] = None
    
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class ArchiveRequest(BaseCreateSchema):
    """Archive old announcements"""
    hostel_id: UUID
    
    # Archive criteria
    archive_before_date: date = Field(..., description="Archive announcements before this date")
    
    # Options
    archive_expired_only: bool = Field(True)
    archive_read_only: bool = Field(False, description="Archive only if all recipients read")
    
    # Exclusions
    exclude_pinned: bool = Field(True)
    exclude_important: bool = Field(True)


class AnnouncementExportRequest(BaseFilterSchema):
    """Export announcements"""
    hostel_id: UUID
    filters: Optional[AnnouncementFilterParams] = None
    
    format: str = Field("pdf", pattern="^(pdf|excel|csv)$")
    
    include_engagement_metrics: bool = Field(True)
    include_recipient_list: bool = Field(False)