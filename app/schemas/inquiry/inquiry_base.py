# --- File: app/schemas/inquiry/inquiry_base.py ---
"""
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
Base visitor inquiry schemas with comprehensive validation.

This module defines the core inquiry schemas for managing visitor
inquiries about hostel availability and bookings.
<<<<<<< Updated upstream
=======
Base visitor inquiry schemas for creation and updates.

This module defines the foundational schemas for visitor inquiries,
including validation rules and business logic constraints.
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID

<<<<<<< Updated upstream
<<<<<<< Updated upstream
from pydantic import EmailStr, Field, field_validator, model_validator

from app.schemas.common.base import BaseCreateSchema, BaseSchema, BaseUpdateSchema
=======
from pydantic import (
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from app.schemas.common.base import (
    BaseCreateSchema,
    BaseFilterSchema,
    BaseSchema,
    BaseUpdateSchema,
)
>>>>>>> Stashed changes
=======
from pydantic import EmailStr, Field, field_validator, model_validator

from app.schemas.common.base import BaseCreateSchema, BaseSchema, BaseUpdateSchema
>>>>>>> Stashed changes
from app.schemas.common.enums import InquirySource, InquiryStatus, RoomType

__all__ = [
    "InquiryBase",
    "InquiryCreate",
    "InquiryUpdate",
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
    "InquiryFilter",
    "InquiryContactUpdate",
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
]


class InquiryBase(BaseSchema):
    """
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
    Base visitor inquiry schema with common fields.
    
    Contains all core inquiry information including hostel selection,
    visitor contact details, preferences, and inquiry metadata.
    """

    hostel_id: UUID = Field(
        ...,
        description="Unique identifier of the hostel being inquired about",
    )

    # Visitor Contact Information
<<<<<<< Updated upstream
=======
    Base visitor inquiry fields.
    
    Contains all common fields shared across inquiry operations
    with comprehensive validation.
    """
    
    hostel_id: UUID = Field(
        ...,
        description="UUID of the hostel being inquired about",
    )
    
    # Visitor information
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    visitor_name: str = Field(
        ...,
        min_length=2,
        max_length=255,
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
        description="Full name of the visitor making the inquiry",
    )
    visitor_email: EmailStr = Field(
        ...,
        description="Email address for communication",
<<<<<<< Updated upstream
=======
        description="Full name of the visitor",
        examples=["John Doe"],
    )
    visitor_email: EmailStr = Field(
        ...,
        description="Visitor's email address for communication",
        examples=["john.doe@example.com"],
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    )
    visitor_phone: str = Field(
        ...,
        pattern=r"^\+?[1-9]\d{9,14}$",
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
        description="Contact phone number (international format supported)",
    )

    # Inquiry Preferences
    preferred_check_in_date: Optional[date] = Field(
        None,
        description="Preferred or approximate check-in date",
<<<<<<< Updated upstream
=======
        description="Visitor's phone number (E.164 format recommended)",
        examples=["+919876543210"],
    )
    
    # Stay preferences
    preferred_check_in_date: Optional[date] = Field(
        None,
        description="Preferred check-in date (must be today or future)",
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    )
    stay_duration_months: Optional[int] = Field(
        None,
        ge=1,
        le=36,
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
        description="Intended stay duration in months (1-36)",
    )
    room_type_preference: Optional[RoomType] = Field(
        None,
        description="Preferred room type if any",
    )

    # Inquiry Details
    message: Optional[str] = Field(
        None,
        max_length=2000,
        description="Additional message or questions from visitor",
    )

    # Metadata
