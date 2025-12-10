# app/services/payment/payment_reminder_service.py
from __future__ import annotations

from datetime import datetime, timezone, date, timedelta
from decimal import Decimal
from typing import Protocol, List, Dict, Optional, Callable
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.transactions import PaymentRepository
from app.schemas.common.enums import PaymentStatus
from app.schemas.payment import (
    ReminderConfig,
    ReminderLog,
    SendReminderRequest,
    ReminderBatch,
    ReminderStats,
)
from app.services.common import UnitOfWork, errors


class ReminderConfigStore(Protocol):
    def get_config(self, hostel_id: UUID) -> Optional[dict]: ...
    def save_config(self, hostel_id: UUID, data: dict) -> None: ...


class ReminderLogStore(Protocol):
    def save_log(self, data: dict) -> dict: ...
    def list_logs_for_hostel(self, hostel_id: UUID, start: date, end: date) -> List[dict]: ...


class NotificationSender(Protocol):
    """
    Abstract notification sender, so you can plug in your notification service.
    """

    def send_email(self, *, to: str, subject: str, body: str) -> None: ...
    def send_sms(self, *, to: str, message: str) -> None: ...
    def send_push(self, *, user_id: UUID, title: str, body: str) -> None: ...


class PaymentReminderService:
    """
    Generate and send payment reminders based on ReminderConfig and Payment due dates.
    """

    def __init__(
        self,
        session_factory: Callable[[], Session],
        config_store: ReminderConfigStore,
        log_store: ReminderLogStore,
        notifier: NotificationSender,
    ) -> None:
        self._session_factory = session_factory
        self._config_store = config_store
        self._log_store = log_store
        self._notifier = notifier

    def _get_repo(self, uow: UnitOfWork) -> PaymentRepository:
        return uow.get_repo(PaymentRepository)

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    # ------------------------------------------------------------------ #
    # Config
    # ------------------------------------------------------------------ #
    def get_config(self, hostel_id: UUID) -> ReminderConfig:
        record = self._config_store.get_config(hostel_id)
        if record:
            return ReminderConfig.model_validate(record)
        cfg = ReminderConfig(hostel_id=hostel_id)
        self._config_store.save_config(hostel_id, cfg.model_dump())
        return cfg

    def set_config(self, config: ReminderConfig) -> None:
        self._config_store.save_config(config.hostel_id, config.model_dump())

    # ------------------------------------------------------------------ #
    # Sending reminders
    # ------------------------------------------------------------------ #
    def send_reminder(self, data: SendReminderRequest) -> ReminderBatch:
        """
        Simple implementation:
        - If payment_id is provided, remind that payment.
        - If student_id or hostel_id is provided, remind all due payments.
        """
        started_at = self._now()
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)

            payments = []
            hostel_id: Optional[UUID] = None

            if data.payment_id:
                p = repo.get(data.payment_id)
                if p:
                    payments = [p]
                    hostel_id = p.hostel_id
            elif data.student_id:
                payments = repo.list_for_student(data.student_id)
                hostel_id = payments[0].hostel_id if payments else None
            elif data.hostel_id:
                payments = repo.list_due_for_hostel(data.hostel_id, on_or_before=date.today())
                hostel_id = data.hostel_id

        reminders_sent = 0
        reminders_failed = 0
        email_sent = sms_sent = push_sent = 0

        for p in payments:
            if p.payment_status != PaymentStatus.PENDING:
                continue

            message = data.custom_message or "Your payment is due. Please pay at the earliest."
            try:
                if "email" in data.channels:
                    # In production, look up student/user email
                    self._notifier.send_email(to="", subject="Payment Reminder", body=message)
                    email_sent += 1
                if "sms" in data.channels:
                    self._notifier.send_sms(to="", message=message)
                    sms_sent += 1
                if "push" in data.channels:
                    self._notifier.send_push(user_id=p.payer_id, title="Payment Reminder", body=message)
                    push_sent += 1

                log = {
                    "payment_id": str(p.id),
                    "payment_reference": f"PAY-{str(p.id)[:8].upper()}",
                    "student_id": str(p.student_id) if p.student_id else None,
                    "student_name": "",
                    "student_email": "",
                    "student_phone": "",
                    "reminder_type": data.reminder_type,
                    "reminder_channel": ",".join(data.channels),
                    "sent_at": self._now(),
                    "delivery_status": "sent",
                    "subject": None,
                    "message_preview": message[:100],
                    "opened": False,
                    "clicked": False,
                }
                self._log_store.save_log(log)
                reminders_sent += 1
            except Exception:
                reminders_failed += 1

        completed_at = self._now()
        return ReminderBatch(
            batch_id=UUID(int=0),
            total_payments=len(payments),
            reminders_sent=reminders_sent,
            reminders_failed=reminders_failed,
            email_sent=email_sent,
            sms_sent=sms_sent,
            push_sent=push_sent,
            started_at=started_at,
            completed_at=completed_at,
            status="completed" if reminders_failed == 0 else "failed",
        )

    # ------------------------------------------------------------------ #
    # Stats
    # ------------------------------------------------------------------ #
    def get_stats(self, hostel_id: UUID, *, period_start: date, period_end: date) -> ReminderStats:
        logs = self._log_store.list_logs_for_hostel(hostel_id, period_start, period_end)
        total = len(logs)
        due_soon = overdue = final = 0
        email = sms = push = 0

        for l in logs:
            t = l.get("reminder_type")
            if t == "due_soon":
                due_soon += 1
            elif t == "overdue":
                overdue += 1
            elif t == "final_notice":
                final += 1
            ch = l.get("reminder_channel", "")
            if "email" in ch:
                email += 1
            if "sms" in ch:
                sms += 1
            if "push" in ch:
                push += 1

        payment_rate = Decimal("0")
        avg_days = Decimal("0")

        return ReminderStats(
            hostel_id=hostel_id,
            period_start=period_start,
            period_end=period_end,
            total_reminders_sent=total,
            due_soon_reminders=due_soon,
            overdue_reminders=overdue,
            final_notices=final,
            email_reminders=email,
            sms_reminders=sms,
            push_reminders=push,
            payment_rate_after_reminder=payment_rate,
            average_days_to_payment=avg_days,
        )