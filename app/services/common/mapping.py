# app/services/common/mapping.py
from __future__ import annotations

from typing import Any, Iterable, List, Sequence, Type, TypeVar

from pydantic import BaseModel

TModel = TypeVar("TModel")
TSchema = TypeVar("TSchema", bound=BaseModel)


def to_schema(obj: TModel, schema_cls: Type[TSchema]) -> TSchema:
    """
    Convert an ORM model (or any attribute-based object) to a Pydantic schema.

    Assumes your BaseSchema has model_config.from_attributes = True (already set).
    """
    if obj is None:
        raise ValueError("to_schema() received None")
    return schema_cls.model_validate(obj)


def to_schema_list(objs: Iterable[TModel], schema_cls: Type[TSchema]) -> List[TSchema]:
    """Convert an iterable of models to a list of schemas."""
    return [schema_cls.model_validate(o) for o in objs]


def update_model_from_schema(
    model_obj: Any,
    schema_obj: BaseModel,
    *,
    exclude_unset: bool = True,
    exclude_fields: Sequence[str] | None = None,
) -> Any:
    """
    Apply fields from a Pydantic schema object to an ORM model.

    Typical usage:
        update_model_from_schema(db_user, user_update_schema, exclude_fields=["id"])
    """
    data = schema_obj.model_dump(exclude_unset=exclude_unset)
    if exclude_fields:
        for field in exclude_fields:
            data.pop(field, None)

    for field_name, value in data.items():
        if hasattr(model_obj, field_name):
            setattr(model_obj, field_name, value)

    return model_obj