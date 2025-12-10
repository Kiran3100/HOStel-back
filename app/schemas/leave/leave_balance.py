"""
Leave balance schemas
"""
from datetime import date
from typing import List
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.enums import LeaveType


class LeaveBalance(BaseSchema):
    """Leave balance for a single leave type"""
    leave_type: LeaveType
    allocated_per_year: int = Field(..., ge=0)
    used_days: int = Field(..., ge=0)
    remaining_days: int = Field(..., ge=0)


class LeaveBalanceSummary(BaseSchema):
    """Overall leave balance for a student"""
    student_id: UUID
    student_name: str
    hostel_id: UUID
    hostel_name: str

    academic_year_start: date
    academic_year_end: date

    balances: List[LeaveBalance] = Field(default_factory=list)