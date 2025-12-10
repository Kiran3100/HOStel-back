# api/v1/files/documents.py
from __future__ import annotations

from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from api import deps
from app.core.exceptions import (
    ServiceError,
    NotFoundError,
    ValidationError,
    ConflictError,
)
from app.schemas.file.document_upload import (
    DocumentUploadInitRequest,
    DocumentUploadInitResponse,
    DocumentValidationResult,
    DocumentInfo,
    DocumentList,
)
from app.services.file import DocumentService

router = APIRouter(prefix="/documents")


def _map_service_error(exc: ServiceError) -> HTTPException:
    if isinstance(exc, NotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, ValidationError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )
    if isinstance(exc, ConflictError):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )


@router.post(
    "/init",
    response_model=DocumentUploadInitResponse,
    status_code=status.HTTP_200_OK,
    summary="Initialize a document upload",
)
async def init_document_upload(
    payload: DocumentUploadInitRequest,
    document_service: Annotated[DocumentService, Depends(deps.get_document_service)],
) -> DocumentUploadInitResponse:
    """
    Initialize a document upload (KYC, ID proofs, etc.) with appropriate
    folder and metadata.
    """
    try:
        return document_service.init_upload(payload)
    except ServiceError as exc:
        raise _map_service_error(exc)


@router.post(
    "/{document_id}/validate",
    response_model=DocumentValidationResult,
    status_code=status.HTTP_200_OK,
    summary="Validate an uploaded document",
)
async def validate_document(
    document_id: UUID = Path(..., description="Document ID"),
    document_service: Annotated[DocumentService, Depends(deps.get_document_service)],
) -> DocumentValidationResult:
    """
    Trigger backend validation for an uploaded document (format checks,
    content validation, expiry checks, etc.).
    """
    try:
        return document_service.validate_document(document_id=document_id)
    except ServiceError as exc:
        raise _map_service_error(exc)


@router.get(
    "",
    response_model=DocumentList,
    summary="List documents",
)
async def list_documents(
    owner_id: Optional[UUID] = Query(
        None,
        description="Optional owner/user ID filter",
    ),
    hostel_id: Optional[UUID] = Query(
        None,
        description="Optional hostel filter",
    ),
    doc_type: Optional[str] = Query(
        None,
        description="Optional document type filter",
    ),
    document_service: Annotated[DocumentService, Depends(deps.get_document_service)],
) -> DocumentList:
    """
    List documents, optionally filtered by owner, hostel, or document type.
    """
    try:
        return document_service.list_documents(
            owner_id=owner_id,
            hostel_id=hostel_id,
            doc_type=doc_type,
        )
    except ServiceError as exc:
        raise _map_service_error(exc)


@router.get(
    "/{document_id}",
    response_model=DocumentInfo,
    summary="Get document details",
)
async def get_document(
    document_id: UUID = Path(..., description="Document ID"),
    document_service: Annotated[DocumentService, Depends(deps.get_document_service)],
) -> DocumentInfo:
    """
    Retrieve detailed document information including URLs and verification status.
    """
    try:
        return document_service.get_document(document_id=document_id)
    except ServiceError as exc:
        raise _map_service_error(exc)