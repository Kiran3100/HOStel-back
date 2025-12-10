"""
Payment reminder schemas
"""
from datetime import datetime, date
from typing import Optional, List
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class ReminderConfig(BaseSchema):
    """Payment reminder configuration"""
    hostel_id: UUID
    
    # Reminder timing
    days_before_due: List[int] = Field(
        default_factory=lambda: [7, 3, 1],
        description="Days before due date to send reminders"
    )
    days_after_due: List[int] = Field(
        default_factory=lambda: [1, 3, 7, 15],
        description="Days after due date for overdue reminders"
    )
    
    # Channels
    send_email: bool = Field(True)
    send_sms: bool = Field(True)
    send_push: bool = Field(True)
    
    # Escalation
    escalate_after_days: int = Field(15, description="Escalate to admin after days")
    
    # Template
    email_template_id: Optional[UUID] = None
    sms_template_id: Optional[UUID] = None
    
    is_active: bool = Field(True)


class ReminderLog(BaseResponseSchema):
    """Payment reminder log entry"""
    payment_id: UUID
    payment_reference: str
    
    student_id: UUID
    student_name: str
    student_email: str
    student_phone: str
    
    # Reminder details
    reminder_type: str = Field(..., pattern="^(due_soon|overdue|final_notice)$")
    reminder_channel: str = Field(..., pattern="^(email|sms|push)$")
    
    # Status
    sent_at: datetime
    delivery_status: str = Field(..., pattern="^(sent|delivered|failed|bounced)$")
    
    # Content
    subject: Optional[str] = None
    message_preview: str
    
    # Response
    opened: bool = Field(False, description="Email opened")
    clicked: bool = Field(False, description="Link clicked")


class SendReminderRequest(BaseCreateSchema):
    """Send payment reminder manually"""
    payment_id: Optional[UUID] = Field(None, description="Specific payment")
    student_id: Optional[UUID] = Field(None, description="All due payments for student")
    hostel_id: Optional[UUID] = Field(None, description="All due payments for hostel")
    
    # Reminder settings
    reminder_type: str = Field("overdue", pattern="^(due_soon|overdue|final_notice)$")
    
    channels: List[str] = Field(
        default_factory=lambda: ["email", "sms"],
        description="Channels to use"
    )
    
    # Custom message
    custom_message: Optional[str] = Field(None, max_length=500)


class ReminderBatch(BaseSchema):
    """Batch reminder sending"""
    batch_id: UUID
    
    total_payments: int
    reminders_sent: int
    reminders_failed: int
    
    # Breakdown by channel
    email_sent: int
    sms_sent: int
    push_sent: int
    
    started_at: datetime
    completed_at: Optional[datetime]
    
    status: str = Field(..., pattern="^(processing|completed|failed)$")


class ReminderStats(BaseSchema):
    """Reminder statistics"""
    hostel_id: UUID
    period_start: date
    period_end: date
    
    total_reminders_sent: int
    
    # By type
    due_soon_reminders: int
    overdue_reminders: int
    final_notices: int
    
    # By channel
    email_reminders: int
    sms_reminders: int
    push_reminders: int
    
    # Effectiveness
    payment_rate_after_reminder: Decimal = Field(..., description="% who paid after reminder")
    average_days_to_payment: Decimal