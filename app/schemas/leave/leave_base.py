# --- File: app/schemas/leave/leave_base.py ---
"""
Base leave schemas with comprehensive validation and type safety.

This module provides foundational schemas for leave management including
applications, updates, and core validation logic.
"""

from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import Field, HttpUrl, field_validator, model_validator
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema, BaseUpdateSchema
from app.schemas.common.enums import LeaveStatus, LeaveType

__all__ = [
    "LeaveBase",
    "LeaveCreate",
    "LeaveUpdate",
]


class LeaveBase(BaseSchema):
    """
    Base leave application schema with core fields.
    
    Provides common leave attributes and validation logic used across
    create/update operations.
    """

    student_id: UUID = Field(
        ...,
        description="Student unique identifier requesting leave",
    )
    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    leave_type: LeaveType = Field(
        ...,
        description="Type of leave being requested",
    )
    from_date: date = Field(
        ...,
        description="Leave start date (inclusive)",
    )
    to_date: date = Field(
        ...,
        description="Leave end date (inclusive)",
    )
    total_days: int = Field(
        ...,
        ge=1,
        le=365,
        description="Total number of leave days (auto-calculated)",
    )
    reason: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Detailed reason for leave request",
    )
    contact_during_leave: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{9,14}$",
        description="Contact phone number during leave period",
    )
    emergency_contact: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{9,14}$",
        description="Emergency contact phone number",
    )
    supporting_document_url: Optional[HttpUrl] = Field(
        None,
        description="URL to supporting document (e.g., medical certificate)",
    )

    @field_validator("from_date")
    @classmethod
    def validate_from_date(cls, v: date) -> date:
        """
        Validate leave start date constraints.
        
        Ensures:
        - Start date is not too far in the past (max 30 days)
        - Start date is within reasonable future range (max 1 year)
        """
        today = date.today()
        
        # Don't allow leaves starting more than 30 days in the past
        days_past = (today - v).days
        if days_past > 30:
            raise ValueError(
                "Leave start date cannot be more than 30 days in the past"
            )
        
        # Don't allow leaves starting more than 1 year in the future
        days_future = (v - today).days
        if days_future > 365:
            raise ValueError(
                "Leave start date cannot be more than 1 year in the future"
            )
        
        return v

    @field_validator("reason")
    @classmethod
    def validate_reason(cls, v: str) -> str:
        """
        Validate and normalize leave reason.
        
        Ensures reason is meaningful and properly formatted.
        """
        v = v.strip()
        
        if len(v) < 10:
            raise ValueError("Leave reason must be at least 10 characters")
        
        # Check if reason is not just repeated characters or meaningless text
        if len(set(v.lower().replace(" ", ""))) < 5:
            raise ValueError("Leave reason must be meaningful and descriptive")
        
        return v

    @field_validator("contact_during_leave", "emergency_contact")
    @classmethod
    def normalize_phone(cls, v: Optional[str]) -> Optional[str]:
        """Normalize phone numbers by removing spaces and dashes."""
        if v is not None:
            return v.replace(" ", "").replace("-", "").strip()
        return None

    @model_validator(mode="after")
    def validate_leave_dates(self) -> "LeaveBase":
        """
        Validate leave date consistency and calculate total days.
        
        Ensures:
        - End date is after or equal to start date
        - Total days matches actual duration
        - Leave duration is reasonable (not too long)
        """
        # Validate end date is after start date
        if self.to_date < self.from_date:
            raise ValueError("Leave end date must be after or equal to start date")
        
        # Calculate expected total days
        expected_days = (self.to_date - self.from_date).days + 1
        
        # Validate total_days matches calculation
        if self.total_days != expected_days:
            raise ValueError(
                f"total_days ({self.total_days}) must equal calculated duration "
                f"({expected_days} days)"
            )
        
        # Validate reasonable leave duration based on leave type
        max_days_by_type = {
            LeaveType.CASUAL: 30,
            LeaveType.SICK: 60,
            LeaveType.EMERGENCY: 15,
            LeaveType.VACATION: 90,
            LeaveType.OTHER: 30,
        }
        
        max_allowed = max_days_by_type.get(self.leave_type, 30)
        if self.total_days > max_allowed:
            raise ValueError(
                f"{self.leave_type.value} leave cannot exceed {max_allowed} days"
            )
        
        return self

    @model_validator(mode="after")
    def validate_document_requirement(self) -> "LeaveBase":
        """
        Validate supporting document requirements.
        
        Certain leave types or durations require supporting documents.
        """
        # Sick leave > 3 days requires medical certificate
        if self.leave_type == LeaveType.SICK and self.total_days > 3:
            if not self.supporting_document_url:
                raise ValueError(
                    "Medical certificate required for sick leave exceeding 3 days"
                )
        
        # Any leave > 15 days requires documentation
        if self.total_days > 15:
            if not self.supporting_document_url:
                raise ValueError(
                    "Supporting documentation required for leave exceeding 15 days"
                )
        
        return self


