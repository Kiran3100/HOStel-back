# --- File: app/schemas/maintenance/maintenance_request.py ---
"""
Maintenance request submission schemas.

Provides schemas for different types of maintenance requests including
standard, detailed supervisor submissions, and emergency requests.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import List, Optional

from pydantic import Field, HttpUrl, field_validator, model_validator
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema
from app.schemas.common.enums import MaintenanceCategory, Priority

__all__ = [
    "MaintenanceRequest",
    "RequestSubmission",
    "EmergencyRequest",
]


class MaintenanceRequest(BaseCreateSchema):
    """
    Standard maintenance request submission.
    
    Simplified schema for students/residents to submit maintenance
    issues with essential information.
    """

    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    room_id: Optional[UUID] = Field(
        None,
        description="Room where issue exists",
    )
    title: str = Field(
        ...,
        min_length=5,
        max_length=255,
        description="Brief issue summary",
    )
    description: str = Field(
        ...,
        min_length=20,
        max_length=2000,
        description="Detailed issue description",
    )
    category: MaintenanceCategory = Field(
        ...,
        description="Issue category",
    )
    priority: Priority = Field(
        Priority.MEDIUM,
        description="Requested priority (may be adjusted by supervisor)",
    )
    location: Optional[str] = Field(
        None,
        max_length=500,
        description="Additional location details",
    )
    issue_photos: List[HttpUrl] = Field(
        default_factory=list,
        max_length=10,
        description="Issue photographs",
    )
    preferred_time_slot: Optional[str] = Field(
        None,
        pattern=r"^(morning|afternoon|evening|any)$",
        description="Preferred time for repair work",
    )
    contact_number: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{9,14}$",
        description="Contact number for follow-up",
    )

    @field_validator("title", "description")
    @classmethod
    def validate_text_fields(cls, v: str) -> str:
        """Validate text fields are meaningful."""
        v = v.strip()
        
        field_name = cls.model_fields.get("title") or cls.model_fields.get("description")
        min_length = 5 if field_name == "title" else 20
        
        if len(v) < min_length:
            raise ValueError(f"Field must be at least {min_length} characters")
        
        # Check for meaningful content
        min_unique_chars = 3 if min_length == 5 else 10
        if len(set(v.lower().replace(" ", ""))) < min_unique_chars:
            raise ValueError("Please provide meaningful and descriptive text")
        
        return v

    @field_validator("contact_number")
    @classmethod
    def normalize_phone(cls, v: Optional[str]) -> Optional[str]:
        """Normalize phone number."""
        if v is not None:
            return v.replace(" ", "").replace("-", "").strip()
        return None

    @field_validator("location")
    @classmethod
    def normalize_location(cls, v: Optional[str]) -> Optional[str]:
        """Normalize location field."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return None


