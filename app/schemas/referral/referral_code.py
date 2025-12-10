"""
Referral code generation/validation schemas
"""
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseSchema


class ReferralCodeGenerate(BaseCreateSchema):
    """Generate referral code for user"""
    user_id: UUID
    program_id: UUID

    # Optional custom prefix
    prefix: str = Field("HOSTEL", max_length=10)


class ReferralCodeResponse(BaseSchema):
    """Referral code response"""
    user_id: UUID
    program_id: UUID
    referral_code: str


class CodeValidationRequest(BaseCreateSchema):
    """Validate referral code"""
    referral_code: str = Field(..., max_length=50)


class CodeValidationResponse(BaseSchema):
    """Validation result"""
    referral_code: str
    is_valid: bool
    program_id: Optional[UUID]
    referrer_id: Optional[UUID]
    message: str