"""
Supervisor response schemas
"""
from datetime import date, datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import SupervisorStatus, EmploymentType


class SupervisorResponse(BaseResponseSchema):
    """Supervisor response schema"""
    user_id: UUID
    full_name: str
    email: str
    phone: str
    
    assigned_hostel_id: UUID
    hostel_name: str
    
    employee_id: Optional[str]
    join_date: date
    employment_type: EmploymentType
    
    status: SupervisorStatus
    is_active: bool
    
    assigned_by: UUID
    assigned_date: date


class SupervisorDetail(BaseResponseSchema):
    """Detailed supervisor information"""
    # User information
    user_id: UUID
    full_name: str
    email: str
    phone: str
    profile_image_url: Optional[str]
    
    # Hostel assignment
    assigned_hostel_id: UUID
    hostel_name: str
    assigned_by: UUID
    assigned_by_name: str
    assigned_date: date
    
    # Employment
    employee_id: Optional[str]
    join_date: date
    employment_type: EmploymentType
    shift_timing: Optional[str]
    
    # Status
    status: SupervisorStatus
    is_active: bool
    termination_date: Optional[date]
    termination_reason: Optional[str]
    
    # Permissions
    permissions: dict = Field(default_factory=dict)
    
    # Performance
    total_complaints_resolved: int
    average_resolution_time_hours: Decimal
    last_performance_review: Optional[date]
    performance_rating: Optional[Decimal]
    
    # Activity
    last_login: Optional[datetime]
    total_logins: int


class SupervisorListItem(BaseSchema):
    """Supervisor list item"""
    id: UUID
    user_id: UUID
    full_name: str
    email: str
    phone: str
    hostel_name: str
    employee_id: Optional[str]
    employment_type: EmploymentType
    status: SupervisorStatus
    is_active: bool
    join_date: date
    performance_rating: Optional[Decimal]


class SupervisorSummary(BaseSchema):
    """Supervisor summary for hostel"""
    supervisor_id: UUID
    full_name: str
    email: str
    phone: str
    employee_id: Optional[str]
    status: SupervisorStatus
    shift_timing: Optional[str]
    
    # Quick stats
    complaints_handled_this_month: int
    attendance_records_this_month: int
    last_active: Optional[datetime]