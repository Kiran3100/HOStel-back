"""
Student filter and search schemas
"""
from datetime import date
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseFilterSchema
from app.schemas.common.enums import StudentStatus


class StudentFilterParams(BaseFilterSchema):
    """Student filter parameters"""
    # Text search
    search: Optional[str] = Field(None, description="Search in name, email, phone, room number")
    
    # Hostel filter
    hostel_id: Optional[UUID] = None
    hostel_ids: Optional[List[UUID]] = None
    
    # Room filter
    room_id: Optional[UUID] = None
    room_number: Optional[str] = None
    room_type: Optional[str] = None
    floor_number: Optional[int] = None
    
    # Status filter
    status: Optional[StudentStatus] = None
    statuses: Optional[List[StudentStatus]] = None
    is_active: Optional[bool] = None
    
    # Date filters
    checked_in_after: Optional[date] = None
    checked_in_before: Optional[date] = None
    expected_checkout_after: Optional[date] = None
    expected_checkout_before: Optional[date] = None
    
    # Financial filters
    has_overdue_payments: Optional[bool] = None
    security_deposit_paid: Optional[bool] = None
    
    # Meal filter
    mess_subscribed: Optional[bool] = None
    
    # Institutional
    institution_name: Optional[str] = None
    course: Optional[str] = None
    
    # Company
    company_name: Optional[str] = None


class StudentSearchRequest(BaseFilterSchema):
    """Student search request"""
    query: str = Field(..., min_length=1, description="Search query")
    hostel_id: Optional[UUID] = Field(None, description="Limit search to hostel")
    
    # Search fields
    search_in_name: bool = Field(True)
    search_in_email: bool = Field(True)
    search_in_phone: bool = Field(True)
    search_in_room: bool = Field(True)
    search_in_institution: bool = Field(True)
    
    # Filters
    status: Optional[StudentStatus] = None
    
    # Pagination
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class StudentSortOptions(BaseFilterSchema):
    """Student sorting options"""
    sort_by: str = Field(
        "created_at",
        pattern="^(name|email|room_number|check_in_date|created_at|monthly_rent)$"
    )
    sort_order: str = Field("desc", pattern="^(asc|desc)$")


class StudentExportRequest(BaseFilterSchema):
    """Export students request"""
    hostel_id: Optional[UUID] = None
    filters: Optional[StudentFilterParams] = None
    
    # Export format
    format: str = Field("csv", pattern="^(csv|excel|pdf)$")
    
    # Fields to include
    include_financial_data: bool = Field(False)
    include_attendance_data: bool = Field(False)
    include_guardian_info: bool = Field(True)
    include_institutional_info: bool = Field(True)


class StudentBulkActionRequest(BaseFilterSchema):
    """Bulk action on students"""
    student_ids: List[UUID] = Field(..., min_items=1, description="Student IDs")
    action: str = Field(
        ...,
        pattern="^(activate|deactivate|send_notification|export|change_status)$",
        description="Action to perform"
    )
    
    # Action-specific parameters
    new_status: Optional[StudentStatus] = Field(None, description="For change_status action")
    notification_message: Optional[str] = Field(None, description="For send_notification action")