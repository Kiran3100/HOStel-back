"""
SMS notification schemas
"""
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class SMSRequest(BaseCreateSchema):
    """Send SMS notification"""
    recipient_phone: str = Field(..., pattern=r'^\+?[1-9]\d{9,14}$', description="Phone number")
    
    message: str = Field(..., min_length=1, max_length=160, description="SMS message (160 chars)")
    
    # Template
    template_code: Optional[str] = None
    template_variables: Optional[Dict[str, str]] = None
    
    # Settings
    sender_id: Optional[str] = Field(None, max_length=11, description="Sender ID/Name")
    
    # Priority
    priority: str = Field("normal", pattern="^(low|normal|high)$")
    
    # DLT (India-specific)
    dlt_template_id: Optional[str] = Field(None, description="DLT template ID for India")


class SMSConfig(BaseSchema):
    """SMS configuration"""
    # Service provider
    service_provider: str = Field(..., pattern="^(twilio|aws_sns|msg91|custom)$")
    
    # Credentials
    account_sid: Optional[str] = None
    auth_token: Optional[str] = None
    
    # Sender
    default_sender_id: str = Field(..., max_length=11)
    
    # Rate limiting
    max_sms_per_hour: int = Field(100, ge=1)
    max_sms_per_day: int = Field(1000, ge=1)
    
    # Country settings
    default_country_code: str = Field("+91", description="Default country code")


class DeliveryStatus(BaseSchema):
    """SMS delivery status"""
    sms_id: UUID
    recipient_phone: str
    
    # Status
    status: str = Field(
        ...,
        pattern="^(queued|sent|delivered|failed|undelivered)$"
    )
    
    # Timeline
    queued_at: datetime
    sent_at: Optional[datetime]
    delivered_at: Optional[datetime]
    failed_at: Optional[datetime]
    
    # Error
    error_code: Optional[str]
    error_message: Optional[str]
    
    # Provider details
    provider_message_id: Optional[str]
    segments_count: int = Field(1, description="Number of SMS segments")
    
    # Cost
    cost: Optional[Decimal] = Field(None, description="Cost per SMS")


class SMSTemplate(BaseSchema):
    """SMS template"""
    template_code: str
    message_template: str = Field(..., max_length=160)
    
    # Variables
    required_variables: List[str]
    
    # DLT (India)
    dlt_template_id: Optional[str]
    dlt_approved: bool = Field(False)


class BulkSMSRequest(BaseCreateSchema):
    """Send bulk SMS"""
    recipients: List[str] = Field(
        ...,
        min_items=1,
        max_items=10000,
        description="List of phone numbers"
    )
    
    message: str = Field(..., max_length=160)
    
    # Template
    template_code: Optional[str] = None
    
    # Per-recipient variables
    recipient_variables: Optional[Dict[str, Dict[str, str]]] = None
    
    # Batch settings
    batch_size: int = Field(100, ge=10, le=1000)
    delay_between_batches_seconds: int = Field(2, ge=1, le=10)


class SMSStats(BaseSchema):
    """SMS statistics"""
    total_sent: int
    total_delivered: int
    total_failed: int
    
    delivery_rate: Decimal
    failure_rate: Decimal
    
    # Cost
    total_cost: Decimal
    average_cost_per_sms: Decimal
    
    # Segments
    total_segments: int
    average_segments_per_sms: Decimal
    
    period_start: date
    period_end: date