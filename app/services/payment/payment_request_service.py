# app/services/payment/payment_request_service.py
from __future__ import annotations

from datetime import datetime, timezone, date
from decimal import Decimal
from typing import Callable, Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.transactions import PaymentRepository
from app.schemas.common.enums import PaymentStatus, PaymentType, PaymentMethod
from app.schemas.payment import (
    PaymentRequest,
    PaymentInitiation,
    ManualPaymentRequest,
    BulkPaymentRequest,
    SinglePaymentRecord,
)
from app.services.common import UnitOfWork, errors
from .payment_gateway_service import PaymentGatewayClient, PaymentGatewayService


class PaymentRequestService:
    """
    High-level payment request service:

    - Initiate online payments (create Payment, prepare gateway order)
    - Record manual payments (cash/cheque/bank_transfer)
    - Bulk payment recording
    """

    def __init__(
        self,
        session_factory: Callable[[], Session],
        gateway_service: PaymentGatewayService,
    ) -> None:
        self._session_factory = session_factory
        self._gateway_service = gateway_service

    def _get_repo(self, uow: UnitOfWork) -> PaymentRepository:
        return uow.get_repo(PaymentRepository)

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _reference(self, payment_id: UUID) -> str:
        return f"PAY-{str(payment_id)[:8].upper()}"

    # ------------------------------------------------------------------ #
    # Online payment initiation
    # ------------------------------------------------------------------ #
    def initiate_online_payment(self, data: PaymentRequest, *, payer_id: UUID) -> PaymentInitiation:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)

            payload = {
                "payer_id": payer_id,
                "hostel_id": data.hostel_id,
                "student_id": data.student_id,
                "booking_id": data.booking_id,
                "payment_type": data.payment_type,
                "amount": data.amount,
                "currency": "INR",
                "payment_period_start": data.payment_period_start,
                "payment_period_end": data.payment_period_end,
                "payment_method": data.payment_method,
                "payment_gateway": data.payment_gateway,
                "payment_status": PaymentStatus.PENDING,
                "transaction_id": None,
                "due_date": None,
                "paid_at": None,
                "failed_at": None,
                "failure_reason": None,
                "receipt_number": None,
                "receipt_url": None,
            }
            p = repo.create(payload)  # type: ignore[arg-type]
            uow.commit()

        # Build gateway request & call gateway service
        initiation = self._gateway_service.create_order_for_payment(
            payment_id=p.id,
            amount=p.amount,
            currency=p.currency,
            customer_name="",
            customer_email="",
            customer_phone="",
            description=f"Payment {self._reference(p.id)}",
        )

        return initiation

    # ------------------------------------------------------------------ #
    # Manual payment recording
    # ------------------------------------------------------------------ #
    def record_manual_payment(self, data: ManualPaymentRequest) -> UUID:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)

            payload = {
                "payer_id": data.student_id,  # or guardian; adjust as needed
                "hostel_id": data.hostel_id,
                "student_id": data.student_id,
                "booking_id": None,
                "payment_type": data.payment_type,
                "amount": data.amount,
                "currency": "INR",
                "payment_period_start": data.payment_period_start,
                "payment_period_end": data.payment_period_end,
                "payment_method": data.payment_method,
                "payment_gateway": None,
                "payment_status": PaymentStatus.COMPLETED,
                "transaction_id": data.transaction_reference or data.cheque_number,
                "due_date": None,
                "paid_at": data.collection_date,
                "failed_at": None,
                "failure_reason": None,
                "receipt_number": None,
                "receipt_url": None,
            }
            p = repo.create(payload)  # type: ignore[arg-type]
            uow.commit()
            return p.id

    def record_bulk_payments(self, data: BulkPaymentRequest) -> List[UUID]:
        ids: List[UUID] = []
        for rec in data.payments:
            req = ManualPaymentRequest(
                hostel_id=data.hostel_id,
                student_id=rec.student_id,
                payment_type=rec.payment_type,
                amount=rec.amount,
                payment_method=rec.payment_method,
                cheque_number=None,
                cheque_date=None,
                bank_name=None,
                transaction_reference=rec.transaction_reference,
                transfer_date=data.collection_date,
                payment_period_start=None,
                payment_period_end=None,
                collected_by=data.collected_by,
                collection_date=data.collection_date,
                notes=rec.notes,
            )
            ids.append(self.record_manual_payment(req))
        return ids