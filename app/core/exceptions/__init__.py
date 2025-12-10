"""
Core exceptions module for the hostel management system.
Provides a comprehensive hierarchy of custom exceptions for different error scenarios.
"""

from .base import (
    BaseAPIException,
    BaseBusinessException,
    BaseValidationException
)

from .auth_exceptions import (
    AuthenticationException,
    InvalidCredentialsException,
    TokenExpiredException,
    InvalidTokenException,
    UserNotActiveException,
    EmailNotVerifiedException,
    AccountLockedException,
    PasswordExpiredException,
    TwoFactorRequiredException,
    InvalidOTPException,
    SessionExpiredException,
    RefreshTokenExpiredException
)

from .permission_exceptions import (
    PermissionDeniedException,
    InsufficientPermissionsException,
    UnauthorizedAccessException,
    HostelAccessDeniedException,
    SupervisorScopeException,
    RoleNotAssignedException,
    ResourceAccessDeniedException,
    ApprovalRequiredException,
    HierarchicalAccessException,
    TenantAccessDeniedException
)

from .validation_exceptions import (
    ValidationException,
    InvalidInputException,
    DataIntegrityException,
    DuplicateEntryException,
    InvalidDateRangeException,
    RequiredFieldException,
    InvalidFormatException,
    ValueOutOfRangeException,
    InvalidEnumValueException,
    FileValidationException,
    SchemaValidationException
)

from .business_exceptions import (
    BusinessRuleException,
    BookingException,
    PaymentException,
    ComplaintException,
    MaintenanceException,
    AvailabilityException,
    CapacityExceededException,
    BookingConflictException,
    PaymentFailedException,
    RefundException,
    CheckInException,
    CheckOutException,
    RoomAllocationException,
    PricingException,
    DiscountException,
    CancellationException
)

from .resource_exceptions import (
    ResourceNotFoundException,
    HostelNotFoundException,
    RoomNotFoundException,
    StudentNotFoundException,
    BookingNotFoundException,
    PaymentNotFoundException,
    ComplaintNotFoundException,
    MaintenanceRequestNotFoundException,
    UserNotFoundException,
    SupervisorNotFoundException,
    AdminNotFoundException,
    DocumentNotFoundException,
    InvoiceNotFoundException
)

from .http_exceptions import (
    BadRequestException,
    NotFoundException,
    ForbiddenException,
    UnauthorizedException,
    ConflictException,
    InternalServerException,
    ServiceUnavailableException,
    TooManyRequestsException,
    UnprocessableEntityException,
    PreconditionFailedException,
    RequestTimeoutException,
    PayloadTooLargeException
)

from .external_service_exceptions import (
    ExternalServiceException,
    PaymentGatewayException,
    EmailServiceException,
    SMSServiceException,
    StorageServiceException,
    NotificationServiceException,
    GeolocationServiceException,
    ThirdPartyAPIException
)

from .system_exceptions import (
    SystemException,
    DatabaseException,
    CacheException,
    ConfigurationException,
    DependencyException,
    InitializationException,
    ShutdownException,
    ResourceExhaustedException,
    TimeoutException,
    ConnectionException
)

__all__ = [
    # Base exceptions
    'BaseAPIException',
    'BaseBusinessException', 
    'BaseValidationException',
    
    # Authentication exceptions
    'AuthenticationException',
    'InvalidCredentialsException',
    'TokenExpiredException',
    'InvalidTokenException',
    'UserNotActiveException',
    'EmailNotVerifiedException',
    'AccountLockedException',
    'PasswordExpiredException',
    'TwoFactorRequiredException',
    'InvalidOTPException',
    'SessionExpiredException',
    'RefreshTokenExpiredException',
    
    # Permission exceptions
    'PermissionDeniedException',
    'InsufficientPermissionsException',
    'UnauthorizedAccessException',
    'HostelAccessDeniedException',
    'SupervisorScopeException',
    'RoleNotAssignedException',
    'ResourceAccessDeniedException',
    'ApprovalRequiredException',
    'HierarchicalAccessException',
    'TenantAccessDeniedException',
    
    # Validation exceptions
    'ValidationException',
    'InvalidInputException',
    'DataIntegrityException',
    'DuplicateEntryException',
    'InvalidDateRangeException',
    'RequiredFieldException',
    'InvalidFormatException',
    'ValueOutOfRangeException',
    'InvalidEnumValueException',
    'FileValidationException',
    'SchemaValidationException',
    
    # Business exceptions
    'BusinessRuleException',
    'BookingException',
    'PaymentException',
    'ComplaintException',
    'MaintenanceException',
    'AvailabilityException',
    'CapacityExceededException',
    'BookingConflictException',
    'PaymentFailedException',
    'RefundException',
    'CheckInException',
    'CheckOutException',
    'RoomAllocationException',
    'PricingException',
    'DiscountException',
    'CancellationException',
    
    # Resource exceptions
    'ResourceNotFoundException',
    'HostelNotFoundException',
    'RoomNotFoundException',
    'StudentNotFoundException',
    'BookingNotFoundException',
    'PaymentNotFoundException',
    'ComplaintNotFoundException',
    'MaintenanceRequestNotFoundException',
    'UserNotFoundException',
    'SupervisorNotFoundException',
    'AdminNotFoundException',
    'DocumentNotFoundException',
    'InvoiceNotFoundException',
    
    # HTTP exceptions
    'BadRequestException',
    'NotFoundException',
    'ForbiddenException',
    'UnauthorizedException',
    'ConflictException',
    'InternalServerException',
    'ServiceUnavailableException',
    'TooManyRequestsException',
    'UnprocessableEntityException',
    'PreconditionFailedException',
    'RequestTimeoutException',
    'PayloadTooLargeException',
    
    # External service exceptions
    'ExternalServiceException',
    'PaymentGatewayException',
    'EmailServiceException',
    'SMSServiceException',
    'StorageServiceException',
    'NotificationServiceException',
    'GeolocationServiceException',
    'ThirdPartyAPIException',
    
    # System exceptions
    'SystemException',
    'DatabaseException',
    'CacheException',
    'ConfigurationException',
    'DependencyException',
    'InitializationException',
    'ShutdownException',
    'ResourceExhaustedException',
    'TimeoutException',
    'ConnectionException'
]