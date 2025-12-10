"""
Preventive maintenance schedule schemas
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema
from app.schemas.common.enums import MaintenanceCategory, MaintenanceRecurrence


class PreventiveSchedule(BaseResponseSchema):
    """Preventive maintenance schedule"""
    hostel_id: UUID
    hostel_name: str
    
    title: str
    description: Optional[str]
    category: MaintenanceCategory
    
    recurrence: MaintenanceRecurrence
    next_due_date: date
    
    assigned_to: Optional[UUID]
    assigned_to_name: Optional[str]
    
    estimated_cost: Optional[Decimal]
    
    is_active: bool
    last_completed_date: Optional[date]


class ScheduleCreate(BaseCreateSchema):
    """Create preventive maintenance schedule"""
    hostel_id: UUID
    
    title: str = Field(..., min_length=5, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    
    category: MaintenanceCategory
    recurrence: MaintenanceRecurrence
    
    # First occurrence
    start_date: date = Field(..., description="First scheduled date")
    
    # Assignment
    assigned_to: Optional[UUID] = None
    
    # Cost
    estimated_cost: Optional[Decimal] = Field(None, ge=0)
    
    # Checklist
    checklist: List["ScheduleChecklistItem"] = Field(default_factory=list)


class ScheduleChecklistItem(BaseSchema):
    """Checklist item for scheduled maintenance"""
    item_description: str = Field(..., min_length=5, max_length=500)
    is_required: bool = Field(True)
    item_order: int = Field(..., ge=1)


class RecurrenceConfig(BaseSchema):
    """Recurrence configuration details"""
    recurrence_type: MaintenanceRecurrence
    
    # Interval (for custom recurrence)
    interval_days: Optional[int] = Field(None, ge=1, description="Interval for custom recurrence")
    
    # Day of week (for weekly)
    day_of_week: Optional[int] = Field(None, ge=0, le=6, description="0=Monday, 6=Sunday")
    
    # Day of month (for monthly)
    day_of_month: Optional[int] = Field(None, ge=1, le=31)
    
    # End condition
    end_date: Optional[date] = Field(None, description="When to stop recurring")
    max_occurrences: Optional[int] = Field(None, ge=1, description="Max number of occurrences")


class ScheduleExecution(BaseCreateSchema):
    """Execute scheduled maintenance"""
    schedule_id: UUID
    execution_date: date
    
    # Was it completed?
    completed: bool
    
    # If completed
    completion_notes: Optional[str] = None
    actual_cost: Optional[Decimal] = Field(None, ge=0)
    
    # Checklist results
    checklist_results: List["ChecklistResult"] = Field(default_factory=list)
    
    # Next occurrence
    skip_next_occurrence: bool = Field(False)
    reschedule_next_to: Optional[date] = None


class ChecklistResult(BaseSchema):
    """Checklist item result"""
    item_description: str
    completed: bool
    notes: Optional[str] = None


class ScheduleUpdate(BaseUpdateSchema):
    """Update schedule"""
    title: Optional[str] = Field(None, min_length=5, max_length=255)
    description: Optional[str] = None
    recurrence: Optional[MaintenanceRecurrence] = None
    next_due_date: Optional[date] = None
    assigned_to: Optional[UUID] = None
    estimated_cost: Optional[Decimal] = None
    is_active: Optional[bool] = None


class ScheduleHistory(BaseSchema):
    """Schedule execution history"""
    schedule_id: UUID
    title: str
    
    total_executions: int
    completed_executions: int
    skipped_executions: int
    
    executions: List["ExecutionHistoryItem"]


class ExecutionHistoryItem(BaseSchema):
    """Individual execution history"""
    execution_date: date
    completed: bool
    actual_cost: Optional[Decimal]
    completion_notes: Optional[str]
    completed_by: Optional[UUID]
    completed_by_name: Optional[str]