class RequestSubmission(BaseCreateSchema):
    """
    Detailed maintenance request submission by supervisor.
    
    Enhanced schema with cost estimation, vendor preferences,
    and timeline planning capabilities.
    """

    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    room_id: Optional[UUID] = Field(
        None,
        description="Room where issue exists",
    )
    title: str = Field(
        ...,
        min_length=5,
        max_length=255,
        description="Issue title",
    )
    description: str = Field(
        ...,
        min_length=20,
        max_length=2000,
        description="Detailed description",
    )
    category: MaintenanceCategory = Field(
        ...,
        description="Maintenance category",
    )
    priority: Priority = Field(
        ...,
        description="Issue priority",
    )
    location: Optional[str] = Field(
        None,
        max_length=500,
        description="Location details",
    )
    issue_photos: List[HttpUrl] = Field(
        default_factory=list,
        max_length=10,
        description="Issue photographs",
    )

    # Supervisor-specific fields
    estimated_cost: Optional[Decimal] = Field(
        None,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Estimated repair cost",
    )
    cost_justification: Optional[str] = Field(
        None,
        max_length=500,
        description="Justification for estimated cost",
    )
    preferred_vendor: Optional[str] = Field(
        None,
        max_length=255,
        description="Preferred vendor/contractor name",
    )
    vendor_contact: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{9,14}$",
        description="Vendor contact number",
    )
    estimated_days: Optional[int] = Field(
        None,
        ge=1,
        le=365,
        description="Estimated days to complete work",
    )
    requires_immediate_attention: bool = Field(
        False,
        description="Flag for urgent/emergency issues",
    )
    approval_required: bool = Field(
        False,
        description="Whether admin approval is required",
    )
    materials_needed: Optional[str] = Field(
        None,
        max_length=1000,
        description="List of materials/parts needed",
    )

    @field_validator("estimated_cost")
    @classmethod
    def round_cost(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Round cost to 2 decimal places."""
        return round(v, 2) if v is not None else None

    @field_validator("vendor_contact")
    @classmethod
    def normalize_phone(cls, v: Optional[str]) -> Optional[str]:
        """Normalize vendor phone number."""
        if v is not None:
            return v.replace(" ", "").replace("-", "").strip()
        return None

    @field_validator("cost_justification", "materials_needed")
    @classmethod
    def normalize_text(cls, v: Optional[str]) -> Optional[str]:
        """Normalize text fields."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return None

    @model_validator(mode="after")
    def validate_vendor_information(self) -> "RequestSubmission":
        """
        Validate vendor information completeness.
        
        If vendor is specified, contact should be provided.
        """
        if self.preferred_vendor and not self.vendor_contact:
            raise ValueError(
                "Vendor contact is required when preferred vendor is specified"
            )
        
        return self

    @model_validator(mode="after")
    def validate_cost_information(self) -> "RequestSubmission":
        """
        Validate cost estimation requirements.
        
        High-cost estimates should have justification.
        """
        if self.estimated_cost is not None:
            # Cost above threshold requires justification
            if self.estimated_cost > Decimal("5000.00"):
                if not self.cost_justification:
                    raise ValueError(
                        "Cost justification required for estimates above ₹5000"
                    )
                
                if len(self.cost_justification.strip()) < 20:
                    raise ValueError(
                        "Cost justification must be at least 20 characters"
                    )
        
        return self

    @model_validator(mode="after")
    def validate_urgency_consistency(self) -> "RequestSubmission":
        """
        Validate urgency and priority consistency.
        
        Immediate attention requests should have high priority.
        """
        if self.requires_immediate_attention:
            if self.priority not in [Priority.HIGH, Priority.URGENT, Priority.CRITICAL]:
                raise ValueError(
                    "Requests requiring immediate attention must have HIGH, "
                    "URGENT, or CRITICAL priority"
                )
        
        return self


class EmergencyRequest(BaseCreateSchema):
    """
    Emergency maintenance request with safety protocols.
    
    Handles critical situations requiring immediate response
    with safety tracking and authority notification.
    """

    hostel_id: UUID = Field(
        ...,
        description="Hostel unique identifier",
    )
    emergency_type: str = Field(
        ...,
        pattern=r"^(fire|flood|electrical_hazard|gas_leak|structural_damage|lift_malfunction|other)$",
        description="Type of emergency",
    )
    description: str = Field(
        ...,
        min_length=20,
        max_length=2000,
        description="Detailed emergency description",
    )
    location: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Exact emergency location",
    )
    affected_area: Optional[str] = Field(
        None,
        max_length=500,
        description="Area/rooms affected by emergency",
    )

    # Safety information
    immediate_actions_taken: Optional[str] = Field(
        None,
        max_length=1000,
        description="Immediate actions already taken",
    )
    evacuated: bool = Field(
        False,
        description="Whether area has been evacuated",
    )
    evacuation_details: Optional[str] = Field(
        None,
        max_length=500,
        description="Evacuation details if applicable",
    )
    authorities_notified: bool = Field(
        False,
        description="Whether emergency services have been notified",
    )
    authority_details: Optional[str] = Field(
        None,
        max_length=500,
        description="Details of authorities notified",
    )

    # Contact information
    contact_person: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="On-site contact person name",
    )
    contact_phone: str = Field(
        ...,
        pattern=r"^\+?[1-9]\d{9,14}$",
        description="Contact person phone number",
    )
    alternate_contact: Optional[str] = Field(
        None,
        pattern=r"^\+?[1-9]\d{9,14}$",
        description="Alternate contact number",
    )

    # Severity assessment
    injuries_reported: bool = Field(
        default=False,
        description="Whether there are any injuries",
    )
    injury_details: Optional[str] = Field(
        None,
        max_length=500,
        description="Details of injuries if any",
    )
    property_damage_estimated: Optional[str] = Field(
        None,
        pattern=r"^(minor|moderate|major|severe|catastrophic)$",
        description="Estimated property damage level",
    )

    # Supporting evidence
    emergency_photos: List[HttpUrl] = Field(
        default_factory=list,
        max_length=15,
        description="Emergency situation photographs",
    )

    @field_validator("description", "location")
    @classmethod
    def validate_required_text(cls, v: str) -> str:
        """Validate required text fields."""
        v = v.strip()
        
        if len(v) < 20:
            raise ValueError("Emergency details must be comprehensive (min 20 chars)")
        
        return v

    @field_validator("contact_phone", "alternate_contact")
    @classmethod
    def normalize_phone(cls, v: Optional[str]) -> Optional[str]:
        """Normalize phone numbers."""
        if v is not None:
            return v.replace(" ", "").replace("-", "").strip()
        return None

    @field_validator(
        "immediate_actions_taken",
        "evacuation_details",
        "authority_details",
        "injury_details",
    )
    @classmethod
    def normalize_text_fields(cls, v: Optional[str]) -> Optional[str]:
        """Normalize optional text fields."""
        if v is not None:
            v = v.strip()
            return v if v else None
        return None

    @model_validator(mode="after")
    def validate_evacuation_consistency(self) -> "EmergencyRequest":
        """
        Validate evacuation information consistency.
        
        If evacuated, details should be provided.
        """
        if self.evacuated and not self.evacuation_details:
            raise ValueError(
                "Evacuation details are required when area has been evacuated"
            )
        
        return self

    @model_validator(mode="after")
    def validate_injury_reporting(self) -> "EmergencyRequest":
        """
        Validate injury reporting requirements.
        
        If injuries reported, details must be provided.
        """
        if self.injuries_reported and not self.injury_details:
            raise ValueError(
                "Injury details are required when injuries are reported"
            )
        
        return self

    @model_validator(mode="after")
    def validate_authority_notification(self) -> "EmergencyRequest":
        """
        Validate authority notification for serious emergencies.
        
        Certain emergency types should have authorities notified.
        """
        serious_emergencies = {"fire", "gas_leak", "structural_damage"}
        
        if self.emergency_type in serious_emergencies:
            if not self.authorities_notified:
                raise ValueError(
                    f"{self.emergency_type} emergencies should have authorities notified. "
                    "If not yet notified, please notify immediately."
                )
            
            if not self.authority_details:
                raise ValueError(
                    "Authority notification details are required for serious emergencies"
                )
        
        return self

    @model_validator(mode="after")
    def validate_safety_actions(self) -> "EmergencyRequest":
        """
        Validate safety action documentation.
        
        Emergency requests should document immediate actions.
        """
        dangerous_types = {"fire", "gas_leak", "electrical_hazard"}
        
        if self.emergency_type in dangerous_types:
            if not self.immediate_actions_taken:
                raise ValueError(
                    f"Immediate actions taken must be documented for {self.emergency_type}"
                )
        
        return self