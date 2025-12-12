# --- File: app/schemas/payment/payment_gateway.py ---
"""
Payment gateway integration schemas.

This module defines schemas for payment gateway integration including
requests, responses, webhooks, callbacks, and refund operations.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import Field, HttpUrl, field_validator

from app.schemas.common.base import BaseCreateSchema, BaseSchema

__all__ = [
    "GatewayRequest",
    "GatewayResponse",
    "GatewayWebhook",
    "GatewayCallback",
    "GatewayRefundRequest",
    "GatewayRefundResponse",
    "GatewayVerification",
]


class GatewayRequest(BaseSchema):
    """
    Payment gateway request payload.
    
    Contains all information needed to initiate payment
    with a payment gateway.
    """

    payment_id: UUID = Field(
        ...,
        description="Internal payment ID",
    )
    amount: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Payment amount",
    )
    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="Currency code (ISO 4217)",
    )

    # Customer Details
    customer_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Customer full name",
    )
    customer_email: str = Field(
        ...,
        description="Customer email",
    )
    customer_phone: str = Field(
        ...,
        pattern=r"^\+?[1-9]\d{9,14}$",
        description="Customer phone",
    )

    # Order Details
    order_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Unique order ID",
    )
    description: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Payment description",
    )

    # Callback URLs
    callback_url: HttpUrl = Field(
        ...,
        description="Server callback/webhook URL",
    )
    success_url: Optional[HttpUrl] = Field(
        None,
        description="Redirect URL on success",
    )
    failure_url: Optional[HttpUrl] = Field(
        None,
        description="Redirect URL on failure",
    )

    # Additional Metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional gateway-specific metadata",
    )

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        """Validate amount is positive."""
        if v <= 0:
            raise ValueError("Amount must be greater than zero")
        return v.quantize(Decimal("0.01"))

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        """Normalize currency code."""
        return v.upper().strip()


class GatewayResponse(BaseSchema):
    """
    Payment gateway response.
    
    Contains gateway response after payment initiation.
    """

    payment_id: UUID = Field(
        ...,
        description="Internal payment ID",
    )
    gateway_order_id: str = Field(
        ...,
        description="Gateway order/transaction ID",
    )
    gateway_payment_id: Optional[str] = Field(
        None,
        description="Gateway payment ID (set after completion)",
    )

    status: str = Field(
        ...,
        pattern=r"^(created|pending|authorized|captured|failed)$",
        description="Payment status from gateway",
    )

    amount: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Payment amount",
    )
    currency: str = Field(
        ...,
        description="Currency code",
    )

    # Gateway-Specific Data
    gateway_response: Dict[str, Any] = Field(
        ...,
        description="Complete gateway response payload",
    )

    # Timestamps
    created_at: datetime = Field(
        ...,
        description="When gateway order was created",
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp",
    )

    # Checkout Details (for client-side integration)
    checkout_url: Optional[HttpUrl] = Field(
        None,
        description="Gateway checkout page URL",
    )
    checkout_token: Optional[str] = Field(
        None,
        description="Checkout session token",
    )


class GatewayWebhook(BaseCreateSchema):
    """
    Payment gateway webhook payload.
    
    Represents webhook/callback received from payment gateway
    for payment status updates.
    """

    event_type: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Event type from gateway (e.g., payment.success)",
    )

    # Gateway Identifiers
    gateway_order_id: str = Field(
        ...,
        description="Gateway order ID",
    )
    gateway_payment_id: Optional[str] = Field(
        None,
        description="Gateway payment ID",
    )

    # Payment Details
    amount: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Payment amount",
    )
    currency: str = Field(
        ...,
        description="Currency code",
    )
    status: str = Field(
        ...,
        description="Payment status",
    )

    # Full Webhook Payload
    raw_payload: Dict[str, Any] = Field(
        ...,
        description="Complete webhook payload for auditing",
    )

    # Signature Verification
    signature: str = Field(
        ...,
        description="Webhook signature for verification",
    )

    # Timestamp
    event_timestamp: datetime = Field(
        ...,
        description="When event occurred (from gateway)",
    )

    @field_validator("event_type")
    @classmethod
    def normalize_event_type(cls, v: str) -> str:
        """Normalize event type."""
        return v.lower().strip()


class GatewayCallback(BaseSchema):
    """
    Payment gateway callback processing result.
    
    Represents processed callback data after verification.
    """

    payment_id: UUID = Field(
        ...,
        description="Internal payment ID",
    )
    gateway_payment_id: str = Field(
        ...,
        description="Gateway payment ID",
    )

    success: bool = Field(
        ...,
        description="Whether payment was successful",
    )
    status: str = Field(
        ...,
        description="Payment status",
    )

    amount_paid: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Amount actually paid",
    )

    # Error Details (if failed)
    error_code: Optional[str] = Field(
        None,
        description="Error code if payment failed",
    )
    error_message: Optional[str] = Field(
        None,
        description="Error message if payment failed",
    )

    # Additional Data
    callback_data: Dict[str, Any] = Field(
        ...,
        description="Processed callback data",
    )

    # Verification
    signature_verified: bool = Field(
        ...,
        description="Whether signature was verified",
    )


class GatewayRefundRequest(BaseCreateSchema):
    """
    Refund request to payment gateway.
    
    Initiates refund through payment gateway.
    """

    payment_id: UUID = Field(
        ...,
        description="Payment ID to refund",
    )
    gateway_payment_id: str = Field(
        ...,
        description="Gateway payment ID",
    )

    refund_amount: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Amount to refund",
    )
    reason: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Reason for refund",
    )

    # Refund Speed
    refund_speed: str = Field(
        "normal",
        pattern=r"^(normal|instant)$",
        description="Refund processing speed",
    )

    # Metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional refund metadata",
    )

    @field_validator("refund_amount")
    @classmethod
    def validate_refund_amount(cls, v: Decimal) -> Decimal:
        """Validate refund amount."""
        if v <= 0:
            raise ValueError("Refund amount must be greater than zero")
        return v.quantize(Decimal("0.01"))

    @field_validator("reason")
    @classmethod
    def validate_reason(cls, v: str) -> str:
        """Validate refund reason."""
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Refund reason must be at least 10 characters")
        return v


class GatewayRefundResponse(BaseSchema):
    """
    Refund response from payment gateway.
    
    Contains refund processing details from gateway.
    """

    refund_id: str = Field(
        ...,
        description="Internal refund ID",
    )
    gateway_refund_id: str = Field(
        ...,
        description="Gateway refund transaction ID",
    )

    status: str = Field(
        ...,
        description="Refund status (pending/processed/failed)",
    )
    amount: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Refund amount",
    )

    # Timeline
    estimated_completion_date: Optional[date] = Field(
        None,
        description="Estimated date when refund will be completed",
    )

    # Gateway Response
    gateway_response: Dict[str, Any] = Field(
        ...,
        description="Complete gateway refund response",
    )

    # Additional Information
    refund_mode: Optional[str] = Field(
        None,
        description="Refund mode (source/bank_transfer/etc)",
    )
    refund_arn: Optional[str] = Field(
        None,
        description="Acquirer Reference Number for refund",
    )


class GatewayVerification(BaseSchema):
    """
    Payment verification request.
    
    Used to verify payment status with gateway.
    """

    payment_id: UUID = Field(
        ...,
        description="Internal payment ID",
    )
    gateway_payment_id: str = Field(
        ...,
        description="Gateway payment ID to verify",
    )

    # Verification Result
    verified: bool = Field(
        ...,
        description="Whether payment is verified",
    )
    status: str = Field(
        ...,
        description="Verified payment status",
    )
    amount: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Verified amount",
    )

    # Gateway Response
    verification_response: Dict[str, Any] = Field(
        ...,
        description="Gateway verification response",
    )

    # Timestamp
    verified_at: datetime = Field(
        ...,
        description="Verification timestamp",
    )