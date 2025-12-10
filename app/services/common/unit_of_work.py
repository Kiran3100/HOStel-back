# app/services/common/unit_of_work.py
from __future__ import annotations

from contextlib import AbstractContextManager
from typing import Callable, Generic, TypeVar

from sqlalchemy.orm import Session

from app.repositories.base import BaseRepository

TRepository = TypeVar("TRepository", bound=BaseRepository)


class UnitOfWork(AbstractContextManager["UnitOfWork"]):
    """
    Simple Unit of Work abstraction over a SQLAlchemy Session.

    Usage:
        uow = UnitOfWork(session_factory)
        with uow as tx:
            user_repo = tx.get_repo(UserRepository)
            user = user_repo.get(user_id)
            ...
            tx.commit()  # optional; auto-commits if no exception
    """

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory
        self.session: Session | None = None
        self._committed: bool = False

    # ------------------------------------------------------------------ #
    # Context manager protocol
    # ------------------------------------------------------------------ #
    def __enter__(self) -> "UnitOfWork":
        self.session = self._session_factory()
        self._committed = False
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if self.session is None:
            return False

        try:
            if exc_type is None:
                # Commit if we haven't already committed manually
                if not self._committed:
                    self.session.commit()
            else:
                # Roll back on error
                self.session.rollback()
        finally:
            self.session.close()
            self.session = None

        # Propagate any exception
        return False

    # ------------------------------------------------------------------ #
    # Transaction helpers
    # ------------------------------------------------------------------ #
    def commit(self) -> None:
        """Explicitly commit current transaction."""
        if self.session is None:
            raise RuntimeError("UnitOfWork.commit() called outside of context")
        self.session.commit()
        self._committed = True

    def rollback(self) -> None:
        """Explicitly roll back current transaction."""
        if self.session is None:
            raise RuntimeError("UnitOfWork.rollback() called outside of context")
        self.session.rollback()
        self._committed = False

    # ------------------------------------------------------------------ #
    # Repository factory
    # ------------------------------------------------------------------ #
    def get_repo(self, repo_cls: type[TRepository]) -> TRepository:
        """
        Instantiate a repository bound to this UnitOfWork's Session.

        Example:
            with UnitOfWork(SessionLocal) as uow:
                user_repo = uow.get_repo(UserRepository)
        """
        if self.session is None:
            raise RuntimeError("UnitOfWork.get_repo() called outside of context")
        return repo_cls(self.session)