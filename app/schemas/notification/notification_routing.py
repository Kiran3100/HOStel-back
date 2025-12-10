"""
Notification routing schemas
"""
from typing import List, Optional, Dict
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema
from app.schemas.common.enums import UserRole, Priority


class RoutingConfig(BaseSchema):
    """Notification routing configuration"""
    hostel_id: UUID
    
    # Routing rules
    rules: List["RoutingRule"]
    
    # Escalation settings
    enable_escalation: bool = Field(True)
    escalation_timeout_hours: int = Field(24, ge=1, le=168)


class RoutingRule(BaseSchema):
    """Individual routing rule"""
    rule_name: str
    
    # Condition
    event_type: str = Field(..., description="complaint, payment, maintenance, etc.")
    priority: Optional[Priority] = None
    
    # Recipients
    recipient_roles: List[UserRole]
    specific_users: List[UUID] = Field(default_factory=list)
    
    # Channels
    channels: List[str] = Field(..., description="email, sms, push")
    
    # Active
    is_active: bool = Field(True)


class HierarchicalRouting(BaseSchema):
    """Hierarchical notification routing"""
    hostel_id: UUID
    event_type: str
    
    # Routing chain
    primary_recipients: List[UUID] = Field(..., description="Supervisors")
    secondary_recipients: List[UUID] = Field(default_factory=list, description="Admins")
    tertiary_recipients: List[UUID] = Field(default_factory=list, description="Super admin")
    
    # Escalation timing
    escalate_to_secondary_after_hours: int = Field(24)
    escalate_to_tertiary_after_hours: int = Field(48)


class EscalationRouting(BaseCreateSchema):
    """Escalation routing configuration"""
    notification_id: UUID
    
    # Escalation path
    escalation_chain: List["EscalationLevel"]
    
    # Current level
    current_level: int = Field(0)
    
    # Auto-escalate
    auto_escalate: bool = Field(True)


class EscalationLevel(BaseSchema):
    """Single level in escalation chain"""
    level: int
    recipients: List[UUID]
    escalate_after_hours: int
    channels: List[str]


class NotificationRoute(BaseSchema):
    """Determined notification route"""
    notification_id: UUID
    
    # Recipients
    primary_recipients: List[UUID]
    cc_recipients: List[UUID] = Field(default_factory=list)
    
    # Channels by recipient
    recipient_channels: Dict[UUID, List[str]]
    
    # Escalation
    escalation_enabled: bool
    escalation_path: Optional[List[EscalationLevel]]