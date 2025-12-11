# --- File: app/schemas/referral/__init__.py ---
"""
Referral schemas package.

Provides comprehensive schemas for referral program management including
programs, referrals, codes, rewards, and analytics.
"""

from __future__ import annotations

# Program schemas
from app.schemas.referral.referral_program_base import (
    ProgramCreate,
    ProgramList,
    ProgramResponse,
    ProgramStats,
    ProgramType,
    ProgramUpdate,
    ReferralProgramBase,
    RewardType,
)

# Referral base schemas
from app.schemas.referral.referral_base import (
    ReferralBase,
    ReferralConversion,
    ReferralCreate,
    ReferralUpdate,
)

# Referral code schemas
from app.schemas.referral.referral_code import (
    CodeValidationRequest,
    CodeValidationResponse,
    ReferralCodeGenerate,
    ReferralCodeResponse,
    ReferralCodeStats,
)

# Response schemas
from app.schemas.referral.referral_response import (
    LeaderboardEntry,
    ReferralAnalytics,
    ReferralDetail,
    ReferralLeaderboard,
    ReferralResponse,
    ReferralStats,
    ReferralTimeline,
    TimelineEvent,
)

# Reward schemas
from app.schemas.referral.referral_rewards import (
    PayoutHistory,
    PayoutRequest,
    PayoutRequestResponse,
    RewardCalculation,
    RewardConfig,
    RewardSummary,
    RewardTracking,
)

__all__ = [
    # Program
    "ReferralProgramBase",
    "ProgramCreate",
    "ProgramUpdate",
    "ProgramResponse",
    "ProgramList",
    "ProgramStats",
    "ProgramType",
    "RewardType",
    # Base
    "ReferralBase",
    "ReferralCreate",
    "ReferralUpdate",
    "ReferralConversion",
    # Code
    "ReferralCodeGenerate",
    "ReferralCodeResponse",
    "CodeValidationRequest",
    "CodeValidationResponse",
    "ReferralCodeStats",
    # Response
    "ReferralResponse",
    "ReferralDetail",
    "ReferralStats",
    "ReferralLeaderboard",
    "LeaderboardEntry",
    "ReferralTimeline",
    "TimelineEvent",
    "ReferralAnalytics",
    # Rewards
    "RewardConfig",
    "RewardTracking",
    "RewardCalculation",
    "PayoutRequest",
    "PayoutRequestResponse",
    "PayoutHistory",
    "RewardSummary",
]