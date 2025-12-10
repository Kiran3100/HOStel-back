"""
File management schemas package
"""

from app.schemas.file.file_upload import (
    FileUploadInitRequest,
    FileUploadInitResponse,
    FileUploadCompleteRequest,
)
from app.schemas.file.file_response import (
    FileInfo,
    FileMetadata,
    FileURL,
    FileListResponse,
)
from app.schemas.file.image_upload import (
    ImageUploadInitRequest,
    ImageUploadInitResponse,
    ImageVariant,
)
from app.schemas.file.document_upload import (
    DocumentUploadInitRequest,
    DocumentUploadInitResponse,
    DocumentValidationResult,
)

__all__ = [
    # Generic file
    "FileUploadInitRequest",
    "FileUploadInitResponse",
    "FileUploadCompleteRequest",
    "FileInfo",
    "FileMetadata",
    "FileURL",
    "FileListResponse",
    # Images
    "ImageUploadInitRequest",
    "ImageUploadInitResponse",
    "ImageVariant",
    # Documents
    "DocumentUploadInitRequest",
    "DocumentUploadInitResponse",
    "DocumentValidationResult",
]