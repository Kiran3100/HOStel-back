# app/core/pagination.py
from __future__ import annotations

from typing import Sequence, Callable, TypeVar, List

from app.core.constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from app.schemas.common.pagination import PaginationParams, PaginatedResponse
from app.schemas.common.base import BaseSchema

TModel = TypeVar("TModel")
TSchema = TypeVar("TSchema", bound=BaseSchema)


def normalize_pagination(
    page: int | None,
    page_size: int | None,
) -> PaginationParams:
    """
    Normalize raw page & page_size inputs into a PaginationParams object
    with sane defaults and clamped max page size.
    """
    if page is None or page < 1:
        page = DEFAULT_PAGE

    if page_size is None or page_size < 1:
        page_size = DEFAULT_PAGE_SIZE

    if page_size > MAX_PAGE_SIZE:
        page_size = MAX_PAGE_SIZE

    return PaginationParams(page=page, page_size=page_size)


def paginate_items(
    *,
    items: Sequence[TModel],
    total_items: int,
    params: PaginationParams,
    mapper: Callable[[TModel], TSchema],
) -> PaginatedResponse[TSchema]:
    """
    Map and wrap items into a PaginatedResponse using the same semantics
    as app.services.common.pagination, but exposed from core.
    """
    mapped: List[TSchema] = [mapper(obj) for obj in items]
    return PaginatedResponse[TSchema].create(
        items=mapped,
        total_items=total_items,
        page=params.page,
        page_size=params.page_size,
    )