# --- File: app/schemas/inquiry/inquiry_response.py ---
"""
Inquiry response schemas for API responses.

<<<<<<< Updated upstream
This module defines response schemas for inquiry data including
basic responses, detailed information, and list items.
=======
This module defines response schemas with varying levels of detail
for different use cases (list views, detail views, etc.).
>>>>>>> Stashed changes
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import Field, computed_field

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import InquirySource, InquiryStatus, RoomType

__all__ = [
    "InquiryResponse",
    "InquiryDetail",
    "InquiryListItem",
    "InquiryStats",
<<<<<<< Updated upstream
=======
    "InquiryConversionInfo",
    "HostelInquirySummary",
>>>>>>> Stashed changes
]


class InquiryResponse(BaseResponseSchema):
    """
    Standard inquiry response schema.
    
<<<<<<< Updated upstream
    Contains core inquiry information for API responses.
    """

    hostel_id: UUID = Field(
        ...,
        description="Hostel identifier",
    )
    hostel_name: str = Field(
        ...,
        description="Name of the hostel",
    )

    # Visitor Information
    visitor_name: str = Field(
        ...,
        description="Visitor full name",
    )
    visitor_email: str = Field(
        ...,
        description="Visitor email",
    )
    visitor_phone: str = Field(
        ...,
        description="Visitor phone",
    )

    # Preferences
=======
    Used for basic inquiry information display after creation
    or simple fetch operations.
    """
    
    # Hostel reference
    hostel_id: UUID = Field(
        ...,
        description="UUID of the associated hostel",
    )
    hostel_name: str = Field(
        ...,
        description="Name of the associated hostel",
    )
    
    # Visitor information
    visitor_name: str = Field(
        ...,
        description="Full name of the visitor",
    )
    visitor_email: str = Field(
        ...,
        description="Visitor's email address",
    )
    visitor_phone: str = Field(
        ...,
        description="Visitor's phone number",
    )
    
    # Stay preferences
>>>>>>> Stashed changes
    preferred_check_in_date: Optional[date] = Field(
        None,
        description="Preferred check-in date",
    )
    stay_duration_months: Optional[int] = Field(
        None,
<<<<<<< Updated upstream
        description="Intended stay duration",
    )
    room_type_preference: Optional[RoomType] = Field(
        None,
        description="Room type preference",
    )

    # Status
=======
        description="Expected stay duration in months",
    )
    room_type_preference: Optional[RoomType] = Field(
        None,
        description="Preferred room type",
    )
    
    # Status and tracking
>>>>>>> Stashed changes
    status: InquiryStatus = Field(
        ...,
        description="Current inquiry status",
    )
<<<<<<< Updated upstream

    created_at: datetime = Field(
        ...,
        description="When inquiry was created",
    )

    @computed_field
    @property
    def age_days(self) -> int:
        """Calculate age of inquiry in days."""
        return (datetime.utcnow() - self.created_at).days

    @computed_field
    @property
    def is_new(self) -> bool:
        """Check if inquiry is new (less than 24 hours old)."""
        return self.age_days < 1

    @computed_field
    @property
    def is_stale(self) -> bool:
        """Check if inquiry is stale (older than 7 days without contact)."""
        return self.age_days > 7 and self.status == InquiryStatus.NEW

    @computed_field
    @property
    def urgency_level(self) -> str:
        """
        Determine urgency level.
        
        Returns: "high", "medium", or "low"
        """
        if self.status == InquiryStatus.NEW and self.age_days < 1:
            return "high"
        elif self.status == InquiryStatus.NEW and self.age_days < 3:
            return "medium"
        else:
            return "low"
=======
    inquiry_source: InquirySource = Field(
        ...,
        description="Source of the inquiry",
    )
    
    @computed_field
    @property
    def is_actionable(self) -> bool:
        """Check if inquiry requires action (new or contacted)."""
        return self.status in {
            InquiryStatus.NEW,
            InquiryStatus.CONTACTED,
            InquiryStatus.INTERESTED,
        }
    
    @computed_field
    @property
    def days_since_inquiry(self) -> int:
        """Calculate days since inquiry was created."""
        return (datetime.utcnow() - self.created_at).days
