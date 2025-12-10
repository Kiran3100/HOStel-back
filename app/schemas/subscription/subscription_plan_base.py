"""
Subscription plan definition schemas
"""
from decimal import Decimal
from typing import Dict, Optional, List
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema
from app.schemas.common.enums import SubscriptionPlan


class SubscriptionPlanBase(BaseSchema):
    """Base subscription plan schema"""
    plan_name: str = Field(..., min_length=3, max_length=100, description="Plan internal name")
    display_name: str = Field(..., min_length=3, max_length=100, description="Plan display name")
    plan_type: SubscriptionPlan = Field(..., description="Plan tier/type")

    description: Optional[str] = Field(None, max_length=1000)

    price_monthly: Decimal = Field(..., ge=0, description="Monthly price")
    price_yearly: Decimal = Field(..., ge=0, description="Yearly price")
    currency: str = Field("INR", min_length=3, max_length=3)

    # Feature flags & limits as JSON
    features: Dict[str, object] = Field(
        default_factory=dict,
        description="Feature flags (e.g. max_hostels, advanced_analytics)",
    )

    max_hostels: Optional[int] = Field(None, ge=1)
    max_rooms_per_hostel: Optional[int] = Field(None, ge=1)
    max_students: Optional[int] = Field(None, ge=1)

    is_active: bool = Field(True)
    is_public: bool = Field(True, description="Show on pricing page")
    sort_order: int = Field(0, description="Ordering for display")


class PlanCreate(SubscriptionPlanBase, BaseCreateSchema):
    """Create new subscription plan"""
    pass


class PlanUpdate(BaseUpdateSchema):
    """Update subscription plan"""
    display_name: Optional[str] = None
    description: Optional[str] = None
    price_monthly: Optional[Decimal] = Field(None, ge=0)
    price_yearly: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = None
    features: Optional[Dict[str, object]] = None
    max_hostels: Optional[int] = Field(None, ge=1)
    max_rooms_per_hostel: Optional[int] = Field(None, ge=1)
    max_students: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None
    sort_order: Optional[int] = None