<<<<<<< Updated upstream
=======
        description="Expected stay duration in months (1-36)",
    )
    room_type_preference: Optional[RoomType] = Field(
        None,
        description="Preferred room type",
    )
    
    # Inquiry details
    message: Optional[str] = Field(
        None,
        max_length=2000,
        description="Additional message or requirements from visitor",
    )
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    inquiry_source: InquirySource = Field(
        InquirySource.WEBSITE,
        description="Source channel of the inquiry",
    )
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes

    status: InquiryStatus = Field(
        InquiryStatus.NEW,
        description="Current status of the inquiry",
    )

    @field_validator("visitor_name")
    @classmethod
    def validate_visitor_name(cls, v: str) -> str:
        """Validate and normalize visitor name."""
        v = v.strip()
        
        if len(v) < 2:
            raise ValueError("Visitor name must be at least 2 characters")
        
        # Check for at least one word
        if not v.split():
            raise ValueError("Visitor name cannot be empty or only whitespace")
        
        # Check for numbers (names shouldn't contain digits)
        if any(char.isdigit() for char in v):
            raise ValueError("Visitor name should not contain numbers")
        
        return v

    @field_validator("visitor_phone")
    @classmethod
    def validate_and_normalize_phone(cls, v: str) -> str:
        """Validate and normalize phone number."""
        # Remove common formatting characters
        v = v.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        # Check minimum length
        if len(v) < 10:
            raise ValueError("Phone number must be at least 10 digits")
        
        return v

    @field_validator("preferred_check_in_date")
    @classmethod
    def validate_check_in_date(cls, v: Optional[date]) -> Optional[date]:
        """Validate preferred check-in date."""
        if v is not None:
            # Allow past dates for inquiries (they might be inquiring for future)
            # but warn if too far in the past
            days_ago = (date.today() - v).days
            if days_ago > 7:
                # This might be an error, but we'll allow it
                # In production, you might want to log a warning
                pass
            
            # Warn if too far in the future (> 1 year)
            days_ahead = (v - date.today()).days
            if days_ahead > 365:
                # Log warning but allow
                pass
        
        return v

    @field_validator("message")
    @classmethod
    def clean_message(cls, v: Optional[str]) -> Optional[str]:
        """Clean and validate message."""
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
            
            # Check for excessive length
            if len(v) > 2000:
                raise ValueError("Message cannot exceed 2000 characters")
        
        return v

    @property
    def has_date_preference(self) -> bool:
        """Check if visitor has specified a preferred check-in date."""
        return self.preferred_check_in_date is not None

    @property
    def has_duration_preference(self) -> bool:
        """Check if visitor has specified stay duration."""
        return self.stay_duration_months is not None

    @property
    def has_room_preference(self) -> bool:
        """Check if visitor has specified room type preference."""
        return self.room_type_preference is not None

    @property
    def is_detailed_inquiry(self) -> bool:
        """Check if inquiry has detailed information."""
        return (
            self.has_date_preference
            and self.has_duration_preference
            and self.has_room_preference
        )
<<<<<<< Updated upstream
=======
    
    @field_validator("visitor_name")
    @classmethod
    def validate_visitor_name(cls, v: str) -> str:
        """Normalize and validate visitor name."""
        # Strip and normalize whitespace
        normalized = " ".join(v.split())
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not all(
            c.isalpha() or c in " -'" for c in normalized
        ):
            raise ValueError(
                "Name can only contain letters, spaces, hyphens, and apostrophes"
            )
        
        return normalized.title()
    
    @field_validator("preferred_check_in_date")
    @classmethod
    def validate_check_in_date(cls, v: Optional[date]) -> Optional[date]:
        """Ensure check-in date is not in the past."""
        if v is not None and v < date.today():
            raise ValueError("Preferred check-in date cannot be in the past")
        return v
    
    @field_validator("message")
    @classmethod
    def validate_message(cls, v: Optional[str]) -> Optional[str]:
        """Clean and validate message content."""
        if v is not None:
            # Strip whitespace and normalize
            v = v.strip()
            if len(v) == 0:
                return None
        return v
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes


class InquiryCreate(InquiryBase, BaseCreateSchema):
    """
    Schema for creating a new visitor inquiry.
    
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
    All base fields are inherited. Status is automatically set to NEW.
    """

    # Override status to always start as NEW
    status: InquiryStatus = Field(
        InquiryStatus.NEW,
        description="Status is automatically set to NEW for new inquiries",
    )

    @field_validator("status")
    @classmethod
    def validate_initial_status(cls, v: InquiryStatus) -> InquiryStatus:
        """Ensure new inquiries start with NEW status."""
        if v != InquiryStatus.NEW:
            # Force to NEW regardless of input
            return InquiryStatus.NEW
        return v