>>>>>>> Stashed changes


class InquiryDetail(BaseResponseSchema):
    """
<<<<<<< Updated upstream
    Detailed inquiry information.
    
    Contains complete inquiry details including contact history,
    notes, and assignment information.
    """

    hostel_id: UUID = Field(
        ...,
        description="Hostel identifier",
    )
    hostel_name: str = Field(
        ...,
        description="Hostel name",
    )

    # Visitor Information
    visitor_name: str = Field(
        ...,
        description="Visitor name",
    )
    visitor_email: str = Field(
        ...,
        description="Visitor email",
    )
    visitor_phone: str = Field(
        ...,
        description="Visitor phone",
    )

    # Preferences
=======
    Detailed inquiry view with complete information.
    
    Used for individual inquiry detail pages and admin views
    with full audit and interaction history.
    """
    
    # Hostel reference
    hostel_id: UUID = Field(
        ...,
        description="UUID of the associated hostel",
    )
    hostel_name: str = Field(
        ...,
        description="Name of the associated hostel",
    )
    
    # Visitor information
    visitor_name: str = Field(
        ...,
        description="Full name of the visitor",
    )
    visitor_email: str = Field(
        ...,
        description="Visitor's email address",
    )
    visitor_phone: str = Field(
        ...,
        description="Visitor's phone number",
    )
    
    # Stay preferences
>>>>>>> Stashed changes
    preferred_check_in_date: Optional[date] = Field(
        None,
        description="Preferred check-in date",
    )
    stay_duration_months: Optional[int] = Field(
        None,
<<<<<<< Updated upstream
        description="Stay duration in months",
    )
    room_type_preference: Optional[RoomType] = Field(
        None,
        description="Room type preference",
    )

    # Inquiry Details
    message: Optional[str] = Field(
        None,
        description="Visitor's message or questions",
    )

    # Metadata
=======
        description="Expected stay duration in months",
    )
    room_type_preference: Optional[RoomType] = Field(
        None,
        description="Preferred room type",
    )
    
    # Inquiry details
    message: Optional[str] = Field(
        None,
        description="Additional message from visitor",
    )
>>>>>>> Stashed changes
    inquiry_source: InquirySource = Field(
        ...,
        description="Source of the inquiry",
    )
    status: InquiryStatus = Field(
        ...,
<<<<<<< Updated upstream
        description="Current status",
    )

    # Contact/Follow-up Information
    contacted_by: Optional[UUID] = Field(
        None,
        description="Admin who contacted the visitor",
    )
    contacted_by_name: Optional[str] = Field(
        None,
        description="Name of admin who made contact",
    )
    contacted_at: Optional[datetime] = Field(
        None,
        description="When visitor was contacted",
    )

    # Assignment Information
    assigned_to: Optional[UUID] = Field(
        None,
        description="Admin assigned to handle this inquiry",
    )
    assigned_to_name: Optional[str] = Field(
        None,
        description="Name of assigned admin",
    )
    assigned_at: Optional[datetime] = Field(
        None,
        description="When inquiry was assigned",
    )

    # Internal Notes
    notes: Optional[str] = Field(
        None,
        description="Internal notes about this inquiry",
    )

    # Timestamps
    created_at: datetime = Field(
        ...,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp",
    )

    @computed_field
    @property
    def age_days(self) -> int:
        """Calculate inquiry age in days."""
        return (datetime.utcnow() - self.created_at).days

    @computed_field
    @property
    def has_been_contacted(self) -> bool:
        """Check if visitor has been contacted."""
        return self.contacted_at is not None

    @computed_field
    @property
    def is_assigned(self) -> bool:
        """Check if inquiry has been assigned to someone."""
        return self.assigned_to is not None

    @computed_field
    @property
    def response_time_hours(self) -> Optional[float]:
        """Calculate response time in hours if contacted."""
        if self.contacted_at is None:
            return None
        
        delta = self.contacted_at - self.created_at
        return round(delta.total_seconds() / 3600, 2)

    @computed_field
    @property
    def days_since_contact(self) -> Optional[int]:
        """Calculate days since last contact."""
        if self.contacted_at is None:
            return None
        
        return (datetime.utcnow() - self.contacted_at).days
=======
        description="Current inquiry status",
    )
    
    # Contact tracking
    contacted_by: Optional[UUID] = Field(
        None,
        description="UUID of user who contacted the visitor",
    )
    contacted_by_name: Optional[str] = Field(
        None,
        description="Name of user who contacted the visitor",
    )
    contacted_at: Optional[datetime] = Field(
        None,
        description="Timestamp of first contact",
    )
    contact_method: Optional[str] = Field(
        None,
        description="Method used for contact",
    )
    
    # Assignment tracking
    assigned_to: Optional[UUID] = Field(
        None,
        description="UUID of assigned staff member",
    )
    assigned_to_name: Optional[str] = Field(
        None,
        description="Name of assigned staff member",
    )
    assigned_at: Optional[datetime] = Field(
        None,
        description="Timestamp of assignment",
    )
    
    # Follow-up tracking
    follow_up_required: bool = Field(
        False,
        description="Whether follow-up is required",
    )
    follow_up_date: Optional[date] = Field(
        None,
        description="Scheduled follow-up date",
    )
    
    # Internal notes
    notes: Optional[str] = Field(
        None,
        description="Internal notes about the inquiry",
    )
    
    # Conversion tracking
    converted_to_booking: bool = Field(
        False,
        description="Whether inquiry converted to booking",
    )
    booking_id: Optional[UUID] = Field(
        None,
        description="Associated booking ID if converted",
    )
    converted_at: Optional[datetime] = Field(
        None,
        description="Timestamp of conversion",
    )
    
    # Marketing tracking
    referral_code: Optional[str] = Field(
        None,
        description="Referral code used",
    )
    utm_source: Optional[str] = Field(
        None,
        description="UTM source parameter",
    )
    utm_medium: Optional[str] = Field(
        None,
        description="UTM medium parameter",
    )
    utm_campaign: Optional[str] = Field(
        None,
        description="UTM campaign parameter",
    )
    
    @computed_field
    @property
    def is_stale(self) -> bool:
        """
        Check if inquiry is stale (no action for 7+ days).
        
        Stale inquiries may need priority attention.
        """
        if self.status in {
            InquiryStatus.CONVERTED,
            InquiryStatus.NOT_INTERESTED,
        }:
            return False
        
        days_old = (datetime.utcnow() - self.updated_at).days
        return days_old >= 7
    
    @computed_field
    @property
    def response_time_hours(self) -> Optional[float]:
        """Calculate response time in hours (if contacted)."""
        if self.contacted_at:
            delta = self.contacted_at - self.created_at
            return round(delta.total_seconds() / 3600, 2)
        return None
    
    @computed_field
    @property
    def is_follow_up_due(self) -> bool:
        """Check if follow-up is due today or overdue."""
        if self.follow_up_required and self.follow_up_date:
            return self.follow_up_date <= date.today()
        return False
>>>>>>> Stashed changes


class InquiryListItem(BaseSchema):
    """
