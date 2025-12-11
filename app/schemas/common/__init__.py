# --- File: app/schemas/common/__init__.py ---
"""
Common schemas package.

This __init__ module re-exports frequently used base schemas, enums,
pagination helpers, responses, and filters from a single location:

    from app.schemas.common import BaseSchema, UserRole, PaginationParams
"""

from __future__ import annotations

from app.schemas.common.base import (
    BaseCreateSchema,
    BaseDBSchema,
    BaseFilterSchema,
    BaseResponseSchema,
    BaseSchema,
    BaseUpdateSchema,
    SoftDeleteMixin,
    TimestampMixin,
    UUIDMixin,
)
from app.schemas.common.enums import (
    AnnouncementCategory,
    AttendanceStatus,
    BillingCycle,
    BookingStatus,
    ComplaintCategory,
    ComplaintStatus,
    DietaryPreference,
    DeviceType,
    EmploymentType,
    Gender,
    IDProofType,
    InquiryStatus,
    MealType,
    MaintenanceCategory,
    MaintenanceStatus,
    NotificationStatus,
    NotificationType,
    PaymentMethod,
    PaymentStatus,
    PaymentType,
    Priority,
    ReferralStatus,
    ReviewStatus,
    RoomType,
    SearchSource,
    StudentStatus,
    SubscriptionPlan,
    SubscriptionStatus,
    SupervisorStatus,
    TargetAudience,
    UserRole,
)
from app.schemas.common.filters import (
    DateRangeFilter,
    DateTimeRangeFilter,
    PriceRangeFilter,
    SearchFilter,
    SortOptions,
    StatusFilter,
)
from app.schemas.common.pagination import (
    PaginatedResponse,
    PaginationMeta,
    PaginationParams,
)
from app.schemas.common.response import (
    BulkOperationResponse,
    ErrorDetail,
    ErrorResponse,
    MessageResponse,
    SuccessResponse,
)

__all__ = [
    # Base schemas
    "BaseSchema",
    "BaseCreateSchema",
    "BaseUpdateSchema",
    "BaseResponseSchema",
    "BaseDBSchema",
    "BaseFilterSchema",
    "TimestampMixin",
    "SoftDeleteMixin",
    "UUIDMixin",
    # Enums
    "UserRole",
    "Gender",
    "RoomType",
    "BookingStatus",
    "PaymentStatus",
    "PaymentMethod",
    "PaymentType",
    "ComplaintCategory",
    "ComplaintStatus",
    "Priority",
    "AttendanceStatus",
    "MaintenanceCategory",
    "MaintenanceStatus",
    "NotificationType",
    "SubscriptionPlan",
    "StudentStatus",
    "SupervisorStatus",
    "AnnouncementCategory",
    "TargetAudience",
    "MealType",
    "DietaryPreference",
    "IDProofType",
    "EmploymentType",
    "BillingCycle",
    "SubscriptionStatus",
    "ReferralStatus",
    "ReviewStatus",
    "NotificationStatus",
    "DeviceType",
    "SearchSource",
    "InquiryStatus",
    # Pagination
    "PaginationParams",
    "PaginationMeta",
    "PaginatedResponse",
    # Responses
    "SuccessResponse",
    "ErrorDetail",
    "ErrorResponse",
    "MessageResponse",
    "BulkOperationResponse",
    # Filters
    "DateRangeFilter",
    "DateTimeRangeFilter",
    "PriceRangeFilter",
    "SearchFilter",
    "SortOptions",
    "StatusFilter",
]