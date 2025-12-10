"""
Announcement delivery schemas
"""
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class DeliveryConfig(BaseSchema):
    """Delivery configuration"""
    announcement_id: UUID
    
    # Channels
    channels: "DeliveryChannels"
    
    # Delivery strategy
    delivery_strategy: str = Field(
        "immediate",
        pattern="^(immediate|scheduled|batched)$"
    )
    
    # Batch settings (if batched)
    batch_size: Optional[int] = Field(None, ge=10, le=1000)
    batch_interval_minutes: Optional[int] = Field(None, ge=1, le=60)


class DeliveryChannels(BaseSchema):
    """Delivery channel settings"""
    email: bool = Field(False)
    sms: bool = Field(False)
    push: bool = Field(True)
    in_app: bool = Field(True)
    
    # Channel priority (for fallback)
    primary_channel: str = Field("push", pattern="^(email|sms|push|in_app)$")
    fallback_channels: List[str] = Field(default_factory=list)


class DeliveryStatus(BaseSchema):
    """Delivery status for announcement"""
    announcement_id: UUID
    
    total_recipients: int
    
    # By channel
    email_sent: int
    email_delivered: int
    email_failed: int
    
    sms_sent: int
    sms_delivered: int
    sms_failed: int
    
    push_sent: int
    push_delivered: int
    push_failed: int
    
    # Overall
    total_delivered: int
    total_failed: int
    delivery_rate: Decimal = Field(..., description="% successfully delivered")
    
    # Timeline
    delivery_started_at: Optional[datetime]
    delivery_completed_at: Optional[datetime]


class DeliveryReport(BaseSchema):
    """Detailed delivery report"""
    announcement_id: UUID
    title: str
    
    # Recipients
    total_recipients: int
    
    # By channel
    channel_breakdown: Dict[str, "ChannelDeliveryStats"]
    
    # By status
    delivered_count: int
    failed_count: int
    pending_count: int
    
    # Failed recipients
    failed_recipients: List["FailedDelivery"] = Field(default_factory=list)
    
    # Timeline
    delivery_duration_minutes: Optional[int]
    
    generated_at: datetime


class ChannelDeliveryStats(BaseSchema):
    """Delivery stats for specific channel"""
    channel: str
    
    sent: int
    delivered: int
    failed: int
    pending: int
    
    delivery_rate: Decimal
    average_delivery_time_seconds: Optional[Decimal]


class FailedDelivery(BaseSchema):
    """Failed delivery record"""
    recipient_id: UUID
    recipient_name: str
    recipient_contact: str
    
    channel: str
    failure_reason: str
    failed_at: datetime
    
    retry_attempted: bool
    retry_successful: Optional[bool]


class BatchDelivery(BaseSchema):
    """Batch delivery progress"""
    announcement_id: UUID
    
    total_batches: int
    completed_batches: int
    current_batch: int
    
    total_recipients: int
    processed_recipients: int
    
    estimated_completion: datetime
    
    status: str = Field(..., pattern="^(processing|completed|failed|paused)$")


class RetryDelivery(BaseCreateSchema):
    """Retry failed deliveries"""
    announcement_id: UUID
    
    # Retry options
    retry_failed_only: bool = Field(True)
    retry_channels: List[str] = Field(default_factory=list, description="Specific channels to retry")
    
    # Specific recipients
    recipient_ids: Optional[List[UUID]] = Field(None, description="Retry specific recipients only")