<<<<<<< Updated upstream
    Inquiry list item for summary views.
    
    Optimized schema for displaying multiple inquiries
    with essential information only.
    """

    id: UUID = Field(
        ...,
        description="Inquiry ID",
    )
    hostel_name: str = Field(
        ...,
        description="Hostel name",
    )
    visitor_name: str = Field(
        ...,
        description="Visitor name",
    )
    visitor_phone: str = Field(
        ...,
        description="Visitor phone",
    )

=======
    Lightweight inquiry schema for list views.
    
    Optimized for displaying inquiries in tables and lists
    with minimal data transfer.
    """
    
    id: UUID = Field(
        ...,
        description="Inquiry UUID",
    )
    hostel_id: UUID = Field(
        ...,
        description="Associated hostel UUID",
    )
    hostel_name: str = Field(
        ...,
        description="Associated hostel name",
    )
    
    # Visitor summary
    visitor_name: str = Field(
        ...,
        description="Visitor's name",
    )
    visitor_phone: str = Field(
        ...,
        description="Visitor's phone number",
    )
    visitor_email: str = Field(
        ...,
        description="Visitor's email address",
    )
    
>>>>>>> Stashed changes
    # Preferences
    preferred_check_in_date: Optional[date] = Field(
        None,
        description="Preferred check-in date",
    )
    stay_duration_months: Optional[int] = Field(
        None,
<<<<<<< Updated upstream
        description="Stay duration",
    )
    room_type_preference: Optional[RoomType] = Field(
        None,
        description="Room type preference",
    )

    # Status and Timing
