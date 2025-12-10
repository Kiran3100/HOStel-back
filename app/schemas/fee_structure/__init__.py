"""
Fee structure & configuration schemas package
"""

from app.schemas.fee_structure.fee_base import (
    FeeStructureBase,
    FeeStructureCreate,
    FeeStructureUpdate,
)
from app.schemas.fee_structure.fee_response import (
    FeeStructureResponse,
    FeeDetail,
    FeeStructureList,
)
from app.schemas.fee_structure.fee_config import (
    FeeConfiguration,
    ChargesBreakdown,
)

__all__ = [
    # Base
    "FeeStructureBase",
    "FeeStructureCreate",
    "FeeStructureUpdate",
    # Response
    "FeeStructureResponse",
    "FeeDetail",
    "FeeStructureList",
    # Config
    "FeeConfiguration",
    "ChargesBreakdown",
]