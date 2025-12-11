# --- File: app/schemas/subscription/__init__.py ---
"""
Subscription schemas package.

Provides comprehensive schemas for subscription management including
plans, billing, upgrades, cancellations, and commissions.
"""

from __future__ import annotations

# Plan schemas
from app.schemas.subscription.subscription_plan_base import (
    FeatureDefinition,
    PlanComparison,
    PlanCreate,
    PlanFeatures,
    PlanResponse,
    PlanUpdate,
    PlanUsageMetrics,
    SubscriptionPlanBase,
)

# Subscription base schemas
from app.schemas.subscription.subscription_base import (
    SubscriptionBase,
    SubscriptionCreate,
    SubscriptionResponse,
    SubscriptionUpdate,
)

# Billing schemas
from app.schemas.subscription.subscription_billing import (
    BillingCycleInfo,
    BillingHistory,
    BillingHistoryItem,
    GenerateInvoiceRequest,
    InvoiceInfo,
    InvoiceLineItem,
    PaymentRecord,
    UpcomingBilling,
)

# Upgrade/downgrade schemas
from app.schemas.subscription.subscription_upgrade import (
    DowngradeRequest,
    PlanChangeRequest,
    PlanChangeResult,
    ProrationCalculation,
    UpgradePreview,
    UpgradeRequest,
)

# Cancellation schemas
from app.schemas.subscription.subscription_cancellation import (
    CancellationFeedback,
    CancellationPreview,
    CancellationRequest,
    CancellationResponse,
)

# Commission schemas
from app.schemas.subscription.commission import (
    BookingCommissionResponse,
    CommissionConfig,
    CommissionPayoutRequest,
    CommissionPayoutResponse,
    CommissionRate,
    CommissionSummary,
)

__all__ = [
    # Plan
    "SubscriptionPlanBase",
    "PlanCreate",
    "PlanUpdate",
    "PlanResponse",
    "PlanFeatures",
    "PlanComparison",
    "FeatureDefinition",
    "PlanUsageMetrics",
    # Subscription
    "SubscriptionBase",
    "SubscriptionCreate",
    "SubscriptionUpdate",
    "SubscriptionResponse",
    # Billing
    "BillingCycleInfo",
    "GenerateInvoiceRequest",
    "InvoiceInfo",
    "InvoiceLineItem",
    "PaymentRecord",
    "BillingHistory",
    "BillingHistoryItem",
    "UpcomingBilling",
    # Upgrade/Downgrade
    "UpgradeRequest",
    "DowngradeRequest",
    "PlanChangeRequest",
    "UpgradePreview",
    "PlanChangeResult",
    "ProrationCalculation",
    # Cancellation
    "CancellationRequest",
    "CancellationResponse",
    "CancellationPreview",
    "CancellationFeedback",
    # Commission
    "CommissionConfig",
    "CommissionRate",
    "BookingCommissionResponse",
    "CommissionSummary",
    "CommissionPayoutRequest",
    "CommissionPayoutResponse",
]