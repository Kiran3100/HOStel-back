"""
Visitor preferences schemas
"""
from decimal import Decimal
from typing import List, Optional
from pydantic import Field, field_validator

from app.schemas.common.base import BaseSchema, BaseUpdateSchema
from app.schemas.common.enums import RoomType, HostelType, DietaryPreference


class VisitorPreferences(BaseSchema):
    """Complete visitor preferences"""
    # Room preferences
    preferred_room_type: Optional[RoomType] = None
    preferred_hostel_type: Optional[HostelType] = None
    
    # Budget
    budget_min: Optional[Decimal] = Field(None, ge=0)
    budget_max: Optional[Decimal] = Field(None, ge=0)
    
    # Location
    preferred_cities: List[str] = Field(default_factory=list)
    preferred_areas: List[str] = Field(default_factory=list)
    max_distance_from_work_km: Optional[Decimal] = Field(None, ge=0, le=50)
    
    # Amenities (must-have)
    required_amenities: List[str] = Field(default_factory=list)
    preferred_amenities: List[str] = Field(default_factory=list)
    
    # Facilities
    need_parking: bool = Field(False)
    need_gym: bool = Field(False)
    need_laundry: bool = Field(False)
    need_mess: bool = Field(False)
    
    # Dietary
    dietary_preference: Optional[DietaryPreference] = None
    
    # Move-in
    earliest_move_in_date: Optional[date] = None
    preferred_lease_duration_months: Optional[int] = Field(None, ge=1, le=24)
    
    # Notifications
    email_notifications: bool = Field(True)
    sms_notifications: bool = Field(True)
    push_notifications: bool = Field(True)
    
    # Specific notification types
    notify_on_price_drop: bool = Field(True, description="Notify when saved hostel reduces price")
    notify_on_availability: bool = Field(True, description="Notify when saved hostel has availability")
    notify_on_new_listings: bool = Field(True, description="Notify about new matching hostels")
    
    @field_validator('budget_max')
    @classmethod
    def validate_budget(cls, v: Optional[Decimal], info) -> Optional[Decimal]:
        """Validate budget_max >= budget_min"""
        if v and info.data.get('budget_min'):
            if v < info.data['budget_min']:
                raise ValueError('Maximum budget must be >= minimum budget')
        return v


class PreferenceUpdate(BaseUpdateSchema):
    """Update visitor preferences"""
    preferred_room_type: Optional[RoomType] = None
    preferred_hostel_type: Optional[HostelType] = None
    budget_min: Optional[Decimal] = Field(None, ge=0)
    budget_max: Optional[Decimal] = Field(None, ge=0)
    preferred_cities: Optional[List[str]] = None
    required_amenities: Optional[List[str]] = None
    dietary_preference: Optional[DietaryPreference] = None
    
    # Notification toggles
    email_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    notify_on_price_drop: Optional[bool] = None
    notify_on_availability: Optional[bool] = None
    notify_on_new_listings: Optional[bool] = None


class SearchPreferences(BaseSchema):
    """Saved search preferences"""
    search_name: str = Field(..., min_length=3, max_length=100, description="Name for this saved search")
    
    # Search criteria
    cities: List[str] = Field(default_factory=list)
    room_types: List[RoomType] = Field(default_factory=list)
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    amenities: List[str] = Field(default_factory=list)
    
    # Alert settings
    notify_on_new_matches: bool = Field(True, description="Notify when new hostels match criteria")
    notification_frequency: str = Field(
        "daily",
        pattern="^(instant|daily|weekly)$",
        description="How often to send notifications"
    )


class SavedSearch(BaseSchema):
    """Saved search with ID"""
    id: UUID
    visitor_id: UUID
    search_name: str
    criteria: dict = Field(..., description="Search criteria as JSON")
    notify_on_new_matches: bool
    notification_frequency: str
    
    # Stats
    total_matches: int = Field(0, description="Current number of matching hostels")
    new_matches_since_last_check: int = Field(0)
    
    created_at: datetime
    last_checked: Optional[datetime]