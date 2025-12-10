# app/core/database.py
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.constants import ENV_DATABASE_URL
from app.models.base import Base


# ------------------------------------------------------------------ #
# Engine & Session
# ------------------------------------------------------------------ #
DATABASE_URL = os.getenv(ENV_DATABASE_URL, "sqlite:///./app.db")

engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=False,          # set True for SQL echo in development
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI-friendly dependency for DB session:

        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()

    Here we export get_session directly.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Iterator[Session]:
    """
    Context manager for scripts / CLIs / background tasks:

        with session_scope() as session:
            ...

    Commits on success, rollbacks on error.
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    """
    Simple helper to create all tables.

    In production, prefer Alembic migrations instead of this.
    """
    Base.metadata.create_all(bind=engine)