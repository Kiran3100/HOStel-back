"""
Subscription plan response & comparison schemas
"""
from decimal import Decimal
from typing import Dict, List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema
from app.schemas.common.enums import SubscriptionPlan


class PlanResponse(BaseResponseSchema):
    """Subscription plan response"""
    plan_name: str
    display_name: str
    plan_type: SubscriptionPlan

    description: Optional[str]
    price_monthly: Decimal
    price_yearly: Decimal
    currency: str

    features: Dict[str, object]
    max_hostels: Optional[int]
    max_rooms_per_hostel: Optional[int]
    max_students: Optional[int]

    is_active: bool
    is_public: bool
    sort_order: int


class PlanFeatures(BaseSchema):
    """Human-friendly plan feature matrix"""
    plan_name: str
    display_name: str
    features: Dict[str, str] = Field(..., description="Feature -> label/value")


class PlanComparison(BaseSchema):
    """Compare multiple plans side by side"""
    plans: List[PlanResponse]
    feature_matrix: Dict[str, Dict[str, object]] = Field(
        ...,
        description="Feature key -> plan_name -> value",
    )