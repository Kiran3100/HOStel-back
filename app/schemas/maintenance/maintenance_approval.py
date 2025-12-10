"""
Maintenance approval schemas
"""
from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class ApprovalRequest(BaseCreateSchema):
    """Request approval for maintenance (supervisor to admin)"""
    maintenance_id: UUID
    
    # Cost details
    estimated_cost: Decimal = Field(..., ge=0)
    cost_breakdown: Optional[dict] = Field(None, description="Detailed cost breakdown")
    
    # Justification
    approval_reason: str = Field(..., min_length=20, max_length=500)
    
    # Urgency
    urgent: bool = Field(False)
    
    # Preferred vendor
    preferred_vendor: Optional[str] = None
    vendor_quote: Optional[str] = None


class ApprovalResponse(BaseSchema):
    """Approval response"""
    maintenance_id: UUID
    request_number: str
    
    approved: bool
    approved_by: UUID
    approved_by_name: str
    approved_at: datetime
    
    # Approved amount (may differ from requested)
    approved_amount: Decimal
    
    # Conditions
    approval_conditions: Optional[str] = None
    
    message: str


class ThresholdConfig(BaseSchema):
    """Approval threshold configuration"""
    hostel_id: UUID
    
    # Supervisor threshold
    supervisor_approval_limit: Decimal = Field(
        Decimal("5000.00"),
        ge=0,
        description="Amount supervisor can approve independently"
    )
    
    # Admin required above this
    admin_approval_required_above: Decimal = Field(Decimal("5000.00"), ge=0)
    
    # Auto-approve below threshold
    auto_approve_below: Decimal = Field(Decimal("1000.00"), ge=0)
    
    # Emergency handling
    emergency_bypass_threshold: bool = Field(
        True,
        description="Allow emergency requests to bypass threshold"
    )


class ApprovalWorkflow(BaseSchema):
    """Approval workflow status"""
    maintenance_id: UUID
    request_number: str
    
    estimated_cost: Decimal
    threshold_exceeded: bool
    
    requires_approval: bool
    approval_pending: bool
    
    # Current approver
    pending_with: Optional[UUID] = None
    pending_with_name: Optional[str] = None
    
    # Timeline
    submitted_for_approval_at: Optional[datetime] = None
    approval_deadline: Optional[datetime] = None


class RejectionRequest(BaseCreateSchema):
    """Reject approval request"""
    maintenance_id: UUID
    rejection_reason: str = Field(..., min_length=20, max_length=500)
    
    # Suggestions
    suggested_alternative: Optional[str] = None
    suggested_cost_reduction: Optional[Decimal] = None