# app/services/users/user_activity_service.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.audit import UserActivityRepository
from app.services.common import UnitOfWork


class UserActivityService:
    """
    Simple wrapper around audit.user_activity for recording user actions.

    This service is intentionally write-focused; most read/reporting use-cases
    can go via dedicated audit/reporting services.
    """

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    # ------------------------------------------------------------------ #
    # Public logging APIs
    # ------------------------------------------------------------------ #
    def log(
        self,
        *,
        user_id: UUID,
        activity_type: str,
        description: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """
        Record an arbitrary user activity event.

        :param user_id: ID of the user performing the action
        :param activity_type: logical type (e.g. 'login', 'logout', 'booking_created')
        :param description: human-readable description
        :param ip_address: optional IP
        :param user_agent: optional User-Agent string
        """
        with UnitOfWork(self._session_factory) as uow:
            repo = uow.get_repo(UserActivityRepository)
            payload = {
                "user_id": user_id,
                "activity_type": activity_type,
                "description": description,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "created_at": self._now(),
            }
            repo.create(payload)  # type: ignore[arg-type]
            uow.commit()

    def log_login(
        self,
        *,
        user_id: UUID,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """Convenience helper for login events."""
        self.log(
            user_id=user_id,
            activity_type="login",
            description="User logged in",
            ip_address=ip_address,
            user_agent=user_agent,
        )

    def log_logout(
        self,
        *,
        user_id: UUID,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """Convenience helper for logout events."""
        self.log(
            user_id=user_id,
            activity_type="logout",
            description="User logged out",
            ip_address=ip_address,
            user_agent=user_agent,
        )

    def log_password_change(
        self,
        *,
        user_id: UUID,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """Convenience helper for password change events."""
        self.log(
            user_id=user_id,
            activity_type="password_change",
            description="User changed password",
            ip_address=ip_address,
            user_agent=user_agent,
        )