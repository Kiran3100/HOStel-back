# app/services/payment/payment_service.py
from __future__ import annotations

from datetime import datetime, timezone, date
from decimal import Decimal
from typing import Callable, Optional, Sequence, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.transactions import PaymentRepository
from app.repositories.core import HostelRepository, StudentRepository, UserRepository, BookingRepository
from app.schemas.common.enums import PaymentStatus, PaymentType
from app.schemas.common.pagination import PaginationParams, PaginatedResponse
from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentFilterParams,
    PaymentResponse,
    PaymentDetail,
    PaymentListItem,
    PaymentSummary,
)
from app.services.common import UnitOfWork, pagination, errors


class PaymentService:
    """
    Core Payment service over txn_payment:

    - Create payments (used by request services / manual recording)
    - Update payments (status, gateway info, receipts)
    - Get payment detail
    - List/filter payments
    - Compute basic payment summaries for student/hostel
    """

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _get_repo(self, uow: UnitOfWork) -> PaymentRepository:
        return uow.get_repo(PaymentRepository)

    def _get_hostel_repo(self, uow: UnitOfWork) -> HostelRepository:
        return uow.get_repo(HostelRepository)

    def _get_student_repo(self, uow: UnitOfWork) -> StudentRepository:
        return uow.get_repo(StudentRepository)

    def _get_user_repo(self, uow: UnitOfWork) -> UserRepository:
        return uow.get_repo(UserRepository)

    def _get_booking_repo(self, uow: UnitOfWork) -> BookingRepository:
        return uow.get_repo(BookingRepository)

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _reference(self, payment_id: UUID) -> str:
        return f"PAY-{str(payment_id)[:8].upper()}"

    def _is_overdue(self, p) -> bool:
        if p.payment_status not in (PaymentStatus.PENDING, PaymentStatus.PROCESSING):
            return False
        if p.due_date is None:
            return False
        return date.today() > p.due_date

    # ------------------------------------------------------------------ #
    # Mapping helpers
    # ------------------------------------------------------------------ #
    def _to_response(self, p, hostel_name: str, payer_name: str) -> PaymentResponse:
        return PaymentResponse(
            id=p.id,
            created_at=p.created_at,
            updated_at=p.updated_at,
            payment_reference=self._reference(p.id),
            transaction_id=p.transaction_id,
            payer_id=p.payer_id,
            payer_name=payer_name,
            hostel_id=p.hostel_id,
            hostel_name=hostel_name,
            payment_type=p.payment_type,
            amount=p.amount,
            currency=p.currency,
            payment_method=p.payment_method,
            payment_status=p.payment_status,
            paid_at=p.paid_at,
            due_date=p.due_date,
            is_overdue=self._is_overdue(p),
            receipt_number=p.receipt_number,
            receipt_url=p.receipt_url,
        )

    def _to_detail(
        self,
        p,
        payer_name: str,
        payer_email: str,
        payer_phone: str,
        hostel_name: str,
        student_name: Optional[str],
        booking_ref: Optional[str],
    ) -> PaymentDetail:
        is_overdue = self._is_overdue(p)
        refund_amount = Decimal("0")
        refund_status = "none"
        refunded_at = None
        refund_tx_id = None
        refund_reason = None

        reminder_sent_count = 0
        last_reminder_sent_at = None

        return PaymentDetail(
            id=p.id,
            created_at=p.created_at,
            updated_at=p.updated_at,
            payment_reference=self._reference(p.id),
            transaction_id=p.transaction_id,
            payer_id=p.payer_id,
            payer_name=payer_name,
            payer_email=payer_email,
            payer_phone=payer_phone,
            hostel_id=p.hostel_id,
            hostel_name=hostel_name,
            student_id=p.student_id,
            student_name=student_name,
            booking_id=p.booking_id,
            booking_reference=booking_ref,
            payment_type=p.payment_type,
            amount=p.amount,
            currency=p.currency,
            payment_period_start=p.payment_period_start,
            payment_period_end=p.payment_period_end,
            payment_method=p.payment_method,
            payment_gateway=p.payment_gateway,
            payment_status=p.payment_status,
            paid_at=p.paid_at,
            failed_at=p.failed_at,
            failure_reason=p.failure_reason,
            gateway_response=None,
            receipt_number=p.receipt_number,
            receipt_url=p.receipt_url,
            receipt_generated_at=None,
            refund_amount=refund_amount,
            refund_status=refund_status,
            refunded_at=refunded_at,
            refund_transaction_id=refund_tx_id,
            refund_reason=refund_reason,
            collected_by=None,
            collected_by_name=None,
            collected_at=None,
            due_date=p.due_date,
            is_overdue=is_overdue,
            reminder_sent_count=reminder_sent_count,
            last_reminder_sent_at=last_reminder_sent_at,
        )

    def _to_list_item(self, p, payer_name: str, hostel_name: str) -> PaymentListItem:
        return PaymentListItem(
            id=p.id,
            payment_reference=self._reference(p.id),
            payer_name=payer_name,
            hostel_name=hostel_name,
            payment_type=p.payment_type.value if hasattr(p.payment_type, "value") else str(p.payment_type),
            amount=p.amount,
            payment_method=p.payment_method.value if hasattr(p.payment_method, "value") else str(p.payment_method),
            payment_status=p.payment_status,
            paid_at=p.paid_at,
            due_date=p.due_date,
            is_overdue=self._is_overdue(p),
            created_at=p.created_at,
        )

    # ------------------------------------------------------------------ #
    # Read
    # ------------------------------------------------------------------ #
    def get_payment(self, payment_id: UUID) -> PaymentDetail:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)
            hostel_repo = self._get_hostel_repo(uow)
            user_repo = self._get_user_repo(uow)
            student_repo = self._get_student_repo(uow)
            booking_repo = self._get_booking_repo(uow)

            p = repo.get(payment_id)
            if p is None:
                raise errors.NotFoundError(f"Payment {payment_id} not found")

            payer = user_repo.get(p.payer_id)
            hostel = hostel_repo.get(p.hostel_id)
            student = student_repo.get(p.student_id) if p.student_id else None
            booking = booking_repo.get(p.booking_id) if p.booking_id else None

            payer_name = payer.full_name if payer else ""
            payer_email = payer.email if payer else ""
            payer_phone = payer.phone if payer else ""
            hostel_name = hostel.name if hostel else ""
            student_name = student.user.full_name if student and getattr(student, "user", None) else None
            booking_ref = f"BKG-{str(booking.id)[:8].upper()}" if booking else None  # type: ignore[name-defined]

            return self._to_detail(
                p,
                payer_name=payer_name,
                payer_email=payer_email,
                payer_phone=payer_phone,
                hostel_name=hostel_name,
                student_name=student_name,
                booking_ref=booking_ref,
            )

    # ------------------------------------------------------------------ #
    # Listing & filters
    # ------------------------------------------------------------------ #
    def list_payments(
        self,
        params: PaginationParams,
        filters: Optional[PaymentFilterParams] = None,
    ) -> PaginatedResponse[PaymentListItem]:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)
            hostel_repo = self._get_hostel_repo(uow)
            user_repo = self._get_user_repo(uow)

            raw_filters: dict = {}
            if filters:
                if filters.hostel_id:
                    raw_filters["hostel_id"] = filters.hostel_id
                if filters.student_id:
                    raw_filters["student_id"] = filters.student_id
                if filters.payer_id:
                    raw_filters["payer_id"] = filters.payer_id
                if filters.payment_type:
                    raw_filters["payment_type"] = filters.payment_type
                if filters.payment_method:
                    raw_filters["payment_method"] = filters.payment_method
                if filters.payment_status:
                    raw_filters["payment_status"] = filters.payment_status

            records: Sequence = repo.get_multi(
                skip=params.offset,
                limit=params.limit,
                filters=raw_filters or None,
                order_by=[repo.model.created_at.desc()],  # type: ignore[attr-defined]
            )
            total = repo.count(filters=raw_filters or None)

            hostel_cache: dict[UUID, str] = {}
            payer_cache: dict[UUID, str] = {}
            items: List[PaymentListItem] = []

            for p in records:
                if p.hostel_id not in hostel_cache:
                    h = hostel_repo.get(p.hostel_id)
                    hostel_cache[p.hostel_id] = h.name if h else ""
                hostel_name = hostel_cache[p.hostel_id]

                if p.payer_id not in payer_cache:
                    u = user_repo.get(p.payer_id)
                    payer_cache[p.payer_id] = u.full_name if u else ""
                payer_name = payer_cache[p.payer_id]

                items.append(self._to_list_item(p, payer_name=payer_name, hostel_name=hostel_name))

            return PaginatedResponse[PaymentListItem].create(
                items=items,
                total_items=total,
                page=params.page,
                page_size=params.page_size,
            )

    # ------------------------------------------------------------------ #
    # Create / update
    # ------------------------------------------------------------------ #
    def create_payment(self, data: PaymentCreate) -> PaymentDetail:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)

            payload = data.model_dump()
            # Ensure default status
            payload.setdefault("payment_status", PaymentStatus.PENDING)
            p = repo.create(payload)  # type: ignore[arg-type]
            uow.commit()
            return self.get_payment(p.id)

    def update_payment(self, payment_id: UUID, data: PaymentUpdate) -> PaymentDetail:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)
            p = repo.get(payment_id)
            if p is None:
                raise errors.NotFoundError(f"Payment {payment_id} not found")

            mapping = data.model_dump(exclude_unset=True)
            for field, value in mapping.items():
                if hasattr(p, field) and field != "id":
                    setattr(p, field, value)

            uow.session.flush()  # type: ignore[union-attr]
            uow.commit()
            return self.get_payment(payment_id)

    # ------------------------------------------------------------------ #
    # State helpers
    # ------------------------------------------------------------------ #
    def mark_paid(
        self,
        payment_id: UUID,
        *,
        transaction_id: Optional[str],
        paid_at: Optional[datetime] = None,
    ) -> PaymentDetail:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)
            p = repo.get(payment_id)
            if p is None:
                raise errors.NotFoundError(f"Payment {payment_id} not found")

            p.payment_status = PaymentStatus.COMPLETED  # type: ignore[attr-defined]
            p.transaction_id = transaction_id  # type: ignore[attr-defined]
            p.paid_at = paid_at or self._now()  # type: ignore[attr-defined]

            uow.session.flush()  # type: ignore[union-attr]
            uow.commit()
            return self.get_payment(payment_id)

    def mark_failed(
        self,
        payment_id: UUID,
        *,
        failure_reason: Optional[str],
    ) -> PaymentDetail:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)
            p = repo.get(payment_id)
            if p is None:
                raise errors.NotFoundError(f"Payment {payment_id} not found")

            p.payment_status = PaymentStatus.FAILED  # type: ignore[attr-defined]
            p.failed_at = self._now()  # type: ignore[attr-defined]
            p.failure_reason = failure_reason  # type: ignore[attr-defined]

            uow.session.flush()  # type: ignore[union-attr]
            uow.commit()
            return self.get_payment(payment_id)

    # ------------------------------------------------------------------ #
    # Summaries
    # ------------------------------------------------------------------ #
    def get_summary_for_entity(self, entity_id: UUID, entity_type: str) -> PaymentSummary:
        """
        Compute PaymentSummary for a student or a hostel.
        """
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)

            if entity_type == "student":
                payments = repo.list_for_student(entity_id)
            elif entity_type == "hostel":
                # All payments for hostel; repository has list_due_for_hostel, but not list all
                payments = repo.get_multi(filters={"hostel_id": entity_id})
            else:
                raise errors.ValidationError("entity_type must be 'student' or 'hostel'")

        total_paid = Decimal("0")
        total_pending = Decimal("0")
        total_overdue = Decimal("0")
        last_payment_date: Optional[date] = None
        next_due_date: Optional[date] = None

        total_payments = len(payments)
        completed_payments = 0
        pending_payments = 0

        for p in payments:
            if p.payment_status == PaymentStatus.COMPLETED:
                total_paid += p.amount
                completed_payments += 1
                if p.paid_at:
                    d = p.paid_at.date()
                    if not last_payment_date or d > last_payment_date:
                        last_payment_date = d
            elif p.payment_status == PaymentStatus.PENDING:
                total_pending += p.amount
                pending_payments += 1
                if p.due_date:
                    if not next_due_date or p.due_date < next_due_date:
                        next_due_date = p.due_date
                    if p.due_date < date.today():
                        total_overdue += p.amount

        return PaymentSummary(
            entity_id=entity_id,
            entity_type=entity_type,
            total_paid=total_paid,
            total_pending=total_pending,
            total_overdue=total_overdue,
            last_payment_date=last_payment_date,
            next_payment_due_date=next_due_date,
            total_payments=total_payments,
            completed_payments=completed_payments,
            pending_payments=pending_payments,
        )