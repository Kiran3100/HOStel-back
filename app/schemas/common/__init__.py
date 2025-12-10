"""
Common schemas package
"""
from app.schemas.common.base import (
    BaseSchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseResponseSchema,
    BaseDBSchema,
    TimestampMixin,
    SoftDeleteMixin,
    UUIDMixin
)
from app.schemas.common.enums import (
    UserRole,
    Gender,
    HostelType,
    RoomType,
    BookingStatus,
    PaymentStatus,
    PaymentMethod,
    PaymentType,
    ComplaintCategory,
    ComplaintStatus,
    Priority,
    AttendanceStatus,
    LeaveType,
    MaintenanceCategory,
    MaintenanceStatus,
    NotificationType,
    SubscriptionPlan,
    StudentStatus,
    SupervisorStatus,
    AnnouncementCategory,
    TargetAudience,
    MealType,
    DietaryPreference,
    IDProofType,
    EmploymentType,
    BillingCycle,
    SubscriptionStatus,
    ReferralStatus,
    ReviewStatus,
    NotificationStatus,
    DeviceType,
    SearchSource,
    InquiryStatus
)
from app.schemas.common.pagination import (
    PaginationParams,
    PaginationMeta,
    PaginatedResponse
)
from app.schemas.common.response import (
    SuccessResponse,
    ErrorDetail,
    ErrorResponse,
    MessageResponse,
    BulkOperationResponse
)
from app.schemas.common.filters import (
    DateRangeFilter,
    DateTimeRangeFilter,
    PriceRangeFilter,
    SearchFilter,
    SortOptions,
    StatusFilter
)

__all__ = [
    # Base schemas
    "BaseSchema",
    "BaseCreateSchema",
    "BaseUpdateSchema",
    "BaseResponseSchema",
    "BaseDBSchema",
    "TimestampMixin",
    "SoftDeleteMixin",
    "UUIDMixin",
    
    # Enums
    "UserRole",
    "Gender",
    "HostelType",
    "RoomType",
    "BookingStatus",
    "PaymentStatus",
    "PaymentMethod",
    "PaymentType",
    "ComplaintCategory",
    "ComplaintStatus",
    "Priority",
    "AttendanceStatus",
    "LeaveType",
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