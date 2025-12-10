"""
Booking schemas package
"""
from app.schemas.booking.booking_base import (
    BookingBase,
    BookingCreate,
    BookingUpdate
)
from app.schemas.booking.booking_response import (
    BookingResponse,
    BookingDetail,
    BookingListItem
)
from app.schemas.booking.booking_request import (
    BookingRequest,
    GuestInformation,
    BookingInquiry
)
from app.schemas.booking.booking_approval import (
    BookingApprovalRequest,
    ApprovalResponse,
    RejectionRequest
)
from app.schemas.booking.booking_calendar import (
    CalendarView,
    CalendarEvent,
    AvailabilityCalendar,
    DayBookings
)
from app.schemas.booking.booking_assignment import (
    RoomAssignment,
    BedAssignment,
    AssignmentRequest
)
from app.schemas.booking.booking_cancellation import (
    CancellationRequest,
    CancellationResponse,
    RefundCalculation
)
from app.schemas.booking.booking_modification import (
    ModificationRequest,
    ModificationResponse,
    DateChangeRequest
)
from app.schemas.booking.booking_waitlist import (
    WaitlistRequest,
    WaitlistResponse,
    WaitlistStatus,
    WaitlistNotification
)
from app.schemas.booking.booking_conversion import (
    ConvertToStudentRequest,
    ConversionResponse,
    ConversionChecklist
)
from app.schemas.booking.booking_filters import (
    BookingFilterParams,
    BookingSearchRequest,
    BookingSortOptions
)

__all__ = [
    # Base
    "BookingBase",
    "BookingCreate",
    "BookingUpdate",
    
    # Response
    "BookingResponse",
    "BookingDetail",
    "BookingListItem",
    
    # Request
    "BookingRequest",
    "GuestInformation",
    "BookingInquiry",
    
    # Approval
    "BookingApprovalRequest",
    "ApprovalResponse",
    "RejectionRequest",
    
    # Calendar
    "CalendarView",
    "CalendarEvent",
    "AvailabilityCalendar",
    "DayBookings",
    
    # Assignment
    "RoomAssignment",
    "BedAssignment",
    "AssignmentRequest",
    
    # Cancellation
    "CancellationRequest",
    "CancellationResponse",
    "RefundCalculation",
    
    # Modification
    "ModificationRequest",
    "ModificationResponse",
    "DateChangeRequest",
    
    # Waitlist
    "WaitlistRequest",
    "WaitlistResponse",
    "WaitlistStatus",
    "WaitlistNotification",
    
    # Conversion
    "ConvertToStudentRequest",
    "ConversionResponse",
    "ConversionChecklist",
    
    # Filters
    "BookingFilterParams",
    "BookingSearchRequest",
    "BookingSortOptions",
]