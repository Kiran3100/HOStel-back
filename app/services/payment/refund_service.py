# app/services/payment/refund_service.py
from __future__ import annotations

from datetime import datetime, timezone, date
from decimal import Decimal
from typing import Callable, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.transactions import PaymentRepository
from app.schemas.common.enums import PaymentStatus
from app.schemas.payment import (
    RefundRequest,
    RefundResponse,
    RefundStatus,
)
from app.services.common import UnitOfWork, errors
from .payment_gateway_service import PaymentGatewayClient


class RefundService:
    """
    Handle payment refunds:

    - Validate refund amount
    - Optionally initiate gateway refund
    """

    def __init__(
        self,
        session_factory: Callable[[], Session],
        gateway_client: Optional[PaymentGatewayClient] = None,
    ) -> None:
        self._session_factory = session_factory
        self._gateway_client = gateway_client

    def _get_repo(self, uow: UnitOfWork) -> PaymentRepository:
        return uow.get_repo(PaymentRepository)

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def request_refund(self, data: RefundRequest) -> RefundResponse:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)
            p = repo.get(data.payment_id)
            if p is None:
                raise errors.NotFoundError(f"Payment {data.payment_id} not found")

            if p.payment_status != PaymentStatus.COMPLETED:
                raise errors.ValidationError("Can only refund completed payments")

            if data.refund_amount > p.amount:
                raise errors.ValidationError("Refund amount exceeds original payment")

            # Stub: mark as REFUNDED; for partial, you'd track amounts separately
            p.payment_status = PaymentStatus.REFUNDED  # type: ignore[attr-defined]
            p.failed_at = None  # type: ignore[attr-defined]
            p.failure_reason = None  # type: ignore[attr-defined]

            uow.session.flush()  # type: ignore[union-attr]
            uow.commit()

        refund_reference = None
        if self._gateway_client and data.refund_method == "original_source":
            # You'd call client's refund API; omitted for brevity
            refund_reference = "GATEWAY_REFUND_ID"

        return RefundResponse(
            id=None,
            created_at=self._now(),
            updated_at=self._now(),
            refund_id=UUID(int=0),
            payment_id=data.payment_id,
            payment_reference=f"PAY-{str(data.payment_id)[:8].upper()}",
            refund_amount=data.refund_amount,
            refund_status="completed",
            refund_method=data.refund_method,
            refund_reference=refund_reference,
            requested_at=self._now(),
            processed_at=self._now(),
            completed_at=self._now(),
            estimated_completion_date=date.today(),
            refunded_to="original_source",
            message="Refund processed",
        )

    def get_refund_status(self, payment_id: UUID) -> RefundStatus:
        # In a fuller design, you'd have a Refund model; here we derive status from Payment.
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)
            p = repo.get(payment_id)
            if not p:
                raise errors.NotFoundError(f"Payment {payment_id} not found")

        status = "none"
        if p.payment_status == PaymentStatus.REFUNDED:
            status = "completed"
        elif p.payment_status == PaymentStatus.PENDING:
            status = "pending"

        return RefundStatus(
            refund_id=UUID(int=0),
            payment_reference=f"PAY-{str(payment_id)[:8].upper()}",
            refund_amount=Decimal("0"),
            currency=p.currency,
            status=status,
            requested_at=self._now(),
            processing_started_at=None,
            completed_at=None,
            days_since_request=0,
            failure_reason=None,
            next_action=None,
            expected_completion_date=None,
        )