=======
        description="Expected stay duration",
    )
    room_type_preference: Optional[RoomType] = Field(
        None,
        description="Preferred room type",
    )
    
    # Status and tracking
>>>>>>> Stashed changes
    status: InquiryStatus = Field(
        ...,
        description="Current status",
    )
<<<<<<< Updated upstream
=======
    inquiry_source: InquirySource = Field(
        ...,
        description="Inquiry source",
    )
    
    # Assignment info
    is_assigned: bool = Field(
        False,
        description="Whether inquiry is assigned",
    )
    assigned_to_name: Optional[str] = Field(
        None,
        description="Assigned staff name",
    )
    
    # Contact info
    is_contacted: bool = Field(
        False,
        description="Whether visitor has been contacted",
    )
    
    # Timestamps
>>>>>>> Stashed changes
    created_at: datetime = Field(
        ...,
        description="Creation timestamp",
    )
<<<<<<< Updated upstream

    # Quick Indicators
    is_urgent: bool = Field(
        ...,
        description="Whether inquiry requires urgent attention",
    )
    is_assigned: bool = Field(
        ...,
        description="Whether inquiry is assigned to someone",
    )

    @computed_field
    @property
    def age_days(self) -> int:
        """Calculate inquiry age."""
        return (datetime.utcnow() - self.created_at).days

    @computed_field
    @property
    def status_badge_color(self) -> str:
        """Get color code for status badge."""
        color_map = {
            InquiryStatus.NEW: "#FFA500",  # Orange
            InquiryStatus.CONTACTED: "#2196F3",  # Blue
            InquiryStatus.INTERESTED: "#4CAF50",  # Green
            InquiryStatus.NOT_INTERESTED: "#9E9E9E",  # Gray
            InquiryStatus.CONVERTED: "#9C27B0",  # Purple
        }
        return color_map.get(self.status, "#000000")
=======
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp",
    )
    
    @computed_field
    @property
    def age_days(self) -> int:
        """Days since inquiry was created."""
        return (datetime.utcnow() - self.created_at).days
    
    @computed_field
    @property
    def priority_score(self) -> int:
        """
        Calculate priority score for sorting.
        
        Higher score = higher priority.
        Factors: status, age, check-in date proximity.
        """
        score = 0
        
        # Status-based scoring
        status_scores = {
            InquiryStatus.NEW: 100,
            InquiryStatus.CONTACTED: 80,
            InquiryStatus.INTERESTED: 90,
            InquiryStatus.NOT_INTERESTED: 10,
            InquiryStatus.CONVERTED: 0,
        }
        score += status_scores.get(self.status, 50)
        
        # Age penalty (older = lower priority, max 50 point penalty)
        age_penalty = min(self.age_days * 2, 50)
        score -= age_penalty
        
        # Check-in date proximity bonus
        if self.preferred_check_in_date:
            days_until_check_in = (
                self.preferred_check_in_date - date.today()
            ).days
            if 0 <= days_until_check_in <= 7:
                score += 30  # Urgent - within a week
            elif 8 <= days_until_check_in <= 30:
                score += 15  # Soon - within a month
        
        return max(score, 0)
>>>>>>> Stashed changes


class InquiryStats(BaseSchema):
    """
<<<<<<< Updated upstream
    Inquiry statistics and analytics.
    
    Provides metrics about inquiry performance and conversion.
    """

    # Volume Metrics
