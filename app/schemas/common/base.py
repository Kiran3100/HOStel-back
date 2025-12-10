"""
Base schema classes with common fields and configurations
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID


class BaseSchema(BaseModel):
    """Base schema with common Pydantic configuration"""
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=False,  # Keep enums as enum objects
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
        }
    )


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields"""
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class SoftDeleteMixin(BaseModel):
    """Mixin for soft delete support"""
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp")
    is_deleted: bool = Field(False, description="Soft delete flag")


class UUIDMixin(BaseModel):
    """Mixin for UUID primary key"""
    id: UUID = Field(..., description="Unique identifier")


class BaseDBSchema(BaseSchema, UUIDMixin, TimestampMixin):
    """Base schema for database entities with ID and timestamps"""
    pass


class BaseCreateSchema(BaseSchema):
    """Base schema for create operations"""
    pass


class BaseUpdateSchema(BaseSchema):
    """Base schema for update operations (all fields optional)"""
    pass


class BaseResponseSchema(BaseDBSchema):
    """Base schema for API responses"""
    pass


class BaseFilterSchema(BaseSchema):
    """Base schema for filter parameters"""
    pass