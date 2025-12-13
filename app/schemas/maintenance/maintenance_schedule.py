# --- File: app/schemas/maintenance/maintenance_schedule.py ---
"""
Preventive maintenance schedule schemas.

Provides schemas for scheduled preventive maintenance with recurrence,
execution tracking, and checklist management.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import Field, field_validator, model_validator,computed_field
from uuid import UUID

from app.schemas.common.base import (
    BaseCreateSchema,
    BaseResponseSchema,
    BaseSchema,
    BaseUpdateSchema,
)
from app.schemas.common.enums import MaintenanceCategory, MaintenanceRecurrence

__all__ = [
    "PreventiveSchedule",
    "ScheduleCreate",
    "ScheduleChecklistItem",
    "RecurrenceConfig",
    "ScheduleExecution",
    "ChecklistResult",
    "ScheduleUpdate",
    "ScheduleHistory",
    "ExecutionHistoryItem",
]


class ScheduleChecklistItem(BaseSchema):
    """
    Checklist item for scheduled maintenance task.
    
    Defines specific checks to be performed during maintenance.
    """

    item_id: Optional[str] = Field(
        None,
        max_length=50,
        description="Unique item identifier",
    )
    item_description: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Description of check/task to perform",
    )
    category: Optional[str] = Field(
        None,
        max_length=100,
        description="Item category",
    )
    is_required: bool = Field(
        True,
        description="Whether this item is mandatory",
    )
    is_critical: bool = Field(
        default=False,
        description="Whether this is a critical safety check",
    )
    item_order: int = Field(
        ...,
        ge=1,
        le=1000,
        description="Display order in checklist",
    )
    estimated_time_minutes: Optional[int] = Field(
        None,
        ge=0,
        le=1440,
        description="Estimated time for this item in minutes",
    )
    instructions: Optional[str] = Field(
        None,
        max_length=1000,
        description="Detailed instructions for this check",
    )

    @field_validator("item_description", "instructions")
    @classmethod
    def normalize_text(cls, v: Optional[str]) -> Optional[str]:
        """Normalize text fields."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return None


class PreventiveSchedule(BaseResponseSchema):
    """
    Preventive maintenance schedule.
    
    Defines recurring maintenance tasks with scheduling
    and assignment information.
    """

    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    hostel_name: str = Field(
        ...,
        description="Hostel name",
    )
    schedule_code: Optional[str] = Field(
        None,
        max_length=50,
        description="Schedule code/reference",
    )
    title: str = Field(
        ...,
        description="Schedule title",
    )
    description: Optional[str] = Field(
        None,
        description="Schedule description",
    )
    category: MaintenanceCategory = Field(
        ...,
        description="Maintenance category",
    )
    recurrence: MaintenanceRecurrence = Field(
        ...,
        description="Recurrence pattern",
    )
    next_due_date: date = Field(
        ...,
        description="Next scheduled execution date",
    )
    last_execution_date: Optional[date] = Field(
        None,
        description="Last execution date",
    )
    assigned_to: Optional[UUID] = Field(
        None,
        description="Default assignee user ID",
    )
    assigned_to_name: Optional[str] = Field(
        None,
        description="Default assignee name",
    )
    estimated_cost: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Estimated cost per execution",
    )
    estimated_duration_hours: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Estimated duration in hours",
    )
    is_active: bool = Field(
        True,
        description="Whether schedule is active",
    )
    total_executions: int = Field(
        default=0,
        ge=0,
        description="Total times executed",
    )
    last_completed_date: Optional[date] = Field(
        None,
        description="Last successful completion date",
    )
    priority_level: Optional[str] = Field(
        None,
        pattern=r"^(low|medium|high)$",
        description="Default priority level",
    )

    @computed_field
    @property
    def is_overdue(self) -> bool:
        """Check if schedule is overdue."""
        return self.next_due_date < date.today()

    @computed_field
    @property
    def days_until_due(self) -> int:
        """Calculate days until next due date."""
        return (self.next_due_date - date.today()).days


