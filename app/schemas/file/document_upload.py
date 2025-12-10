"""
Document upload-specific schemas
"""
from datetime import date
from typing import Optional, List
from pydantic import Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema
from app.schemas.file.file_upload import FileUploadInitResponse


class DocumentUploadInitRequest(BaseCreateSchema):
    """
    Initialize a document upload.

    For ID proofs, agreements, invoices, etc.
    """
    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(
        ...,
        pattern=r"^(application\/pdf|image\/[a-zA-Z0-9.+-]+)$",
        description="Allowed: PDF or image formats",
    )
    size_bytes: int = Field(
        ...,
        ge=1,
        le=25 * 1024 * 1024,
        description="Max 25MB for documents",
    )

    uploaded_by_user_id: UUID
    student_id: Optional[UUID] = None
    hostel_id: Optional[UUID] = None

    document_type: str = Field(
        ...,
        pattern=(
            r"^(id_proof|address_proof|agreement|invoice|receipt|"
            r"medical_certificate|other)$"
        ),
        description="Type of document",
    )

    # Additional classification
    description: Optional[str] = Field(None, max_length=255)


class DocumentUploadInitResponse(FileUploadInitResponse):
    """Document-specific init response (same as generic for now)"""
    # Can be extended with OCR flags, etc.
    pass


class DocumentValidationResult(BaseSchema):
    """
    Result of backend-side document validation
    (e.g. mime, size, simple content checks).
    """
    storage_key: str
    is_valid: bool
    reason: Optional[str] = Field(None, description="Why invalid, if false")

    # Optional extracted info (non-PII summary)
    extracted_metadata: Optional[dict] = Field(
        None,
        description="e.g. issue_date, expiry_date (if parsed)",
    )


class DocumentInfo(BaseSchema):
    """Document info for student/admin views"""
    id: UUID
    storage_key: str
    url: HttpUrl

    document_type: str
    description: Optional[str]

    uploaded_by_user_id: UUID
    uploaded_by_name: Optional[str]

    uploaded_at: date
    verified: bool
    verified_by: Optional[UUID]
    verified_at: Optional[date]
    verification_notes: Optional[str]


class DocumentList(BaseSchema):
    """List of documents for a student/hostel"""
    owner_type: str = Field(..., pattern="^(student|hostel|system)$")
    owner_id: UUID

    documents: List[DocumentInfo] = Field(default_factory=list)
    total_documents: int