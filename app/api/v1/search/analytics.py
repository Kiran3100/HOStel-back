# app/api/v1/search/analytics.py
from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core import get_session
from app.services import UnitOfWork
from app.services.search import SearchAnalyticsService
from app.schemas.search.search_analytics import SearchAnalytics
from . import CurrentUser, get_current_user

router = APIRouter(tags=["Search - Analytics"])


def _get_service(session: Session) -> SearchAnalyticsService:
    uow = UnitOfWork(session)
    return SearchAnalyticsService(uow)


@router.get("/summary", response_model=SearchAnalytics)
def get_search_analytics(
    start_date: Optional[date] = Query(
        None,
        description="Start date for analytics window (inclusive). If omitted, uses a default window.",
    ),
    end_date: Optional[date] = Query(
        None,
        description="End date for analytics window (inclusive). If omitted, uses today.",
    ),
    session: Session = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
) -> SearchAnalytics:
    """
    Aggregated search analytics for a period.

    Expected service method:
        get_analytics(start_date: Optional[date], end_date: Optional[date]) -> SearchAnalytics
    """
    service = _get_service(session)
    return service.get_analytics(
        start_date=start_date,
        end_date=end_date,
    )