class LeaveCreate(LeaveBase, BaseCreateSchema):
    """
    Create leave application request.
    
    Inherits all validation from LeaveBase and adds creation context.
    """

    # Override total_days to make it optional (will be auto-calculated)
    total_days: Optional[int] = Field(
        None,
        ge=1,
        le=365,
        description="Total leave days (auto-calculated if not provided)",
    )

    @model_validator(mode="after")
    def calculate_total_days(self) -> "LeaveCreate":
        """
        Auto-calculate total_days if not provided.
        
        Calculates duration from from_date and to_date.
        """
        if self.total_days is None:
            self.total_days = (self.to_date - self.from_date).days + 1
        return self


class LeaveUpdate(BaseUpdateSchema):
    """
    Update leave application with partial fields.
    
    All fields are optional for flexible updates. Typically used
    before leave approval to modify application details.
    """

    leave_type: Optional[LeaveType] = Field(
        None,
        description="Updated leave type",
    )
    from_date: Optional[date] = Field(
        None,
        description="Updated start date",
    )
    to_date: Optional[date] = Field(
        None,
        description="Updated end date",
    )
    total_days: Optional[int] = Field(
        None,
        ge=1,
        le=365,
        description="Updated total days",
    )
    reason: Optional[str] = Field(
        None,
        min_length=10,
        max_length=1000,
        description="Updated leave reason",
    )
    contact_during_leave: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{9,14}$",
        description="Updated contact number",
    )
    emergency_contact: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{9,14}$",
        description="Updated emergency contact",
    )
    supporting_document_url: Optional[HttpUrl] = Field(
        None,
        description="Updated supporting document URL",
    )
    status: Optional[LeaveStatus] = Field(
        None,
        description="Updated leave status (restricted to certain roles)",
    )

    @field_validator("reason")
    @classmethod
    def validate_reason(cls, v: Optional[str]) -> Optional[str]:
        """Validate updated reason if provided."""
        if v is not None:
            v = v.strip()
            if len(v) < 10:
                raise ValueError("Leave reason must be at least 10 characters")
            if len(set(v.lower().replace(" ", ""))) < 5:
                raise ValueError("Leave reason must be meaningful")
            return v
        return None

    @field_validator("contact_during_leave", "emergency_contact")
    @classmethod
    def normalize_phone(cls, v: Optional[str]) -> Optional[str]:
        """Normalize phone numbers."""
        if v is not None:
            return v.replace(" ", "").replace("-", "").strip()
        return None

    @model_validator(mode="after")
    def validate_date_consistency(self) -> "LeaveUpdate":
        """
        Validate date consistency when both dates are updated.
        
        Ensures end date is after start date when both are provided.
        """
        # Only validate if both dates are being updated
        if self.from_date is not None and self.to_date is not None:
            if self.to_date < self.from_date:
                raise ValueError("End date must be after or equal to start date")
            
            # Recalculate total_days if dates changed but total_days not provided
            if self.total_days is None:
                self.total_days = (self.to_date - self.from_date).days + 1
        
        return self