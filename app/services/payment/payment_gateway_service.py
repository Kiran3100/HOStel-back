# app/services/payment/payment_gateway_service.py
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Protocol, Dict, Any
from uuid import UUID

from app.schemas.payment import (
    GatewayRequest,
    GatewayResponse,
    GatewayWebhook,
    GatewayCallback,
)
from app.services.common import errors


class PaymentGatewayClient(Protocol):
    """
    Abstract payment gateway client.

    Implement this for Razorpay, Stripe, Paytm, etc.
    """

    def create_order(self, data: GatewayRequest) -> GatewayResponse: ...
    def handle_webhook(self, data: GatewayWebhook) -> GatewayCallback: ...


class PaymentGatewayService:
    """
    High-level wrapper around a PaymentGatewayClient.

    - Build GatewayRequest from Payment information
    - Delegate to client
    """

    def __init__(self, client: PaymentGatewayClient, gateway_key: str) -> None:
        self._client = client
        self._gateway_key = gateway_key

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def create_order_for_payment(
        self,
        *,
        payment_id: UUID,
        amount: Decimal,
        currency: str,
        customer_name: str,
        customer_email: str,
        customer_phone: str,
        description: str,
    ):
        req = GatewayRequest(
            payment_id=payment_id,
            amount=amount,
            currency=currency,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            order_id=f"ORD-{str(payment_id)[:8].upper()}",
            description=description,
            callback_url="",
            success_url=None,
            failure_url=None,
            metadata={},
        )
        resp = self._client.create_order(req)
        # Convert GatewayResponse -> PaymentInitiation schema
        from app.schemas.payment import PaymentInitiation

        return PaymentInitiation(
            payment_id=payment_id,
            payment_reference=f"PAY-{str(payment_id)[:8].upper()}",
            amount=amount,
            currency=currency,
            gateway="generic",
            gateway_order_id=resp.gateway_order_id,
            gateway_key=self._gateway_key,
            checkout_url=None,
            checkout_token=None,
            gateway_options=resp.gateway_response,
        )

    def process_webhook(self, data: GatewayWebhook) -> GatewayCallback:
        return self._client.handle_webhook(data)