"""
Hostel response to review schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class HostelResponseCreate(BaseCreateSchema):
    """Create hostel response to review"""
    review_id: UUID = Field(..., description="Review being responded to")
    
    response_text: str = Field(
        ...,
        min_length=20,
        max_length=2000,
        description="Response text"
    )
    
    responded_by: UUID = Field(..., description="Admin/owner responding")


class OwnerResponse(BaseResponseSchema):
    """Owner/hostel response to review"""
    review_id: UUID
    
    response_text: str
    
    responded_by: UUID
    responded_by_name: str
    responded_by_role: str
    
    responded_at: datetime


class ResponseUpdate(BaseCreateSchema):
    """Update hostel response"""
    response_id: UUID
    
    response_text: str = Field(..., min_length=20, max_length=2000)


class ResponseGuidelines(BaseSchema):
    """Guidelines for hostel responses"""
    guidelines: List[str] = Field(
        default_factory=lambda: [
            "Thank the reviewer for their feedback",
            "Address specific concerns mentioned",
            "Be professional and courteous",
            "Explain any misunderstandings",
            "Mention improvements made",
            "Invite them to connect directly if needed"
        ]
    )
    
    best_practices: List[str] = Field(
        default_factory=lambda: [
            "Respond within 48 hours",
            "Personalize your response",
            "Acknowledge both positive and negative points",
            "Don't be defensive or argumentative",
            "Keep it concise and relevant"
        ]
    )


class ResponseStats(BaseSchema):
    """Hostel response statistics"""
    hostel_id: UUID
    
    total_reviews: int
    total_responses: int
    response_rate: Decimal = Field(..., description="% of reviews with responses")
    
    average_response_time_hours: Decimal
    
    # By rating
    response_rate_5_star: Decimal
    response_rate_4_star: Decimal
    response_rate_3_star: Decimal
    response_rate_2_star: Decimal
    response_rate_1_star: Decimal