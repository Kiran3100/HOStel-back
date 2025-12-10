"""
Supervisor profile schemas
"""
from datetime import date
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseUpdateSchema
from app.schemas.common.enums import EmploymentType, SupervisorStatus


class SupervisorProfile(BaseSchema):
    """Complete supervisor profile"""
    id: UUID
    user_id: UUID
    full_name: str
    email: str
    phone: str
    profile_image_url: Optional[str]
    
    # Assignment
    hostel_id: UUID
    hostel_name: str
    
    # Employment
    employment: "SupervisorEmployment"
    
    # Permissions
    permissions: dict
    
    # Performance
    performance_summary: "PerformanceSummary"


class SupervisorEmployment(BaseSchema):
    """Supervisor employment details"""
    employee_id: Optional[str]
    join_date: date
    employment_type: EmploymentType
    shift_timing: Optional[str]
    
    status: SupervisorStatus
    is_active: bool
    
    # If terminated
    termination_date: Optional[date]
    termination_reason: Optional[str]
    
    # Assigned by
    assigned_by: UUID
    assigned_by_name: str
    assigned_date: date


class PerformanceSummary(BaseSchema):
    """Performance summary"""
    total_complaints_resolved: int
    average_resolution_time_hours: Decimal
    total_attendance_records: int
    total_maintenance_requests: int
    
    current_month_complaints: int
    current_month_attendance_records: int
    
    performance_rating: Optional[Decimal]
    last_performance_review: Optional[date]


class SupervisorProfileUpdate(BaseUpdateSchema):
    """Update supervisor profile (supervisor can update own profile)"""
    # Contact updates (requires admin approval)
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{9,14}$')
    
    # Shift preference (requires admin approval)
    preferred_shift_timing: Optional[str] = None
    
    # Personal notes
    notes: Optional[str] = Field(None, max_length=1000)