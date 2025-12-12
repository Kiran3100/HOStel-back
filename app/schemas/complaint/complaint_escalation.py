"""
Complaint escalation schemas with business rule validation.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class EscalationRequest(BaseCreateSchema):
    """Escalate complaint with validation."""
    
    complaint_id: UUID = Field(..., description="Complaint ID")
    escalate_to: UUID = Field(..., description="User to escalate to (admin/supervisor)")
    
    escalation_reason: str = Field(
        ...,
        min_length=20,
        max_length=500,
        description="Reason for escalation"
    )
    
    # Priority increase
    increase_priority: bool = Field(True, description="Increase priority level")
    
    # Urgency
    is_urgent: bool = Field(False)

    @field_validator("escalation_reason")
    @classmethod
    def validate_escalation_reason(cls, v: str) -> str:
        """Ensure escalation reason is detailed."""
        v = v.strip()
        if len(v.split()) < 5:
            raise ValueError("Escalation reason must contain at least 5 words")
        return v


class EscalationResponse(BaseSchema):
    """Escalation response with complete information."""
    
    complaint_id: UUID
    complaint_number: str
    
    escalated: bool
    escalated_to: UUID
    escalated_to_name: str
    escalated_by: UUID
    escalated_by_name: str
    escalated_at: datetime
    
    new_priority: str
    
    message: str

    @classmethod
    def create(
        cls,
        complaint_id: UUID,
        complaint_number: str,
        escalated_to: UUID,
        escalated_to_name: str,
        escalated_by: UUID,
        escalated_by_name: str,
        new_priority: str
    ) -> "EscalationResponse":
        """Factory method to create escalation response."""
        return cls(
            complaint_id=complaint_id,
            complaint_number=complaint_number,
            escalated=True,
            escalated_to=escalated_to,
            escalated_to_name=escalated_to_name,
            escalated_by=escalated_by,
            escalated_by_name=escalated_by_name,
            escalated_at=datetime.utcnow(),
            new_priority=new_priority,
            message=f"Complaint {complaint_number} escalated to {escalated_to_name}"
        )


class EscalationHistory(BaseSchema):
    """Escalation history for complaint."""
    
    complaint_id: UUID
    complaint_number: str
    
    escalations: List["EscalationEntry"]
    total_escalations: int

    @property
    def is_frequently_escalated(self) -> bool:
        """Check if complaint is frequently escalated."""
        return self.total_escalations >= 3


class EscalationEntry(BaseResponseSchema):
    """Individual escalation entry with metrics."""
    
    escalated_to: UUID
    escalated_to_name: str
    escalated_by: UUID
    escalated_by_name: str
    escalated_at: datetime
    
    reason: str
    
    # Status at time of escalation
    status_before: str
    priority_before: str
    priority_after: str
    
    # Response time
    response_time_hours: Optional[int] = None
    resolved_after_escalation: bool

    @property
    def was_effective(self) -> bool:
        """Check if escalation was effective."""
        return self.resolved_after_escalation and (
            self.response_time_hours is not None and self.response_time_hours < 24
        )


class AutoEscalationRule(BaseSchema):
    """Auto-escalation rule configuration with validation."""
    
    hostel_id: UUID
    
    # Trigger conditions
    escalate_after_hours: int = Field(24, ge=1, le=168, description="Hours before auto-escalation")
    escalate_on_sla_breach: bool = Field(True)
    
    # Priority-based rules
    urgent_escalation_hours: int = Field(4, ge=1, le=24)
    high_escalation_hours: int = Field(12, ge=1, le=48)
    medium_escalation_hours: int = Field(24, ge=1, le=72)
    
    # Escalation chain
    first_escalation_to: UUID = Field(..., description="First level escalation")
    second_escalation_to: Optional[UUID] = Field(None, description="Second level if not resolved")
    
    is_active: bool = Field(True)

    @model_validator(mode="after")
    def validate_escalation_hours_hierarchy(self) -> "AutoEscalationRule":
        """Ensure escalation hours follow logical hierarchy."""
        if self.urgent_escalation_hours >= self.high_escalation_hours:
            raise ValueError("Urgent escalation hours must be less than high priority hours")
        if self.high_escalation_hours >= self.medium_escalation_hours:
            raise ValueError("High priority escalation hours must be less than medium priority hours")
        return self

    @model_validator(mode="after")
    def validate_escalation_chain(self) -> "AutoEscalationRule":
        """Ensure escalation chain is valid."""
        if self.second_escalation_to and self.first_escalation_to == self.second_escalation_to:
            raise ValueError("Second escalation level must be different from first level")
        return self