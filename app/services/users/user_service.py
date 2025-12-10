# app/services/users/user_service.py
from __future__ import annotations

from typing import Callable, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.core import UserRepository
from app.schemas.common.enums import UserRole
from app.schemas.common.pagination import PaginationParams, PaginatedResponse
from app.schemas.user import (
    UserResponse,
    UserDetail,
    UserListItem,
    UserCreate,
    UserUpdate,
)
from app.services.common import UnitOfWork, mapping, pagination, errors


class UserService:
    """
    Core user read/update/list operations.

    NOTE:
    - Creation/registration flows should go via dedicated auth/registration
      services that also handle password hashing and role-specific setup.
    - This service assumes the User model is the canonical user record.
    """

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _get_user_repo(self, uow: UnitOfWork) -> UserRepository:
        return uow.get_repo(UserRepository)

    # ------------------------------------------------------------------ #
    # Read operations
    # ------------------------------------------------------------------ #
    def get_user(self, user_id: UUID) -> UserDetail:
        """Fetch a user by ID or raise NotFoundError."""
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_user_repo(uow)
            user = repo.get(user_id)
            if user is None:
                raise errors.NotFoundError(f"User {user_id} not found")

            return mapping.to_schema(user, UserDetail)

    def get_user_by_email(self, email: str) -> UserDetail:
        """Fetch a user by email or raise NotFoundError."""
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_user_repo(uow)
            user = repo.get_by_email(email)
            if user is None:
                raise errors.NotFoundError(f"User with email {email!r} not found")
            return mapping.to_schema(user, UserDetail)

    def get_user_summary(self, user_id: UUID) -> UserResponse:
        """
        Fetch a lightweight summary of a user.

        This is often enough for authentication/identity contexts.
        """
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_user_repo(uow)
            user = repo.get(user_id)
            if user is None:
                raise errors.NotFoundError(f"User {user_id} not found")
            return mapping.to_schema(user, UserResponse)

    # ------------------------------------------------------------------ #
    # Listing
    # ------------------------------------------------------------------ #
    def list_users(
        self,
        params: PaginationParams,
        *,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
    ) -> PaginatedResponse[UserListItem]:
        """
        List users with basic filtering and pagination.

        :param params: Pagination parameters
        :param role: optional UserRole filter
        :param is_active: optional active flag filter
        """
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_user_repo(uow)

            filters = {}
            if role is not None:
                filters["user_role"] = role
            if is_active is not None:
                filters["is_active"] = is_active

            records = repo.get_multi(
                skip=params.offset,
                limit=params.limit,
                filters=filters or None,
                order_by=[repo.model.created_at.desc()],  # type: ignore[attr-defined]
            )
            total = repo.count(filters=filters or None)

            return pagination.paginate(
                items=records,
                total_items=total,
                params=params,
                mapper=lambda u: mapping.to_schema(u, UserListItem),
            )

    # ------------------------------------------------------------------ #
    # Creation
    # ------------------------------------------------------------------ #
    def create_user(self, data: UserCreate) -> UserDetail:
        """
        Create a user record.

        WARNING: This method does NOT handle password hashing or verification.
        In most cases, registration should be done via a dedicated
        RegistrationService that also creates the appropriate role profile
        (Student, Visitor, Admin, Supervisor).
        """
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_user_repo(uow)

            # Enforce unique email/phone at service level (in addition to DB)
            existing_by_email = repo.get_by_email(data.email)
            if existing_by_email:
                raise errors.ConflictError(
                    f"User with email {data.email!r} already exists"
                )

            existing_by_phone = repo.get_by_phone(data.phone)
            if existing_by_phone:
                raise errors.ConflictError(
                    f"User with phone {data.phone!r} already exists"
                )

            # Prepare dict excluding password (handled by auth layer)
            payload = data.model_dump(exclude={"password"})
            user = repo.create(payload)  # type: ignore[arg-type]

            # Explicit commit to get ID and ensure persistence
            uow.commit()

            return mapping.to_schema(user, UserDetail)

    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #
    def update_user(self, user_id: UUID, data: UserUpdate) -> UserDetail:
        """
        Update user fields (admin or self-service).

        Handles uniqueness checks for email/phone when changed.
        """
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_user_repo(uow)
            user = repo.get(user_id)
            if user is None:
                raise errors.NotFoundError(f"User {user_id} not found")

            # Email/phone uniqueness checks only if changed
            if data.email is not None and data.email != user.email:
                if repo.get_by_email(data.email):
                    raise errors.ConflictError(
                        f"User with email {data.email!r} already exists"
                    )

            if data.phone is not None and data.phone != user.phone:
                if repo.get_by_phone(data.phone):
                    raise errors.ConflictError(
                        f"User with phone {data.phone!r} already exists"
                    )

            # Apply changes
            mapping.update_model_from_schema(user, data, exclude_fields=["id"])
            uow.session.flush()  # type: ignore[union-attr]

            uow.commit()
            return mapping.to_schema(user, UserDetail)

    # ------------------------------------------------------------------ #
    # State changes
    # ------------------------------------------------------------------ #
    def deactivate_user(self, user_id: UUID) -> UserResponse:
        """Soft-deactivate a user account."""
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_user_repo(uow)
            user = repo.get(user_id)
            if user is None:
                raise errors.NotFoundError(f"User {user_id} not found")

            user.is_active = False  # type: ignore[attr-defined]
            uow.session.flush()  # type: ignore[union-attr]
            uow.commit()
            return mapping.to_schema(user, UserResponse)

    def activate_user(self, user_id: UUID) -> UserResponse:
        """Reactivate a previously deactivated user account."""
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_user_repo(uow)
            user = repo.get(user_id)
            if user is None:
                raise errors.NotFoundError(f"User {user_id} not found")

            user.is_active = True  # type: ignore[attr-defined]
            uow.session.flush()  # type: ignore[union-attr]
            uow.commit()
            return mapping.to_schema(user, UserResponse)