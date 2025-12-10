"""
Complaint escalation schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class EscalationRequest(BaseCreateSchema):
    """Escalate complaint"""
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


class EscalationResponse(BaseSchema):
    """Escalation response"""
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


class EscalationHistory(BaseSchema):
    """Escalation history for complaint"""
    complaint_id: UUID
    complaint_number: str
    
    escalations: List["EscalationEntry"]
    total_escalations: int


class EscalationEntry(BaseResponseSchema):
    """Individual escalation entry"""
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


class AutoEscalationRule(BaseSchema):
    """Auto-escalation rule configuration"""
    hostel_id: UUID
    
    # Trigger conditions
    escalate_after_hours: int = Field(24, description="Hours before auto-escalation")
    escalate_on_sla_breach: bool = Field(True)
    
    # Priority-based rules
    urgent_escalation_hours: int = Field(4)
    high_escalation_hours: int = Field(12)
    medium_escalation_hours: int = Field(24)
    
    # Escalation chain
    first_escalation_to: UUID = Field(..., description="First level escalation")
    second_escalation_to: Optional[UUID] = Field(None, description="Second level if not resolved")
    
    is_active: bool = Field(True)