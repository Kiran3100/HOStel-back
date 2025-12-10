"""
Visitor base schemas
"""
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseSchema
from app.schemas.common.enums import RoomType


class VisitorBase(BaseSchema):
    """Base visitor schema"""
    user_id: UUID = Field(..., description="Associated user ID")
    
    # Preferences
    preferred_room_type: Optional[RoomType] = Field(None, description="Preferred room type")
    budget_min: Optional[Decimal] = Field(None, ge=0, description="Minimum budget")
    budget_max: Optional[Decimal] = Field(None, ge=0, description="Maximum budget")
    preferred_cities: List[str] = Field(default_factory=list, description="Preferred cities")
    preferred_amenities: List[str] = Field(default_factory=list, description="Must-have amenities")
    
    # Saved/favorite hostels
    favorite_hostel_ids: List[UUID] = Field(default_factory=list, description="Favorite hostel IDs")
    
    # Notification preferences
    email_notifications: bool = Field(True, description="Receive email notifications")
    sms_notifications: bool = Field(True, description="Receive SMS notifications")
    push_notifications: bool = Field(True, description="Receive push notifications")


class VisitorCreate(VisitorBase, BaseCreateSchema):
    """Create visitor profile"""
    pass


class VisitorUpdate(BaseUpdateSchema):
    """Update visitor profile"""
    preferred_room_type: Optional[RoomType] = None
    budget_min: Optional[Decimal] = Field(None, ge=0)
    budget_max: Optional[Decimal] = Field(None, ge=0)
    preferred_cities: Optional[List[str]] = None
    preferred_amenities: Optional[List[str]] = None
    
    # Notification preferences
    email_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None