"""
Notification queue schemas
"""
from datetime import datetime
from typing import Optional, List
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.enums import NotificationType, NotificationStatus, Priority


class QueueStatus(BaseSchema):
    """Notification queue status"""
    total_queued: int
    total_processing: int
    total_failed: int
    
    # By priority
    urgent_queued: int
    high_queued: int
    medium_queued: int
    low_queued: int
    
    # By type
    email_queued: int
    sms_queued: int
    push_queued: int
    
    # Processing rate
    avg_processing_time_seconds: Decimal
    throughput_per_minute: Decimal


class QueuedNotification(BaseSchema):
    """Queued notification details"""
    notification_id: UUID
    
    notification_type: NotificationType
    priority: Priority
    status: NotificationStatus
    
    recipient: str = Field(..., description="Email/phone/user_id")
    
    scheduled_at: Optional[datetime]
    queued_at: datetime
    
    retry_count: int
    max_retries: int
    
    estimated_send_time: Optional[datetime]


class BatchProcessing(BaseSchema):
    """Batch processing status"""
    batch_id: UUID
    
    total_notifications: int
    processed: int
    successful: int
    failed: int
    
    status: str = Field(..., pattern="^(queued|processing|completed|failed)$")
    
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    
    estimated_completion: Optional[datetime]


class QueueStats(BaseSchema):
    """Queue statistics"""
    # Current state
    current_queue_size: int
    oldest_queued_age_minutes: Optional[int]
    
    # Today's stats
    today_processed: int
    today_successful: int
    today_failed: int
    
    # Rates
    success_rate: Decimal
    failure_rate: Decimal
    
    # Performance
    average_queue_time_minutes: Decimal
    average_processing_time_seconds: Decimal