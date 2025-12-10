# app/services/common/pagination.py
from __future__ import annotations

from typing import Callable, Iterable, List, Sequence, TypeVar

from app.schemas.common.base import BaseSchema
from app.schemas.common.pagination import (
    PaginationParams,
    PaginatedResponse,
)

TModel = TypeVar("TModel")
TSchema = TypeVar("TSchema", bound=BaseSchema)


def paginate(
    *,
    items: Sequence[TModel],
    total_items: int,
    params: PaginationParams,
    mapper: Callable[[TModel], TSchema],
) -> PaginatedResponse[TSchema]:
    """
    Build a PaginatedResponse from a list of models and total count.

    :param items: Current page of ORM objects
    :param total_items: Total count across all pages
    :param params: PaginationParams
    :param mapper: Function mapping model -> schema
    """
    schema_items: List[TSchema] = [mapper(item) for item in items]
    return PaginatedResponse[TSchema].create(
        items=schema_items,
        total_items=total_items,
        page=params.page,
        page_size=params.page_size,
    )