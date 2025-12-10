"""
Image upload-specific schemas
"""
from typing import List, Optional
from pydantic import Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema
from app.schemas.file.file_upload import FileUploadInitResponse


class ImageUploadInitRequest(BaseCreateSchema):
    """
    Initialize an image upload.

    Used for hostel photos, room photos, avatars, etc.
    """
    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(
        ...,
        pattern=r"^image\/[a-zA-Z0-9.+-]+$",
        description="Image MIME type, e.g. 'image/jpeg', 'image/png'",
    )
    size_bytes: int = Field(
        ...,
        ge=1,
        le=20 * 1024 * 1024,
        description="Max 20MB for images",
    )

    uploaded_by_user_id: UUID
    hostel_id: Optional[UUID] = None

    # Usage context
    usage: str = Field(
        ...,
        pattern=r"^(hostel_cover|hostel_gallery|room_photo|avatar|document_scan)$",
        description="Intended usage of the image",
    )

    # Optional transformations
    generate_variants: bool = Field(
        True,
        description="If true, system may generate resized variants",
    )


class ImageVariant(BaseSchema):
    """Information about an image variant (thumbnail, medium, etc.)"""
    name: str = Field(..., description="Variant name, e.g. 'thumbnail', 'medium'")
    url: HttpUrl = Field(..., description="URL for this variant")
    width: Optional[int] = Field(None, ge=1)
    height: Optional[int] = Field(None, ge=1)
    size_bytes: Optional[int] = Field(None, ge=0)


class ImageUploadInitResponse(FileUploadInitResponse):
    """
    Image-specific upload init response.

    Extends generic file upload init response with image-specific hints.
    """
    variants_planned: List[str] = Field(
        default_factory=lambda: ["thumbnail", "medium"],
        description="Variants the system will generate after upload (for reference)",
    )


class ImageProcessingResult(BaseSchema):
    """Result of post-upload image processing"""
    storage_key: str
    original_url: HttpUrl
    variants: List[ImageVariant] = Field(default_factory=list)