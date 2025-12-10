"""
Announcement tracking schemas
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema, BaseResponseSchema


class ReadReceipt(BaseCreateSchema):
    """Mark announcement as read"""
    announcement_id: UUID
    student_id: UUID
    
    read_at: datetime = Field(default_factory=datetime.now)
    
    # Reading context
    reading_time_seconds: Optional[int] = Field(None, ge=0, description="Time spent reading")
    device_type: Optional[str] = Field(None, pattern="^(mobile|web|tablet)$")


class ReadReceiptResponse(BaseResponseSchema):
    """Read receipt response"""
    announcement_id: UUID
    student_id: UUID
    read_at: datetime
    
    # If acknowledgment is required
    requires_acknowledgment: bool
    acknowledged: bool


class AcknowledgmentTracking(BaseSchema):
    """Track acknowledgments for announcement"""
    announcement_id: UUID
    
    requires_acknowledgment: bool
    
    total_recipients: int
    acknowledged_count: int
    pending_acknowledgments: int
    
    acknowledgment_rate: Decimal = Field(..., description="% who acknowledged")
    
    # Students pending acknowledgment
    pending_students: List["PendingAcknowledgment"] = Field(default_factory=list)


class PendingAcknowledgment(BaseSchema):
    """Pending acknowledgment"""
    student_id: UUID
    student_name: str
    room_number: Optional[str]
    
    delivered_at: datetime
    read: bool
    read_at: Optional[datetime]


class AcknowledgmentRequest(BaseCreateSchema):
    """Submit acknowledgment"""
    announcement_id: UUID
    student_id: UUID
    
    acknowledged: bool = Field(True)
    acknowledgment_note: Optional[str] = Field(None, max_length=500)


class EngagementMetrics(BaseSchema):
    """Engagement metrics for announcement"""
    announcement_id: UUID
    title: str
    
    # Delivery
    total_recipients: int
    delivered_count: int
    delivery_rate: Decimal
    
    # Reading
    read_count: int
    read_rate: Decimal = Field(..., description="% who read")
    
    average_reading_time_seconds: Optional[Decimal]
    
    # Acknowledgment
    acknowledged_count: int
    acknowledgment_rate: Decimal
    
    # Timing
    average_time_to_read_hours: Optional[Decimal] = Field(
        None,
        description="Average time between delivery and reading"
    )
    
    # Engagement score
    engagement_score: Decimal = Field(..., ge=0, le=100, description="Overall engagement score")


class ReadingTime(BaseSchema):
    """Reading time analytics"""
    announcement_id: UUID
    
    # Statistics
    average_reading_time_seconds: Decimal
    median_reading_time_seconds: Decimal
    min_reading_time_seconds: int
    max_reading_time_seconds: int
    
    # Distribution
    quick_readers: int = Field(..., description="< 30 seconds")
    normal_readers: int = Field(..., description="30-120 seconds")
    thorough_readers: int = Field(..., description="> 120 seconds")


class AnnouncementAnalytics(BaseSchema):
    """Complete announcement analytics"""
    announcement_id: UUID
    title: str
    published_at: datetime
    
    # Delivery metrics
    delivery_metrics: DeliveryStatus
    
    # Engagement metrics
    engagement_metrics: EngagementMetrics
    
    # Reading patterns
    reading_by_hour: dict = Field(..., description="Hour -> read count")
    reading_by_day: dict = Field(..., description="Day -> read count")
    
    # Device breakdown
    reads_by_device: dict = Field(..., description="Device type -> count")