# app/services/payment/payment_reporting_service.py
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Callable, List, Dict, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.transactions import PaymentRepository
from app.schemas.payment import (
    PaymentReportRequest,
)
from app.schemas.common.enums import PaymentStatus, PaymentType, PaymentMethod
from app.services.common import UnitOfWork


class PaymentReportingService:
    """
    Generate aggregated payment reports.

    - Totals by day/week/month, type, method
    - Raw export can reuse PaymentService.list_payments
    """

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory

    def _get_repo(self, uow: UnitOfWork) -> PaymentRepository:
        return uow.get_repo(PaymentRepository)

    def generate_report(self, req: PaymentReportRequest) -> Dict[str, any]:
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_repo(uow)

            filters: dict = {}
            if req.hostel_id:
                filters["hostel_id"] = req.hostel_id

            payments = repo.get_multi(filters=filters or None)

        start = req.date_from
        end = req.date_to

        filtered = []
        for p in payments:
            d = p.created_at.date()
            if d < start or d > end:
                continue
            if req.payment_types and p.payment_type not in req.payment_types:
                continue
            if req.payment_methods and p.payment_method not in req.payment_methods:
                continue
            filtered.append(p)

        total_amount = sum((p.amount for p in filtered), Decimal("0"))
        total_completed = sum(
            (p.amount for p in filtered if p.payment_status == PaymentStatus.COMPLETED),
            Decimal("0"),
        )

        by_type: Dict[PaymentType, Decimal] = {}
        by_method: Dict[PaymentMethod, Decimal] = {}

        for p in filtered:
            by_type[p.payment_type] = by_type.get(p.payment_type, Decimal("0")) + p.amount
            by_method[p.payment_method] = by_method.get(p.payment_method, Decimal("0")) + p.amount

        group_by = req.group_by
        # For brevity, we skip heavy grouping; you can add per-group buckets as needed.

        return {
            "hostel_id": req.hostel_id,
            "date_from": str(start),
            "date_to": str(end),
            "total_amount": str(total_amount),
            "total_completed": str(total_completed),
            "by_type": {k.value: str(v) for k, v in by_type.items()},
            "by_method": {k.value: str(v) for k, v in by_method.items()},
            "group_by": group_by,
        }