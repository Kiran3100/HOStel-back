"""
Hostel admin view schemas
"""
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseUpdateSchema
from app.schemas.common.enums import HostelStatus, SubscriptionPlan


class HostelAdminView(BaseSchema):
    """Hostel view for administrators"""
    id: UUID
    name: str
    slug: str
    
    # Status
    status: HostelStatus
    is_active: bool
    is_public: bool
    is_featured: bool
    is_verified: bool
    
    # Stats
    total_rooms: int
    total_beds: int
    occupied_beds: int
    available_beds: int
    occupancy_percentage: Decimal
    
    # Students
    total_students: int
    active_students: int
    
    # Financial
    total_revenue_this_month: Decimal
    outstanding_payments: Decimal
    
    # Pending items
    pending_bookings: int
    pending_complaints: int
    pending_maintenance: int
    
    # Subscription
    subscription_plan: Optional[SubscriptionPlan]
    subscription_expires_at: Optional[datetime]
    
    # Performance
    average_rating: Decimal
    total_reviews: int


class HostelSettings(BaseUpdateSchema):
    """Hostel configuration settings"""
    # Visibility
    is_public: Optional[bool] = Field(None, description="Public listing visibility")
    is_active: Optional[bool] = Field(None, description="Hostel active status")
    
    # Booking settings
    auto_approve_bookings: bool = Field(False, description="Auto-approve booking requests")
    booking_advance_percentage: Decimal = Field(
        Decimal("20.00"),
        ge=0,
        le=100,
        description="Advance payment percentage"
    )
    max_booking_duration_months: int = Field(12, ge=1, le=24, description="Max booking duration")
    
    # Payment settings
    payment_due_day: int = Field(5, ge=1, le=28, description="Monthly payment due day")
    late_payment_grace_days: int = Field(3, ge=0, le=10, description="Grace period for late payments")
    
    # Attendance settings
    enable_attendance_tracking: bool = Field(True, description="Enable attendance system")
    minimum_attendance_percentage: Decimal = Field(
        Decimal("75.00"),
        ge=0,
        le=100,
        description="Minimum required attendance %"
    )
    
    # Notification settings
    notify_on_booking: bool = Field(True, description="Notify on new bookings")
    notify_on_complaint: bool = Field(True, description="Notify on complaints")
    notify_on_payment: bool = Field(True, description="Notify on payments")
    
    # Mess settings
    mess_included: bool = Field(False, description="Mess facility included")
    mess_charges_monthly: Optional[Decimal] = Field(None, ge=0, description="Monthly mess charges")


class HostelVisibilityUpdate(BaseUpdateSchema):
    """Update hostel visibility settings"""
    is_public: bool = Field(..., description="Make hostel publicly visible")
    is_featured: bool = Field(False, description="Feature hostel in search results")


class HostelCapacityUpdate(BaseUpdateSchema):
    """Update hostel capacity (admin only)"""
    total_rooms: int = Field(..., ge=1, description="Total number of rooms")
    total_beds: int = Field(..., ge=1, description="Total number of beds")


class HostelStatusUpdate(BaseUpdateSchema):
    """Update hostel operational status"""
    status: HostelStatus = Field(..., description="Hostel status")
    is_active: bool = Field(..., description="Active status")
    reason: Optional[str] = Field(None, description="Reason for status change")