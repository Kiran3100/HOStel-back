"""
Bed base schemas
"""
from datetime import date
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import BedStatus


class BedBase(BaseSchema):
    """Base bed schema"""
    room_id: UUID = Field(..., description="Room ID")
    bed_number: str = Field(..., min_length=1, max_length=10, description="Bed identifier (A1, B2, etc.)")
    status: BedStatus = Field(BedStatus.AVAILABLE, description="Bed status")


class BedCreate(BedBase, BaseCreateSchema):
    """Create bed schema"""
    pass


class BedUpdate(BaseUpdateSchema):
    """Update bed schema"""
    bed_number: Optional[str] = Field(None, min_length=1, max_length=10)
    status: Optional[BedStatus] = None
    is_occupied: Optional[bool] = None


class BulkBedCreate(BaseCreateSchema):
    """Bulk create beds for a room"""
    room_id: UUID = Field(..., description="Room ID")
    bed_count: int = Field(..., ge=1, le=20, description="Number of beds to create")
    bed_prefix: str = Field("B", description="Bed number prefix")
    start_number: int = Field(1, ge=1, description="Starting number for beds")


class BedAssignmentRequest(BaseCreateSchema):
    """Assign bed to student"""
    bed_id: UUID = Field(..., description="Bed ID to assign")
    student_id: UUID = Field(..., description="Student ID")
    occupied_from: date = Field(..., description="Occupancy start date")


class BedReleaseRequest(BaseCreateSchema):
    """Release bed from student"""
    bed_id: UUID = Field(..., description="Bed ID to release")
    release_date: date = Field(..., description="Release date")
    reason: Optional[str] = Field(None, description="Release reason")