# app/services/payment/payment_schedule_service.py
from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from typing import Protocol, List
from uuid import UUID

from app.schemas.payment import (
    PaymentSchedule,
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleGeneration,
    ScheduledPaymentGenerated,
    BulkScheduleCreate,
    ScheduleSuspension,
)
from app.schemas.common.enums import FeeType
from app.services.common import errors


class ScheduleStore(Protocol):
    """
    Store for recurring payment schedules (student-level).

    Implementations can use a DB table or Redis.
    """

    def create(self, data: dict) -> dict: ...
    def update(self, schedule_id: UUID, data: dict) -> dict: ...
    def get(self, schedule_id: UUID) -> dict | None: ...
    def list_for_student(self, student_id: UUID) -> List[dict]: ...


class PaymentScheduleService:
    """
    Manage recurring payment schedules for students (rent/mess, etc.).

    - Create/update schedules
    - Generate scheduled payments (via PaymentRequestService)
    """

    def __init__(self, store: ScheduleStore) -> None:
        self._store = store

    def create_schedule(self, data: ScheduleCreate, *, hostel_name: str, student_name: str) -> PaymentSchedule:
        record = {
            "id": None,
            "student_id": str(data.student_id),
            "student_name": student_name,
            "hostel_id": str(data.hostel_id),
            "hostel_name": hostel_name,
            "fee_type": data.fee_type.value if hasattr(data.fee_type, "value") else str(data.fee_type),
            "amount": str(data.amount),
            "start_date": data.start_date.isoformat(),
            "end_date": data.end_date.isoformat() if data.end_date else None,
            "next_due_date": data.first_due_date.isoformat(),
            "auto_generate_invoice": data.auto_generate_invoice,
            "is_active": True,
        }
        created = self._store.create(record)
        return PaymentSchedule(
            id=UUID(created["id"]),
            created_at=None,
            updated_at=None,
            student_id=data.student_id,
            student_name=student_name,
            hostel_id=data.hostel_id,
            hostel_name=hostel_name,
            fee_type=data.fee_type,
            amount=data.amount,
            start_date=data.start_date,
            end_date=data.end_date,
            next_due_date=data.first_due_date,
            auto_generate_invoice=data.auto_generate_invoice,
            is_active=True,
        )

    def update_schedule(self, schedule_id: UUID, data: ScheduleUpdate) -> PaymentSchedule:
        existing = self._store.get(schedule_id)
        if not existing:
            raise errors.NotFoundError(f"Schedule {schedule_id} not found")

        mapping = data.model_dump(exclude_unset=True)
        for field, value in mapping.items():
            if field == "amount" and value is not None:
                existing["amount"] = str(value)
            elif field in ("next_due_date", "end_date") and value is not None:
                existing[field] = value.isoformat()
            else:
                existing[field] = value

        updated = self._store.update(schedule_id, existing)

        return PaymentSchedule(
            id=schedule_id,
            created_at=None,
            updated_at=None,
            student_id=UUID(updated["student_id"]),
            student_name=updated.get("student_name", ""),
            hostel_id=UUID(updated["hostel_id"]),
            hostel_name=updated.get("hostel_name", ""),
            fee_type=FeeType(updated["fee_type"]),
            amount=Decimal(updated["amount"]),
            start_date=date.fromisoformat(updated["start_date"]),
            end_date=date.fromisoformat(updated["end_date"]) if updated.get("end_date") else None,
            next_due_date=date.fromisoformat(updated["next_due_date"]),
            auto_generate_invoice=updated.get("auto_generate_invoice", True),
            is_active=updated.get("is_active", True),
        )

    def generate_payments(self, data: ScheduleGeneration) -> ScheduledPaymentGenerated:
        """
        This only computes which dates a bill should be generated; actual Payment
        objects should be created by PaymentRequestService, using the returned dates.
        """
        schedule = self._store.get(data.schedule_id)
        if not schedule:
            raise errors.NotFoundError(f"Schedule {data.schedule_id} not found")

        fee_type = FeeType(schedule["fee_type"])
        step_days = {
            FeeType.MONTHLY: 30,
            FeeType.QUARTERLY: 90,
            FeeType.HALF_YEARLY: 180,
            FeeType.YEARLY: 365,
        }.get(fee_type, 30)

        current = date.fromisoformat(schedule["next_due_date"])
        payments_generated = 0
        payments_skipped = 0
        generated_ids: List[UUID] = []

        while current <= data.generate_to_date:
            if current >= data.generate_from_date:
                if data.skip_if_already_paid:
                    # In a real implementation you'd check existing payments
                    payments_skipped += 0
                payments_generated += 1
            current = current + timedelta(days=step_days)

        next_generation_date = current

        return ScheduledPaymentGenerated(
            schedule_id=data.schedule_id,
            payments_generated=payments_generated,
            payments_skipped=payments_skipped,
            generated_payment_ids=generated_ids,
            next_generation_date=next_generation_date,
        )

    def suspend_schedule(self, data: ScheduleSuspension) -> None:
        schedule = self._store.get(data.schedule_id)
        if not schedule:
            raise errors.NotFoundError(f"Schedule {data.schedule_id} not found")
        schedule["suspended"] = True
        schedule["suspend_from_date"] = data.suspend_from_date.isoformat()
        schedule["suspend_to_date"] = data.suspend_to_date.isoformat()
        schedule["skip_dues_during_suspension"] = data.skip_dues_during_suspension
        self._store.update(data.schedule_id, schedule)

    def bulk_create(self, data: BulkScheduleCreate, *, hostel_name: str, student_names: dict[UUID, str]) -> List[UUID]:
        ids: List[UUID] = []
        for sid in data.student_ids:
            sched = ScheduleCreate(
                student_id=sid,
                hostel_id=data.hostel_id,
                fee_type=data.fee_type,
                amount=data.amount,
                start_date=data.start_date,
                end_date=None,
                first_due_date=data.first_due_date,
                auto_generate_invoice=True,
                send_reminders=True,
            )
            created = self.create_schedule(
                sched,
                hostel_name=hostel_name,
                student_name=student_names.get(sid, ""),
            )
            ids.append(created.id)
        return ids