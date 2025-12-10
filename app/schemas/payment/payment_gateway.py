"""
Payment gateway integration schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class GatewayRequest(BaseSchema):
    """Payment gateway request"""
    payment_id: UUID
    amount: Decimal
    currency: str
    
    # Customer details
    customer_name: str
    customer_email: str
    customer_phone: str
    
    # Order details
    order_id: str
    description: str
    
    # Callback URLs
    callback_url: str
    success_url: Optional[str]
    failure_url: Optional[str]
    
    # Additional metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GatewayResponse(BaseSchema):
    """Payment gateway response"""
    payment_id: UUID
    gateway_order_id: str
    gateway_payment_id: Optional[str]
    
    status: str = Field(..., pattern="^(created|pending|authorized|captured|failed)$")
    
    amount: Decimal
    currency: str
    
    # Gateway-specific data
    gateway_response: Dict[str, Any]
    
    # Timestamps
    created_at: datetime
    updated_at: datetime


class GatewayWebhook(BaseCreateSchema):
    """Payment gateway webhook payload"""
    event_type: str = Field(..., description="Event type from gateway")
    
    # Gateway identifiers
    gateway_order_id: str
    gateway_payment_id: Optional[str]
    
    # Payment details
    amount: Decimal
    currency: str
    status: str
    
    # Full webhook payload
    raw_payload: Dict[str, Any] = Field(..., description="Complete webhook payload")
    
    # Signature verification
    signature: str = Field(..., description="Webhook signature")
    
    # Timestamp
    event_timestamp: datetime


class GatewayCallback(BaseSchema):
    """Payment gateway callback processing"""
    payment_id: UUID
    gateway_payment_id: str
    
    success: bool
    status: str
    
    amount_paid: Decimal
    
    # Error details (if failed)
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    
    # Additional data
    callback_data: Dict[str, Any]


class GatewayRefundRequest(BaseCreateSchema):
    """Refund request to gateway"""
    payment_id: UUID
    gateway_payment_id: str
    
    refund_amount: Decimal
    reason: str = Field(..., min_length=10, max_length=500)
    
    # Speed
    refund_speed: str = Field("normal", pattern="^(normal|instant)$")


class GatewayRefundResponse(BaseSchema):
    """Refund response from gateway"""
    refund_id: str
    gateway_refund_id: str
    
    status: str
    amount: Decimal
    
    # Estimated timeline
    estimated_completion_date: Optional[date]
    
    gateway_response: Dict[str, Any]