<<<<<<< Updated upstream
=======
    Inherits all fields from InquiryBase with creation-specific
    defaults and validations.
    """
    
    status: InquiryStatus = Field(
        InquiryStatus.NEW,
        description="Initial inquiry status (defaults to NEW)",
    )
    
    # Optional referral tracking
    referral_code: Optional[str] = Field(
        None,
        max_length=50,
        pattern=r"^[A-Z0-9_-]+$",
        description="Referral code if inquiry came through referral",
    )
    
    # UTM tracking for marketing analytics
    utm_source: Optional[str] = Field(
        None,
        max_length=100,
        description="UTM source parameter",
    )
    utm_medium: Optional[str] = Field(
        None,
        max_length=100,
        description="UTM medium parameter",
    )
    utm_campaign: Optional[str] = Field(
        None,
        max_length=100,
        description="UTM campaign parameter",
    )
    
    @model_validator(mode="after")
    def validate_referral_source(self) -> "InquiryCreate":
        """Validate referral code is provided when source is referral."""
        if (
            self.inquiry_source == InquirySource.REFERRAL
            and not self.referral_code
        ):
            raise ValueError(
                "Referral code is required when inquiry source is 'referral'"
            )
        return self
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes


class InquiryUpdate(BaseUpdateSchema):
    """
    Schema for updating an existing inquiry.
    
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
    All fields are optional, allowing partial updates.
    Typically used by admins to add notes or update contact info.
    """

    # Visitor Contact (rarely updated, but allowed)
<<<<<<< Updated upstream
=======
    All fields are optional to support partial updates.
    Status updates should use InquiryStatusUpdate for audit trail.
    """
    
    # Visitor information updates
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    visitor_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=255,
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
        description="Update visitor name",
    )
    visitor_email: Optional[EmailStr] = Field(
        None,
        description="Update visitor email",
<<<<<<< Updated upstream
=======
        description="Updated visitor name",
    )
    visitor_email: Optional[EmailStr] = Field(
        None,
        description="Updated visitor email",
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    )
    visitor_phone: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{9,14}$",
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
        description="Update visitor phone",
    )

    # Preferences (can be updated as inquiry is refined)
    preferred_check_in_date: Optional[date] = Field(
        None,
        description="Update preferred check-in date",
<<<<<<< Updated upstream
=======
        description="Updated visitor phone",
    )
    
    # Stay preference updates
    preferred_check_in_date: Optional[date] = Field(
        None,
        description="Updated preferred check-in date",
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    )
    stay_duration_months: Optional[int] = Field(
        None,
        ge=1,
        le=36,
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
        description="Update stay duration",
    )
    room_type_preference: Optional[RoomType] = Field(
        None,
        description="Update room type preference",
    )

    # Message (can be appended or updated)
    message: Optional[str] = Field(
        None,
        max_length=2000,
        description="Update inquiry message",
    )

    # Status (usually updated via separate status update endpoint)
    status: Optional[InquiryStatus] = Field(
        None,
        description="Update inquiry status",
    )

    @field_validator("visitor_name")
    @classmethod
    def validate_visitor_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate visitor name if provided."""
        if v is not None:
            v = v.strip()
            if len(v) < 2:
                raise ValueError("Visitor name must be at least 2 characters")
            if any(char.isdigit() for char in v):
                raise ValueError("Visitor name should not contain numbers")
        return v

    @field_validator("visitor_phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Normalize phone number if provided."""
        if v is not None:
            v = v.replace(" ", "").replace("-", "")
            if len(v) < 10:
                raise ValueError("Phone number must be at least 10 digits")
        return v

    @field_validator("message")
    @classmethod
    def clean_message(cls, v: Optional[str]) -> Optional[str]:
        """Clean message if provided."""
        if v is not None:
            v = v.strip()
            if len(v) == 0:
                return None
<<<<<<< Updated upstream
=======
        description="Updated stay duration",
    )
    room_type_preference: Optional[RoomType] = Field(
        None,
        description="Updated room type preference",
    )
    
    # Other updates
    message: Optional[str] = Field(
        None,
        max_length=2000,
        description="Updated message",
    )
    notes: Optional[str] = Field(
        None,
        max_length=2000,
        description="Internal notes about the inquiry",
    )
    
    @field_validator("visitor_name")
    @classmethod
    def validate_visitor_name(cls, v: Optional[str]) -> Optional[str]:
        """Normalize visitor name if provided."""
        if v is not None:
            normalized = " ".join(v.split())
            if not all(c.isalpha() or c in " -'" for c in normalized):
                raise ValueError(
                    "Name can only contain letters, spaces, hyphens, and apostrophes"
                )
            return normalized.title()
        return v
    
    @field_validator("preferred_check_in_date")
    @classmethod
    def validate_check_in_date(cls, v: Optional[date]) -> Optional[date]:
        """Ensure check-in date is not in the past."""
        if v is not None and v < date.today():
            raise ValueError("Preferred check-in date cannot be in the past")
        return v
    
    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "InquiryUpdate":
        """Ensure at least one field is provided for update."""
        update_fields = {
            "visitor_name",
            "visitor_email", 
            "visitor_phone",
            "preferred_check_in_date",
            "stay_duration_months",
            "room_type_preference",
            "message",
            "notes",
        }
        
        if not any(
            getattr(self, field) is not None for field in update_fields
        ):
            raise ValueError("At least one field must be provided for update")
        
        return self