=======
    Inquiry statistics for dashboard and reporting.
    
    Aggregated metrics for inquiry performance analysis.
    """
    
    # Volume metrics
>>>>>>> Stashed changes
    total_inquiries: int = Field(
        ...,
        ge=0,
        description="Total number of inquiries",
    )
    new_inquiries: int = Field(
        ...,
        ge=0,
        description="Inquiries with NEW status",
    )
    contacted_inquiries: int = Field(
        ...,
        ge=0,
        description="Inquiries that have been contacted",
    )
<<<<<<< Updated upstream
=======
    interested_inquiries: int = Field(
        ...,
        ge=0,
        description="Inquiries marked as interested",
    )
>>>>>>> Stashed changes
    converted_inquiries: int = Field(
        ...,
        ge=0,
        description="Inquiries converted to bookings",
    )
<<<<<<< Updated upstream

    # Response Metrics
    average_response_time_hours: Optional[float] = Field(
        None,
        ge=0,
        description="Average time to first contact in hours",
    )
    
    # Conversion Metrics
=======
    
    # Performance metrics
    avg_response_time_hours: Optional[float] = Field(
        None,
        ge=0,
        description="Average response time in hours",
    )
>>>>>>> Stashed changes
    conversion_rate: float = Field(
        ...,
        ge=0,
        le=100,
<<<<<<< Updated upstream
        description="Inquiry to booking conversion rate (%)",
    )
    interest_rate: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of inquiries showing interest",
    )

    # Source Breakdown
    inquiries_by_source: dict = Field(
        default_factory=dict,
        description="Breakdown of inquiries by source",
    )

    @computed_field
    @property
    def pending_action_count(self) -> int:
        """Count inquiries needing action (NEW + CONTACTED)."""
        return self.new_inquiries + self.contacted_inquiries

    @computed_field
    @property
    def response_rate(self) -> float:
        """Calculate percentage of inquiries that were contacted."""
        if self.total_inquiries == 0:
            return 0.0
        return round((self.contacted_inquiries / self.total_inquiries) * 100, 2)
=======
        description="Conversion rate percentage",
    )
    
    # Source breakdown
    inquiries_by_source: dict[str, int] = Field(
        default_factory=dict,
        description="Inquiry count by source",
    )
    
    # Time period
    period_start: datetime = Field(
        ...,
        description="Start of reporting period",
    )
    period_end: datetime = Field(
        ...,
        description="End of reporting period",
    )
    
    @computed_field
    @property
    def pending_action_count(self) -> int:
        """Count of inquiries requiring action."""
        return self.new_inquiries + self.interested_inquiries


class InquiryConversionInfo(BaseSchema):
    """
    Schema for inquiry to booking conversion details.
    
    Tracks the conversion event and associated booking.
    """
    
    inquiry_id: UUID = Field(
        ...,
        description="Original inquiry UUID",
    )
    booking_id: UUID = Field(
        ...,
        description="Created booking UUID",
    )
    converted_by: UUID = Field(
        ...,
        description="User who performed the conversion",
    )
    converted_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Conversion timestamp",
    )
    conversion_notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Notes about the conversion",
    )
    
    # Metrics
    days_to_convert: int = Field(
        ...,
        ge=0,
        description="Days from inquiry to conversion",
    )
    interactions_count: int = Field(
        ...,
        ge=0,
        description="Number of interactions before conversion",
    )


class HostelInquirySummary(BaseSchema):
    """
    Hostel-level inquiry summary for comparison views.
    
    Used in admin dashboards for multi-hostel overview.
    """
    
    hostel_id: UUID = Field(
        ...,
        description="Hostel UUID",
    )
    hostel_name: str = Field(
        ...,
        description="Hostel name",
    )
    
    # Counts
    total_inquiries: int = Field(
        ...,
        ge=0,
        description="Total inquiries for this hostel",
    )
    pending_inquiries: int = Field(
        ...,
        ge=0,
        description="Pending inquiries requiring action",
    )
    converted_inquiries: int = Field(
        ...,
        ge=0,
        description="Successfully converted inquiries",
    )
    
    # Performance
    conversion_rate: float = Field(
        ...,
        ge=0,
        le=100,
        description="Conversion rate percentage",
    )
    avg_response_time_hours: Optional[float] = Field(
        None,
        ge=0,
        description="Average response time",
    )
    
    # Recent activity
    last_inquiry_at: Optional[datetime] = Field(
        None,
        description="Most recent inquiry timestamp",
    )
>>>>>>> Stashed changes
