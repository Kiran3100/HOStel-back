# app/services/payment/payment_ledger_service.py
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Callable, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.transactions import PaymentRepository
from app.schemas.payment import (
    LedgerEntry,
    LedgerSummary,
    AccountStatement,
    TransactionHistory,
    TransactionItem,
    BalanceAdjustment,
    WriteOff,
)
from app.schemas.common.enums import PaymentStatus
from app.services.common import UnitOfWork, errors


class PaymentLedgerService:
    """
    Compute a virtual ledger from payments.

    NOTE:
    - This does not persist ledger rows;
      it derives them from txn_payment for reporting.
    """

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory

    def _get_repo(self, uow: UnitOfWork) -> PaymentRepository:
        return uow.get_repo(PaymentRepository)

    def _now(self) -> datetime:
        return datetime.now()

    # ------------------------------------------------------------------ #
    # Ledger summary
    # ------------------------------------------------------------------ #
    def get_ledger_summary(self, student_id: UUID, hostel_id: UUID) -> LedgerSummary:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)
            payments = repo.list_for_student(student_id)

        total_charges = Decimal("0")
        total_payments = Decimal("0")
        total_refunds = Decimal("0")

        last_transaction_date = None
        last_payment_date = None

        for p in payments:
            if p.payment_status == PaymentStatus.COMPLETED:
                total_payments += p.amount
                if p.paid_at:
                    d = p.paid_at.date()
                    if not last_payment_date or d > last_payment_date:
                        last_payment_date = d
                    if not last_transaction_date or d > last_transaction_date:
                        last_transaction_date = d

        current_balance = total_charges - total_payments + total_refunds
        total_due = current_balance if current_balance > 0 else Decimal("0")
        overdue_amount = Decimal("0")  # requires due-date logic; omitted

        return LedgerSummary(
            student_id=student_id,
            student_name="",
            hostel_id=hostel_id,
            hostel_name="",
            current_balance=current_balance,
            total_charges=total_charges,
            total_payments=total_payments,
            total_refunds=total_refunds,
            total_due=total_due,
            overdue_amount=overdue_amount,
            last_transaction_date=last_transaction_date,
            last_payment_date=last_payment_date,
        )

    # ------------------------------------------------------------------ #
    # Account statement
    # ------------------------------------------------------------------ #
    def get_account_statement(
        self,
        student_id: UUID,
        hostel_id: UUID,
        *,
        start: date,
        end: date,
    ) -> AccountStatement:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)
            payments = repo.list_for_student(student_id)

        opening_balance = Decimal("0")
        entries: List[LedgerEntry] = []
        total_debits = Decimal("0")
        total_credits = Decimal("0")

        for p in payments:
            if not p.paid_at:
                continue
            d = p.paid_at.date()
            if d < start:
                # accumulate into opening balance
                opening_balance -= p.amount  # treat payment as credit; charges are external
                continue
            if d > end:
                continue

            # Payment = credit
            balance_before = opening_balance + total_debits - total_credits
            total_credits += p.amount
            balance_after = opening_balance + total_debits - total_credits

            entries.append(
                LedgerEntry(
                    id=None,
                    created_at=p.created_at,
                    updated_at=p.updated_at,
                    student_id=student_id,
                    hostel_id=hostel_id,
                    entry_date=d,
                    entry_type="credit",
                    transaction_type=p.payment_type.value if hasattr(p.payment_type, "value") else str(p.payment_type),
                    amount=p.amount,
                    balance_before=balance_before,
                    balance_after=balance_after,
                    payment_id=p.id,
                    payment_reference=f"PAY-{str(p.id)[:8].upper()}",
                    description="Payment received",
                    created_by=None,
                    notes=None,
                )
            )

        closing_balance = opening_balance + total_debits - total_credits

        return AccountStatement(
            student_id=student_id,
            student_name="",
            hostel_id=hostel_id,
            hostel_name="",
            statement_period_start=start,
            statement_period_end=end,
            generated_at=self._now(),
            opening_balance=opening_balance,
            entries=entries,
            total_debits=total_debits,
            total_credits=total_credits,
            closing_balance=closing_balance,
            pdf_url=None,
        )

    # ------------------------------------------------------------------ #
    # Transaction history
    # ------------------------------------------------------------------ #
    def get_transaction_history(
        self,
        student_id: UUID,
        page: int,
        page_size: int,
    ) -> TransactionHistory:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)
            payments = repo.list_for_student(student_id)

        payments_sorted = sorted(payments, key=lambda p: p.created_at, reverse=True)
        total = len(payments_sorted)
        start = (page - 1) * page_size
        end = start + page_size
        page_payments = payments_sorted[start:end]

        balance_after = Decimal("0")
        items: List[TransactionItem] = []
        for p in page_payments:
            items.append(
                TransactionItem(
                    transaction_id=p.id,
                    transaction_date=p.created_at,
                    transaction_type=p.payment_type.value if hasattr(p.payment_type, "value") else str(p.payment_type),
                    amount=p.amount,
                    balance_after=balance_after,
                    description="Payment",
                    payment_reference=f"PAY-{str(p.id)[:8].upper()}",
                    status=p.payment_status.value if hasattr(p.payment_status, "value") else str(p.payment_status),
                )
            )

        return TransactionHistory(
            student_id=student_id,
            transactions=items,
            total_transactions=total,
            page=page,
            page_size=page_size,
        )

    # Adjustments & write-offs would normally be separate persisted records;
    # here we only define their schemas, not state changes.
    def record_adjustment(self, data: BalanceAdjustment) -> None:
        # Persist as a separate table/collection in real implementation
        pass

    def record_writeoff(self, data: WriteOff) -> None:
        # Persist as a separate table/collection in real implementation
        pass