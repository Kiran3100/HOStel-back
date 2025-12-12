# --- File: app/schemas/payment/payment_reminder.py ---
"""
Payment reminder schemas.

This module defines schemas for payment reminder configuration,
logging, manual sending, and statistics.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import Field, field_validator, model_validator, computed_field

from app.schemas.common.base import (
    BaseCreateSchema,
    BaseResponseSchema,
    BaseSchema,
)

__all__ = [
    "ReminderConfig",
    "ReminderLog",
    "SendReminderRequest",
    "ReminderBatch",
    "ReminderStats",
]


class ReminderConfig(BaseSchema):
    """
    Payment reminder configuration for a hostel.
    
    Defines when and how payment reminders should be sent.
    """

    hostel_id: UUID = Field(
        ...,
        description="Hostel ID",
    )

    # Reminder Timing
    days_before_due: List[int] = Field(
        default_factory=lambda: [7, 3, 1],
        min_length=1,
        max_length=10,
        description="Days before due date to send reminders",
    )
    days_after_due: List[int] = Field(
        default_factory=lambda: [1, 3, 7, 15],
        min_length=1,
        max_length=10,
        description="Days after due date for overdue reminders",
    )

    # Communication Channels
    send_email: bool = Field(
        True,
        description="Send email reminders",
    )
    send_sms: bool = Field(
        True,
        description="Send SMS reminders",
    )
    send_push: bool = Field(
        True,
        description="Send push notifications",
    )

    # Escalation
    escalate_after_days: int = Field(
        15,
        ge=1,
        le=90,
        description="Escalate to admin after this many days overdue",
    )

    # Templates
    email_template_id: Optional[UUID] = Field(
        None,
        description="Custom email template ID",
    )
    sms_template_id: Optional[UUID] = Field(
        None,
        description="Custom SMS template ID",
    )

    # Status
    is_active: bool = Field(
        True,
        description="Whether reminder system is active",
    )

    @field_validator("days_before_due", "days_after_due")
    @classmethod
    def validate_days_list(cls, v: List[int]) -> List[int]:
        """Validate days lists."""
        if not v:
            raise ValueError("At least one reminder day must be configured")
        
        # Ensure all values are positive
        if any(day < 0 for day in v):
            raise ValueError("Days must be non-negative")
        
        # Remove duplicates and sort
        return sorted(set(v))

    @model_validator(mode="after")
    def validate_channels(self) -> "ReminderConfig":
        """Ensure at least one channel is enabled."""
        if not any([self.send_email, self.send_sms, self.send_push]):
            raise ValueError(
                "At least one communication channel must be enabled"
            )
        return self


class ReminderLog(BaseResponseSchema):
    """
    Payment reminder log entry.
    
    Records details of a sent reminder.
    """

    payment_id: UUID = Field(
        ...,
        description="Payment ID",
    )
    payment_reference: str = Field(
        ...,
        description="Payment reference",
    )

    # Student Information
    student_id: UUID = Field(
        ...,
        description="Student ID",
    )
    student_name: str = Field(
        ...,
        description="Student name",
    )
    student_email: str = Field(
        ...,
        description="Student email",
    )
    student_phone: str = Field(
        ...,
        description="Student phone",
    )

    # Reminder Details
    reminder_type: str = Field(
        ...,
        pattern=r"^(due_soon|overdue|final_notice)$",
        description="Type of reminder",
    )
    reminder_channel: str = Field(
        ...,
        pattern=r"^(email|sms|push)$",
        description="Communication channel used",
    )

    # Delivery Status
    sent_at: datetime = Field(
        ...,
        description="When reminder was sent",
    )
    delivery_status: str = Field(
        ...,
        pattern=r"^(sent|delivered|failed|bounced)$",
        description="Delivery status",
    )

    # Content
    subject: Optional[str] = Field(
        None,
        description="Email subject (if email)",
    )
    message_preview: str = Field(
        ...,
        max_length=200,
        description="First 200 characters of message",
    )

    # Engagement Tracking
    opened: bool = Field(
        False,
        description="Whether email was opened",
    )
    clicked: bool = Field(
        False,
        description="Whether any link was clicked",
    )

    # Error Details (if failed)
    error_message: Optional[str] = Field(
        None,
        description="Error message if delivery failed",
    )

    @computed_field
    @property
    def was_successful(self) -> bool:
        """Check if reminder was successfully delivered."""
        return self.delivery_status in ["sent", "delivered"]


class SendReminderRequest(BaseCreateSchema):
    """
    Request to send payment reminder manually.
    
    Allows manual triggering of reminders for specific payments,
    students, or entire hostel.
    """

    # Target Selection (one of these must be provided)
    payment_id: Optional[UUID] = Field(
        None,
        description="Send reminder for specific payment",
    )
    student_id: Optional[UUID] = Field(
        None,
        description="Send reminders for all due payments of student",
    )
    hostel_id: Optional[UUID] = Field(
        None,
        description="Send reminders for all due payments in hostel",
    )

    # Reminder Settings
    reminder_type: str = Field(
        "overdue",
        pattern=r"^(due_soon|overdue|final_notice)$",
        description="Type of reminder to send",
    )

    # Channel Selection
    channels: List[str] = Field(
        default_factory=lambda: ["email", "sms"],
        description="Channels to use for reminder",
    )

    # Custom Message
    custom_message: Optional[str] = Field(
        None,
        max_length=500,
        description="Custom message to append to reminder",
    )

    @model_validator(mode="after")
    def validate_target_selection(self) -> "SendReminderRequest":
        """Ensure exactly one target is selected."""
        targets = [self.payment_id, self.student_id, self.hostel_id]
        selected = sum(1 for t in targets if t is not None)
        
        if selected == 0:
            raise ValueError(
                "One of payment_id, student_id, or hostel_id must be provided"
            )
        
        if selected > 1:
            raise ValueError(
                "Only one of payment_id, student_id, or hostel_id can be provided"
            )
        
        return self

    @field_validator("channels")
    @classmethod
    def validate_channels(cls, v: List[str]) -> List[str]:
        """Validate channels list."""
        if not v:
            raise ValueError("At least one channel must be specified")
        
        valid_channels = ["email", "sms", "push"]
        invalid = [ch for ch in v if ch not in valid_channels]
        if invalid:
            raise ValueError(
                f"Invalid channels: {', '.join(invalid)}. "
                f"Valid: {', '.join(valid_channels)}"
            )
        
        # Remove duplicates
        return list(dict.fromkeys(v))


class ReminderBatch(BaseSchema):
    """
    Batch reminder sending result.
    
    Contains information about a bulk reminder operation.
    """

    batch_id: UUID = Field(
        ...,
        description="Unique batch identifier",
    )

    # Processing Stats
    total_payments: int = Field(
        ...,
        ge=0,
        description="Total payments processed",
    )
    reminders_sent: int = Field(
        ...,
        ge=0,
        description="Number of reminders successfully sent",
    )
    reminders_failed: int = Field(
        ...,
        ge=0,
        description="Number of failed reminders",
    )

    # Breakdown by Channel
    email_sent: int = Field(
        ...,
        ge=0,
        description="Emails sent",
    )
    sms_sent: int = Field(
        ...,
        ge=0,
        description="SMS sent",
    )
    push_sent: int = Field(
        ...,
        ge=0,
        description="Push notifications sent",
    )

    # Timing
    started_at: datetime = Field(
        ...,
        description="When batch processing started",
    )
    completed_at: Optional[datetime] = Field(
        None,
        description="When batch processing completed",
    )

    # Status
    status: str = Field(
        ...,
        pattern=r"^(processing|completed|failed)$",
        description="Batch processing status",
    )

    @computed_field
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        total = self.reminders_sent + self.reminders_failed
        if total == 0:
            return 0.0
        return round((self.reminders_sent / total) * 100, 2)

    @computed_field
    @property
    def total_channels_used(self) -> int:
        """Count total reminder sends across all channels."""
        return self.email_sent + self.sms_sent + self.push_sent


class ReminderStats(BaseSchema):
    """
    Payment reminder statistics.
    
    Provides analytics about reminder effectiveness.
    """

    hostel_id: UUID = Field(
        ...,
        description="Hostel ID",
    )
    period_start: date = Field(
        ...,
        description="Statistics period start",
    )
    period_end: date = Field(
        ...,
        description="Statistics period end",
    )

    # Volume
    total_reminders_sent: int = Field(
        ...,
        ge=0,
        description="Total reminders sent in period",
    )

    # By Type
    due_soon_reminders: int = Field(
        ...,
        ge=0,
        description="Due soon reminders",
    )
    overdue_reminders: int = Field(
        ...,
        ge=0,
        description="Overdue reminders",
    )
    final_notices: int = Field(
        ...,
        ge=0,
        description="Final notices",
    )

    # By Channel
    email_reminders: int = Field(
        ...,
        ge=0,
        description="Email reminders",
    )
    sms_reminders: int = Field(
        ...,
        ge=0,
        description="SMS reminders",
    )
    push_reminders: int = Field(
        ...,
        ge=0,
        description="Push notifications",
    )

    # Effectiveness
    payment_rate_after_reminder: Decimal = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of reminded students who paid",
    )
    average_days_to_payment: Decimal = Field(
        ...,
        ge=0,
        description="Average days from reminder to payment",
    )

    @computed_field
    @property
    def most_effective_channel(self) -> str:
        """Determine most used channel."""
        channels = {
            "email": self.email_reminders,
            "sms": self.sms_reminders,
            "push": self.push_reminders,
        }
        return max(channels, key=channels.get)