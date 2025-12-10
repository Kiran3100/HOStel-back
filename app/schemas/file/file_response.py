"""
File information and listing schemas
"""
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema


class FileMetadata(BaseSchema):
    """Additional metadata attached to a file"""
    content_type: str = Field(..., description="MIME type")
    size_bytes: int = Field(..., ge=0, description="File size in bytes")

    # Optional metadata
    original_filename: Optional[str] = Field(None, description="Original filename")
    tags: List[str] = Field(default_factory=list)
    category: Optional[str] = Field(None, description="Logical category")
    custom_metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Free-form key/value metadata (e.g. 'room_id', 'hostel_id')",
    )


class FileInfo(BaseResponseSchema):
    """Full file information as stored in the system"""
    storage_key: str = Field(..., description="Storage path/key (unique)")

    # Ownership / context
    uploaded_by_user_id: UUID
    hostel_id: Optional[UUID] = None

    # Access
    is_public: bool = Field(False, description="Publicly accessible or not")
    public_url: Optional[HttpUrl] = Field(None, description="Public CDN URL if is_public=True")
    signed_url: Optional[HttpUrl] = Field(
        None,
        description="Signed temporary URL for private access (optional)",
    )

    # Metadata
    metadata: FileMetadata

    # Audit
    created_at: datetime
    updated_at: datetime


class FileURL(BaseSchema):
    """Simple container for a file URL"""
    url: HttpUrl
    expires_at: Optional[datetime] = Field(
        None,
        description="If signed URL, when it will expire",
    )


class FileListResponse(BaseSchema):
    """Paginated list of files"""
    items: List[FileInfo] = Field(default_factory=list)
    total_items: int
    page: int
    page_size: int