"""
Announcement targeting schemas
"""
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class TargetingConfig(BaseSchema):
    """Targeting configuration for announcement"""
    target_type: str = Field(
        ...,
        pattern="^(all|specific_rooms|specific_floors|specific_students|custom)$",
        description="Targeting type"
    )
    
    # Specific targets
    room_ids: List[UUID] = Field(default_factory=list)
    floor_numbers: List[int] = Field(default_factory=list)
    student_ids: List[UUID] = Field(default_factory=list)
    
    # Exclude
    exclude_student_ids: List[UUID] = Field(default_factory=list, description="Students to exclude")


class AudienceSelection(BaseCreateSchema):
    """Audience selection for announcement"""
    announcement_id: UUID
    
    # Selection criteria
    include_all: bool = Field(False)
    include_active_students: bool = Field(True)
    include_inactive_students: bool = Field(False)
    
    # Filters
    room_types: Optional[List[str]] = Field(None, description="Filter by room types")
    floors: Optional[List[int]] = None
    
    # Specific selection
    specific_room_ids: List[UUID] = Field(default_factory=list)
    specific_student_ids: List[UUID] = Field(default_factory=list)
    
    # Exclusions
    exclude_student_ids: List[UUID] = Field(default_factory=list)


class TargetRooms(BaseCreateSchema):
    """Target specific rooms"""
    announcement_id: UUID
    room_ids: List[UUID] = Field(..., min_items=1, description="Room IDs to target")
    
    # Include all students in these rooms
    include_all_students: bool = Field(True)


class TargetFloors(BaseCreateSchema):
    """Target specific floors"""
    announcement_id: UUID
    floor_numbers: List[int] = Field(..., min_items=1, description="Floor numbers")
    
    # Options
    include_all_rooms: bool = Field(True)


class IndividualTargeting(BaseCreateSchema):
    """Target individual students"""
    announcement_id: UUID
    student_ids: List[UUID] = Field(..., min_items=1, max_items=100, description="Student IDs")


class TargetingSummary(BaseSchema):
    """Summary of who will receive announcement"""
    announcement_id: UUID
    
    targeting_type: str
    
    # Counts
    total_recipients: int
    students_count: int
    rooms_count: int
    floors_count: int
    
    # Breakdown
    recipients_by_room: dict = Field(default_factory=dict, description="Room ID -> student count")
    recipients_by_floor: dict = Field(default_factory=dict, description="Floor -> student count")


class BulkTargeting(BaseCreateSchema):
    """Add multiple targeting rules"""
    announcement_id: UUID
    
    targeting_rules: List[TargetingConfig] = Field(..., min_items=1)
    
    # How to combine rules
    combine_mode: str = Field("union", pattern="^(union|intersection)$")