class ScheduleCreate(BaseCreateSchema):
    """
    Create preventive maintenance schedule.
    
    Defines new recurring maintenance with checklist and recurrence rules.
    """

    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    schedule_code: Optional[str] = Field(
        None,
        max_length=50,
        description="Schedule code/reference",
    )
    title: str = Field(
        ...,
        min_length=5,
        max_length=255,
        description="Schedule title",
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Detailed description",
    )
    category: MaintenanceCategory = Field(
        ...,
        description="Maintenance category",
    )
    recurrence: MaintenanceRecurrence = Field(
        ...,
        description="Recurrence pattern",
    )
    start_date: date = Field(
        ...,
        description="First scheduled date",
    )
    end_date: Optional[date] = Field(
        None,
        description="Last scheduled date (optional)",
    )
    assigned_to: Optional[UUID] = Field(
        None,
        description="Default assignee",
    )
    estimated_cost: Optional[Decimal] = Field(
        None,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Estimated cost per execution",
    )
    estimated_duration_hours: Optional[Decimal] = Field(
        None,
        ge=0,
        le=1000,
        decimal_places=2,
        description="Estimated duration in hours",
    )
    checklist: List[ScheduleChecklistItem] = Field(
        default_factory=list,
        max_length=100,
        description="Maintenance checklist items",
    )
    auto_create_requests: bool = Field(
        default=True,
        description="Auto-create maintenance requests on due date",
    )
    notification_days_before: int = Field(
        default=3,
        ge=0,
        le=30,
        description="Days before due date to send notification",
    )
    priority_level: Optional[str] = Field(
        None,
        pattern=r"^(low|medium|high)$",
        description="Default priority level",
    )

    @field_validator("start_date")
    @classmethod
    def validate_start_date(cls, v: date) -> date:
        """Validate start date is reasonable."""
        # Can't be too far in past
        days_past = (date.today() - v).days
        if days_past > 365:
            raise ValueError(
                "Start date cannot be more than 1 year in the past"
            )
        
        return v

    @field_validator("title", "description")
    @classmethod
    def normalize_text(cls, v: Optional[str]) -> Optional[str]:
        """Normalize text fields."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return None

    @field_validator("estimated_cost", "estimated_duration_hours")
    @classmethod
    def round_decimals(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Round decimal values."""
        return round(v, 2) if v is not None else None

    @model_validator(mode="after")
    def validate_date_range(self) -> "ScheduleCreate":
        """
        Validate schedule date range.
        
        End date should be after start date if provided.
        """
        if self.end_date:
            if self.end_date <= self.start_date:
                raise ValueError("End date must be after start date")
            
            # Reasonable maximum duration
            duration_years = (self.end_date - self.start_date).days / 365
            if duration_years > 10:
                raise ValueError(
                    "Schedule duration cannot exceed 10 years"
                )
        
        return self

    @model_validator(mode="after")
    def validate_checklist_order(self) -> "ScheduleCreate":
        """
        Validate checklist item ordering.
        
        Ensures no duplicate order numbers.
        """
        if self.checklist:
            orders = [item.item_order for item in self.checklist]
            if len(orders) != len(set(orders)):
                raise ValueError(
                    "Checklist items must have unique order numbers"
                )
        
        return self


class RecurrenceConfig(BaseSchema):
    """
    Advanced recurrence configuration.
    
    Defines detailed recurrence rules for complex scheduling patterns.
    """

    recurrence_type: MaintenanceRecurrence = Field(
        ...,
        description="Recurrence type",
    )
    interval_days: Optional[int] = Field(
        None,
        ge=1,
        le=365,
        description="Interval for custom recurrence (in days)",
    )
    day_of_week: Optional[int] = Field(
        None,
        ge=0,
        le=6,
        description="Day of week (0=Monday, 6=Sunday) for weekly recurrence",
    )
    day_of_month: Optional[int] = Field(
        None,
        ge=1,
        le=31,
        description="Day of month for monthly recurrence",
    )
    month_of_year: Optional[int] = Field(
        None,
        ge=1,
        le=12,
        description="Month for yearly recurrence",
    )
    end_date: Optional[date] = Field(
        None,
        description="Stop recurring after this date",
    )
    max_occurrences: Optional[int] = Field(
        None,
        ge=1,
        le=1000,
        description="Maximum number of occurrences",
    )
    skip_weekends: bool = Field(
        default=False,
        description="Skip weekends when scheduling",
    )
    skip_holidays: bool = Field(
        default=False,
        description="Skip holidays when scheduling",
    )

    @model_validator(mode="after")
    def validate_recurrence_rules(self) -> "RecurrenceConfig":
        """
        Validate recurrence configuration consistency.
        
        Ensures appropriate fields are set for recurrence type.
        """
        # Weekly should have day_of_week
        if self.recurrence_type == MaintenanceRecurrence.WEEKLY:
            if self.day_of_week is None:
                raise ValueError(
                    "day_of_week is required for weekly recurrence"
                )
        
        # Monthly should have day_of_month
        if self.recurrence_type == MaintenanceRecurrence.MONTHLY:
            if self.day_of_month is None:
                raise ValueError(
                    "day_of_month is required for monthly recurrence"
                )
        
        # Yearly should have month
        if self.recurrence_type == MaintenanceRecurrence.YEARLY:
            if self.month_of_year is None:
                raise ValueError(
                    "month_of_year is required for yearly recurrence"
                )
        
        # End condition validation
        if self.end_date and self.max_occurrences:
            # Both provided is okay, will use whichever comes first
            pass
        
        return self


