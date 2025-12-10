"""
Generic file upload schemas (pre-signed URL / direct upload)
"""
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class FileUploadInitRequest(BaseCreateSchema):
    """
    Request to initialize a file upload.

    Typically used to generate a pre-signed URL or
    register a file before multipart upload.
    """
    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(
        ...,
        max_length=255,
        description="MIME type, e.g. 'image/jpeg', 'application/pdf'",
    )
    size_bytes: int = Field(
        ...,
        ge=1,
        le=50 * 1024 * 1024,
        description="Expected file size in bytes (max 50MB by default)",
    )

    # Logical location
    folder: Optional[str] = Field(
        None,
        max_length=255,
        description="Logical folder/path (e.g. 'hostels/123/photos')",
    )

    # Ownership / context
    uploaded_by_user_id: UUID = Field(..., description="User initiating upload")
    hostel_id: Optional[UUID] = Field(
        None,
        description="Hostel context (if file is hostel-specific)",
    )

    # Metadata / classification
    category: Optional[str] = Field(
        None,
        max_length=50,
        description="Category, e.g. 'hostel_photo', 'document', 'avatar'",
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Free-form tags for search/filtering",
    )

    # Access control
    is_public: bool = Field(
        False,
        description="If true, file will be publicly accessible (CDN/public URL)",
    )


class FileUploadInitResponse(BaseResponseSchema):
    """
    Response for upload initialization.

    Either returns a direct upload URL (pre-signed) or
    indicates that the client should upload via the API.
    """
    filename: str
    content_type: str
    size_bytes: int

    storage_key: str = Field(
        ...,
        description="Internal storage key/path for this file",
    )

    # Pre-signed URL (for direct S3/GCS upload)
    upload_url: Optional[str] = Field(
        None,
        description="Pre-signed URL for direct upload to object storage",
    )
    upload_method: str = Field(
        "PUT",
        description="HTTP method to use with upload_url (PUT/POST)",
    )
    upload_headers: Dict[str, str] = Field(
        default_factory=dict,
        description="Any headers that must be included when uploading",
    )

    # Access information
    is_public: bool
    public_url: Optional[str] = Field(
        None,
        description="Public URL if file is/will be public",
    )


class FileUploadCompleteRequest(BaseCreateSchema):
    """
    Notify backend that the client finished uploading the file
    to the storage using the pre-signed URL.
    """
    storage_key: str = Field(..., description="Storage key returned in init response")
    uploaded_by_user_id: UUID = Field(..., description="User who uploaded")
    checksum: Optional[str] = Field(
        None,
        description="Optional checksum/ETag from storage to verify integrity",
    )