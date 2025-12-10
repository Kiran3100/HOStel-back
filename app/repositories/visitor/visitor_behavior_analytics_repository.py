# app/repositories/visitor/visitor_behavior_analytics_repository.py
from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository
from models.visitor import VisitorBehaviorAnalytics  # note: duplicates analytics table name


class VisitorBehaviorAnalyticsVisitorRepository(BaseRepository[VisitorBehaviorAnalytics]):
    """
    Visitor-side access to behavior analytics.
    (Table is shared with analytics. Use consistently in codebase.)
    """
    def __init__(self, session: Session):
        super().__init__(session, VisitorBehaviorAnalytics)

    def get_by_visitor_id(self, visitor_id: UUID) -> Optional[VisitorBehaviorAnalytics]:
        stmt = self._base_select().where(VisitorBehaviorAnalytics.visitor_id == visitor_id)
        return self.session.execute(stmt).scalar_one_or_none()