class ChecklistResult(BaseSchema):
    """
    Result of individual checklist item execution.
    
    Records completion status and findings for checklist item.
    """

    item_id: Optional[str] = Field(
        None,
        description="Checklist item ID",
    )
    item_description: str = Field(
        ...,
        description="Item description",
    )
    completed: bool = Field(
        ...,
        description="Whether item was completed",
    )
    status: str = Field(
        ...,
        pattern=r"^(pass|fail|na|skipped)$",
        description="Item completion status",
    )
    notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Notes or observations",
    )
    issues_found: Optional[str] = Field(
        None,
        max_length=500,
        description="Issues found during check",
    )
    action_taken: Optional[str] = Field(
        None,
        max_length=500,
        description="Action taken to resolve issues",
    )
    time_taken_minutes: Optional[int] = Field(
        None,
        ge=0,
        le=1440,
        description="Time taken for this item",
    )

    @field_validator("notes", "issues_found", "action_taken")
    @classmethod
    def normalize_text(cls, v: Optional[str]) -> Optional[str]:
        """Normalize text fields."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return None


class ScheduleExecution(BaseCreateSchema):
    """
    Execute scheduled preventive maintenance.
    
    Records execution of scheduled maintenance with results
    and next occurrence scheduling.
    """

    schedule_id: UUID = Field(
        ...,
        description="Schedule unique identifier",
    )
    execution_date: date = Field(
        ...,
        description="Execution date",
    )
    executed_by: UUID = Field(
        ...,
        description="User who executed the maintenance",
    )
    completed: bool = Field(
        ...,
        description="Whether execution was completed successfully",
    )
    completion_notes: Optional[str] = Field(
        None,
        max_length=2000,
        description="Detailed completion notes",
    )
    actual_cost: Optional[Decimal] = Field(
        None,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Actual cost incurred",
    )
    actual_duration_hours: Optional[Decimal] = Field(
        None,
        ge=0,
        le=1000,
        decimal_places=2,
        description="Actual time taken in hours",
    )
    checklist_results: List[ChecklistResult] = Field(
        default_factory=list,
        max_length=100,
        description="Results for each checklist item",
    )
    materials_used: Optional[List[dict]] = Field(
        None,
        max_length=100,
        description="Materials used in execution",
    )
    issues_found: Optional[str] = Field(
        None,
        max_length=1000,
        description="Issues or concerns identified",
    )
    recommendations: Optional[str] = Field(
        None,
        max_length=1000,
        description="Recommendations for future maintenance",
    )
    skip_next_occurrence: bool = Field(
        False,
        description="Skip the next scheduled occurrence",
    )
    reschedule_next_to: Optional[date] = Field(
        None,
        description="Reschedule next occurrence to specific date",
    )
    execution_photos: Optional[List[str]] = Field(
        None,
        max_length=20,
        description="Execution photographs",
    )

    @field_validator("execution_date")
    @classmethod
    def validate_execution_date(cls, v: date) -> date:
        """Validate execution date is not in future."""
        if v > date.today():
            raise ValueError("Execution date cannot be in the future")
        return v

    @field_validator("actual_cost", "actual_duration_hours")
    @classmethod
    def round_decimals(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Round decimal values."""
        return round(v, 2) if v is not None else None

    @field_validator(
        "completion_notes",
        "issues_found",
        "recommendations",
    )
    @classmethod
    def normalize_text(cls, v: Optional[str]) -> Optional[str]:
        """Normalize text fields."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return None

    @model_validator(mode="after")
    def validate_completion_requirements(self) -> "ScheduleExecution":
        """
        Validate completion information.
        
        Completed executions should have notes.
        """
        if self.completed and not self.completion_notes:
            raise ValueError(
                "Completion notes are required for completed executions"
            )
        
        return self

    @model_validator(mode="after")
    def validate_rescheduling(self) -> "ScheduleExecution":
        """
        Validate rescheduling logic.
        
        Can't both skip and reschedule next occurrence.
        """
        if self.skip_next_occurrence and self.reschedule_next_to:
            raise ValueError(
                "Cannot both skip and reschedule next occurrence"
            )
        
        if self.reschedule_next_to:
            # Rescheduled date should be in future
            if self.reschedule_next_to <= date.today():
                raise ValueError(
                    "Rescheduled date must be in the future"
                )
        
        return self


class ScheduleUpdate(BaseUpdateSchema):
    """
    Update preventive maintenance schedule.
    
    Allows modification of schedule parameters and status.
    """

    title: Optional[str] = Field(
        None,
        min_length=5,
        max_length=255,
        description="Updated title",
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Updated description",
    )
    recurrence: Optional[MaintenanceRecurrence] = Field(
        None,
        description="Updated recurrence pattern",
    )
    next_due_date: Optional[date] = Field(
        None,
        description="Updated next due date",
    )
    assigned_to: Optional[UUID] = Field(
        None,
        description="Updated default assignee",
    )
    estimated_cost: Optional[Decimal] = Field(
        None,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Updated estimated cost",
    )
    estimated_duration_hours: Optional[Decimal] = Field(
        None,
        ge=0,
        le=1000,
        decimal_places=2,
        description="Updated estimated duration",
    )
    is_active: Optional[bool] = Field(
        None,
        description="Active status",
    )
    auto_create_requests: Optional[bool] = Field(
        None,
        description="Auto-create maintenance requests",
    )
    notification_days_before: Optional[int] = Field(
        None,
        ge=0,
        le=30,
        description="Notification days before due date",
    )
    priority_level: Optional[str] = Field(
        None,
        pattern=r"^(low|medium|high)$",
        description="Updated priority level",
    )

    @field_validator("title", "description")
    @classmethod
    def normalize_text(cls, v: Optional[str]) -> Optional[str]:
        """Normalize text fields."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return None

    @field_validator("estimated_cost", "estimated_duration_hours")
    @classmethod
    def round_decimals(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Round decimal values."""
        return round(v, 2) if v is not None else None

    @field_validator("next_due_date")
    @classmethod
    def validate_due_date(cls, v: Optional[date]) -> Optional[date]:
        """Validate next due date is reasonable."""
        if v is not None:
            # Should not be too far in past
            days_past = (date.today() - v).days
            if days_past > 30:
                raise ValueError(
                    "Next due date cannot be more than 30 days in the past"
                )
        return v


class ExecutionHistoryItem(BaseSchema):
    """
    Individual execution history record.
    
    Represents single execution in schedule history.
    """

    execution_id: UUID = Field(
        ...,
        description="Execution unique identifier",
    )
    execution_date: date = Field(
        ...,
        description="Execution date",
    )
    scheduled_date: date = Field(
        ...,
        description="Originally scheduled date",
    )
    executed_by: UUID = Field(
        ...,
        description="User who executed",
    )
    executed_by_name: str = Field(
        ...,
        description="Executor name",
    )
    completed: bool = Field(
        ...,
        description="Whether completed successfully",
    )
    completed_at: Optional[datetime] = Field(
        None,
        description="Completion timestamp",
    )
    actual_cost: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Actual cost",
    )
    actual_duration_hours: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Actual duration",
    )
    completion_notes: Optional[str] = Field(
        None,
        description="Completion notes",
    )
    issues_found: Optional[str] = Field(
        None,
        description="Issues found",
    )
    was_on_time: bool = Field(
        ...,
        description="Whether executed on scheduled date",
    )
    days_delay: int = Field(
        default=0,
        description="Days delayed from scheduled date",
    )
    quality_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Quality rating for execution",
    )

    @computed_field
    @property
    def execution_status(self) -> str:
        """Get execution status summary."""
        if not self.completed:
            return "incomplete"
        elif self.was_on_time:
            return "on_time"
        else:
            return "delayed"


class ScheduleHistory(BaseSchema):
    """
    Complete execution history for schedule.
    
    Tracks all executions with statistics and trends.
    """

    schedule_id: UUID = Field(
        ...,
        description="Schedule unique identifier",
    )
    schedule_title: str = Field(
        ...,
        description="Schedule title",
    )
    schedule_code: Optional[str] = Field(
        None,
        description="Schedule code",
    )
    total_executions: int = Field(
        ...,
        ge=0,
        description="Total number of executions",
    )
    completed_executions: int = Field(
        ...,
        ge=0,
        description="Successfully completed executions",
    )
    skipped_executions: int = Field(
        ...,
        ge=0,
        description="Skipped executions",
    )
    delayed_executions: int = Field(
        default=0,
        ge=0,
        description="Delayed executions",
    )
    on_time_executions: int = Field(
        default=0,
        ge=0,
        description="On-time executions",
    )
    executions: List[ExecutionHistoryItem] = Field(
        ...,
        description="Chronological execution history",
    )
    total_cost: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        description="Total cost across all executions",
    )
    average_cost: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        description="Average cost per execution",
    )
    average_duration_hours: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Average execution duration",
    )
    average_quality_rating: Optional[Decimal] = Field(
        None,
        ge=0,
        le=5,
        description="Average quality rating",
    )

    @computed_field
    @property
    def completion_rate(self) -> Decimal:
        """Calculate completion rate percentage."""
        if self.total_executions == 0:
            return Decimal("0.00")
        return round(
            Decimal(self.completed_executions) / Decimal(self.total_executions) * 100,
            2,
        )

    @computed_field
    @property
    def on_time_rate(self) -> Decimal:
        """Calculate on-time execution rate."""
        if self.completed_executions == 0:
            return Decimal("0.00")
        return round(
            Decimal(self.on_time_executions) / Decimal(self.completed_executions) * 100,
            2,
        )