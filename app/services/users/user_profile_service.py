# app/services/users/user_profile_service.py
from __future__ import annotations

from typing import Callable
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.core import UserRepository
from app.schemas.user import (
    ProfileUpdate,
    ProfileImageUpdate,
    ContactInfoUpdate,
    UserDetail,
)
from app.services.common import UnitOfWork, mapping, errors


class UserProfileService:
    """
    User profile-related operations.

    This service focuses on fields that are logically part of the User entity
    (name, contact, profile image, basic profile info).

    Note: Some fields in ProfileUpdate (e.g., address_line1, pincode) do not
    exist on the current User model; those will be silently ignored by the
    generic mapping helper. To persist them, the data model would need to be
    extended.
    """

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory

    def _get_user_repo(self, uow: UnitOfWork) -> UserRepository:
        return uow.get_repo(UserRepository)

    # ------------------------------------------------------------------ #
    # Profile update
    # ------------------------------------------------------------------ #
    def update_profile(self, user_id: UUID, data: ProfileUpdate) -> UserDetail:
        """
        Update basic profile fields (name, gender, DOB, and any supported
        contact/address fields that exist on the User model).
        """
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_user_repo(uow)
            user = repo.get(user_id)
            if user is None:
                raise errors.NotFoundError(f"User {user_id} not found")

            mapping.update_model_from_schema(user, data, exclude_fields=["id"])
            uow.session.flush()  # type: ignore[union-attr]
            uow.commit()
            return mapping.to_schema(user, UserDetail)

    def update_profile_image(self, user_id: UUID, data: ProfileImageUpdate) -> UserDetail:
        """
        Update the user's profile image URL.
        """
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_user_repo(uow)
            user = repo.get(user_id)
            if user is None:
                raise errors.NotFoundError(f"User {user_id} not found")

            user.profile_image_url = str(data.profile_image_url)  # type: ignore[attr-defined]
            uow.session.flush()  # type: ignore[union-attr]
            uow.commit()
            return mapping.to_schema(user, UserDetail)

    def update_contact_info(self, user_id: UUID, data: ContactInfoUpdate) -> UserDetail:
        """
        Update phone/email and emergency contact information.

        For phone/email, uniqueness checks should be done at a higher level
        (e.g., via UserService.update_user). This method assumes those have
        already been validated if necessary.
        """
        with UnitOfWork(self._session_factory) as uow:
            repo = self._get_user_repo(uow)
            user = repo.get(user_id)
            if user is None:
                raise errors.NotFoundError(f"User {user_id} not found")

            mapping.update_model_from_schema(user, data, exclude_fields=["id"])
            uow.session.flush()  # type: ignore[union-attr]
            uow.commit()
            return mapping.to_schema(user, UserDetail)