class InquiryContactUpdate(BaseUpdateSchema):
    """
    Schema for recording contact with inquiry visitor.
    
    Used when admin/staff contacts a visitor regarding their inquiry.
    """
    
    contacted_by: UUID = Field(
        ...,
        description="UUID of the user who contacted the visitor",
    )
    contacted_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of when contact was made",
    )
    contact_method: str = Field(
        ...,
        pattern=r"^(phone|email|whatsapp|in_person|other)$",
        description="Method used to contact the visitor",
    )
    contact_notes: Optional[str] = Field(
        None,
        max_length=1000,
        description="Notes from the contact interaction",
    )
    follow_up_required: bool = Field(
        False,
        description="Whether follow-up is required",
    )
    follow_up_date: Optional[date] = Field(
        None,
        description="Scheduled follow-up date if required",
    )
    
    @model_validator(mode="after")
    def validate_follow_up(self) -> "InquiryContactUpdate":
        """Validate follow-up date is provided when required."""
        if self.follow_up_required and not self.follow_up_date:
            raise ValueError(
                "Follow-up date is required when follow_up_required is True"
            )
        if self.follow_up_date and self.follow_up_date < date.today():
            raise ValueError("Follow-up date cannot be in the past")
        return self


class InquiryFilter(BaseFilterSchema):
    """
    Filter parameters for querying inquiries.
    
    Supports filtering by various criteria including status,
    date ranges, hostel, and search terms.
    """
    
    # Status filtering
    status: Optional[InquiryStatus] = Field(
        None,
        description="Filter by inquiry status",
    )
    statuses: Optional[list[InquiryStatus]] = Field(
        None,
        description="Filter by multiple statuses",
    )
    exclude_statuses: Optional[list[InquiryStatus]] = Field(
        None,
        description="Exclude specific statuses",
    )
    
    # Hostel filtering
    hostel_id: Optional[UUID] = Field(
        None,
        description="Filter by specific hostel",
    )
    hostel_ids: Optional[list[UUID]] = Field(
        None,
        description="Filter by multiple hostels",
    )
    
    # Source filtering
    inquiry_source: Optional[InquirySource] = Field(
        None,
        description="Filter by inquiry source",
    )
    
    # Room preference filtering
    room_type_preference: Optional[RoomType] = Field(
        None,
        description="Filter by room type preference",
    )
    
    # Date range filtering
    created_after: Optional[datetime] = Field(
        None,
        description="Filter inquiries created after this datetime",
    )
    created_before: Optional[datetime] = Field(
        None,
        description="Filter inquiries created before this datetime",
    )
    check_in_date_from: Optional[date] = Field(
        None,
        description="Filter by preferred check-in date (from)",
    )
    check_in_date_to: Optional[date] = Field(
        None,
        description="Filter by preferred check-in date (to)",
    )
    
    # Assignment filtering
    assigned_to: Optional[UUID] = Field(
        None,
        description="Filter by assigned user",
    )
    is_assigned: Optional[bool] = Field(
        None,
        description="Filter by assignment status",
    )
    is_contacted: Optional[bool] = Field(
        None,
        description="Filter by contact status",
    )
    
    # Search
    search: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Search in visitor name, email, or phone",
    )
    
    # Sorting
    sort_by: str = Field(
        "created_at",
        pattern=r"^(created_at|updated_at|visitor_name|status|preferred_check_in_date)$",
        description="Field to sort by",
    )
    sort_order: str = Field(
        "desc",
        pattern=r"^(asc|desc)$",
        description="Sort order (asc/desc)",
    )
    
    @field_validator("created_before")
    @classmethod
    def validate_date_range(
        cls, v: Optional[datetime], info
    ) -> Optional[datetime]:
        """Validate that created_before is after created_after."""
        created_after = info.data.get("created_after")
        if v and created_after and v < created_after:
            raise ValueError("created_before must be after created_after")
        return v
    
    @field_validator("check_in_date_to")
    @classmethod
    def validate_check_in_range(
        cls, v: Optional[date], info
    ) -> Optional[date]:
        """Validate check-in date range."""
        check_in_from = info.data.get("check_in_date_from")
        if v and check_in_from and v < check_in_from:
            raise ValueError("check_in_date_to must be after check_in_date_from")
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        return v