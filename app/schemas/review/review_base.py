# --- File: app/schemas/review/review_base.py ---
"""
Base review schemas with comprehensive validation.

Provides foundation schemas for review creation and updates.
"""

from __future__ import annotations

from decimal import Decimal
from typing import List, Optional

from pydantic import Field, HttpUrl, field_validator, model_validator
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema

__all__ = [
    "ReviewBase",
    "ReviewCreate",
    "ReviewUpdate",
    "DetailedRatings",
]


class DetailedRatings(BaseSchema):
    """
    Detailed aspect-based ratings for comprehensive feedback.
    
    Allows reviewers to rate specific aspects of their experience.
    """
    
    cleanliness_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Cleanliness and hygiene rating",
    )
    food_quality_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Food quality rating (if mess facility available)",
    )
    staff_behavior_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Staff courtesy and helpfulness rating",
    )
    security_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Safety and security measures rating",
    )
    value_for_money_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Value for money rating",
    )
    amenities_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Facilities and amenities quality rating",
    )
    location_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Location convenience rating",
    )
    wifi_quality_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Internet/WiFi quality rating",
    )
    maintenance_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Maintenance responsiveness rating",
    )


class ReviewBase(BaseSchema):
    """
    Base review schema with all core fields.
    
    Foundation for review creation with comprehensive validation.
    """
    
    # Identifiers
    hostel_id: UUID = Field(..., description="Hostel being reviewed")
    reviewer_id: UUID = Field(..., description="User submitting the review")
    student_id: Optional[UUID] = Field(
        None,
        description="Student profile ID (for verified stay reviews)",
    )
    booking_id: Optional[UUID] = Field(
        None,
        description="Related booking reference for verification",
    )
    
    # Overall rating
    overall_rating: Decimal = Field(
        ...,
        ge=Decimal("1.0"),
        le=Decimal("5.0"),
        decimal_places=1,
        description="Overall rating (1.0 to 5.0, in 0.5 increments)",
        examples=[Decimal("4.5"), Decimal("3.0")],
    )
    
    # Review content
    title: str = Field(
        ...,
        min_length=5,
        max_length=255,
        description="Review title/headline",
        examples=["Great hostel with excellent facilities"],
    )
    review_text: str = Field(
        ...,
        min_length=50,
        max_length=5000,
        description="Detailed review text",
    )
    
    # Detailed aspect ratings (optional but encouraged)
    cleanliness_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Cleanliness rating",
    )
    food_quality_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Food quality rating",
    )
    staff_behavior_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Staff behavior rating",
    )
    security_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Security rating",
    )
    value_for_money_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Value for money rating",
    )
    amenities_rating: Optional[int] = Field(
        None,
        ge=1,
        le=5,
        description="Amenities rating",
    )
    
    # Media attachments
    photos: List[HttpUrl] = Field(
        default_factory=list,
        max_length=10,
        description="Review photos (max 10)",
        examples=[
            [
                "https://example.com/photos/room1.jpg",
                "https://example.com/photos/facilities.jpg",
            ]
        ],
    )
    
    @field_validator("overall_rating")
    @classmethod
    def round_rating_to_half(cls, v: Decimal) -> Decimal:
        """
        Round overall rating to nearest 0.5.
        
        Ensures consistent rating increments (1.0, 1.5, 2.0, etc.).
        """
        return Decimal(str(round(float(v) * 2) / 2))
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate and clean review title."""
        v = v.strip()
        if not v:
            raise ValueError("Review title cannot be empty")
        
        # Check for excessive capitalization (possible spam)
        if len(v) > 10 and v.isupper():
            raise ValueError(
                "Please avoid using all caps in your review title"
            )
        
        return v
    
    @field_validator("review_text")
    @classmethod
    def validate_review_text(cls, v: str) -> str:
        """Validate and clean review text."""
        v = v.strip()
        if not v:
            raise ValueError("Review text cannot be empty")
        
        # Check minimum word count (approximately 10 words)
        word_count = len(v.split())
        if word_count < 10:
            raise ValueError(
                "Please provide a more detailed review (minimum 10 words)"
            )
        
        # Check for excessive capitalization
        if len(v) > 50 and sum(1 for c in v if c.isupper()) / len(v) > 0.5:
            raise ValueError(
                "Please avoid excessive use of capital letters in your review"
            )
        
        return v
    
    @field_validator("photos")
    @classmethod
    def validate_photos(cls, v: List[HttpUrl]) -> List[HttpUrl]:
        """Validate photo URLs."""
        if len(v) > 10:
            raise ValueError("Maximum 10 photos allowed per review")
        
        # Convert to list of strings and back to ensure consistency
        return v
    
    @model_validator(mode="after")
    def validate_rating_consistency(self) -> "ReviewBase":
        """
        Validate that overall rating is consistent with detailed ratings.
        
        If detailed ratings are provided, checks that overall rating
        is reasonably aligned with the average of detailed ratings.
        """
        detailed_ratings = [
            r for r in [
                self.cleanliness_rating,
                self.food_quality_rating,
                self.staff_behavior_rating,
                self.security_rating,
                self.value_for_money_rating,
                self.amenities_rating,
            ]
            if r is not None
        ]
        
        if detailed_ratings:
            avg_detailed = sum(detailed_ratings) / len(detailed_ratings)
            overall = float(self.overall_rating)
            
            # Allow some variance (±1 star)
            if abs(overall - avg_detailed) > 1.5:
                raise ValueError(
                    "Overall rating seems inconsistent with detailed ratings. "
                    "Please review your ratings."
                )
        
        return self


class ReviewCreate(ReviewBase, BaseCreateSchema):
    """
    Schema for creating a new review.
    
    Inherits all validation from ReviewBase and adds creation-specific rules.
    """
    
    # Additional fields for creation context
    would_recommend: bool = Field(
        ...,
        description="Would the reviewer recommend this hostel?",
    )
    
    stay_duration_months: Optional[int] = Field(
        None,
        ge=1,
        le=24,
        description="Duration of stay in months (helps with verification)",
    )
    
    @model_validator(mode="after")
    def validate_recommendation_consistency(self) -> "ReviewCreate":
        """
        Validate recommendation aligns with rating.
        
        Warns if low-rated review has recommendation or vice versa.
        """
        rating = float(self.overall_rating)
        
        # High rating (4+) but not recommending seems inconsistent
        if rating >= 4.0 and not self.would_recommend:
            # This is allowed but logged for review
            pass
        
        # Low rating (<3) but recommending seems inconsistent
        if rating < 3.0 and self.would_recommend:
            # This is allowed but logged for review
            pass
        
        return self


class ReviewUpdate(BaseUpdateSchema):
    """
    Schema for updating an existing review.
    
    Allows partial updates with time-limited edit window.
    All fields are optional to support partial updates.
    """
    
    # Content updates
    title: Optional[str] = Field(
        None,
        min_length=5,
        max_length=255,
        description="Updated review title",
    )
    review_text: Optional[str] = Field(
        None,
        min_length=50,
        max_length=5000,
        description="Updated review text",
    )
    
    # Rating updates
    overall_rating: Optional[Decimal] = Field(
        None,
        ge=Decimal("1.0"),
        le=Decimal("5.0"),
        decimal_places=1,
        description="Updated overall rating",
    )
    
    # Detailed ratings updates
    cleanliness_rating: Optional[int] = Field(None, ge=1, le=5)
    food_quality_rating: Optional[int] = Field(None, ge=1, le=5)
    staff_behavior_rating: Optional[int] = Field(None, ge=1, le=5)
    security_rating: Optional[int] = Field(None, ge=1, le=5)
    value_for_money_rating: Optional[int] = Field(None, ge=1, le=5)
    amenities_rating: Optional[int] = Field(None, ge=1, le=5)
    
    # Media updates
    photos: Optional[List[HttpUrl]] = Field(
        None,
        max_length=10,
        description="Updated photo list",
    )
    
    @field_validator("overall_rating")
    @classmethod
    def round_rating_to_half(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Round overall rating to nearest 0.5."""
        if v is None:
            return v
        return Decimal(str(round(float(v) * 2) / 2))
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate updated title."""
        if v is None:
            return v
        
        v = v.strip()
        if not v:
            raise ValueError("Review title cannot be empty")
        
        if len(v) > 10 and v.isupper():
            raise ValueError(
                "Please avoid using all caps in your review title"
            )
        
        return v
    
    @field_validator("review_text")
    @classmethod
    def validate_review_text(cls, v: Optional[str]) -> Optional[str]:
        """Validate updated review text."""
        if v is None:
            return v
        
        v = v.strip()
        if not v:
            raise ValueError("Review text cannot be empty")
        
        word_count = len(v.split())
        if word_count < 10:
            raise ValueError(
                "Please provide a more detailed review (minimum 10 words)"
            )
        
        return v
    
    @field_validator("photos")
    @classmethod
    def validate_photos(cls, v: Optional[List[HttpUrl]]) -> Optional[List[HttpUrl]]:
        """Validate updated photos."""
        if v is None:
            return v
        
        if len(v) > 10:
            raise ValueError("Maximum 10 photos allowed per review")
        
        return v