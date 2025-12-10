"""
Email notification schemas
"""
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import EmailStr, Field, HttpUrl
from uuid import UUID

from app.schemas.common.base import BaseSchema, BaseCreateSchema


class EmailRequest(BaseCreateSchema):
    """Send email notification"""
    recipient_email: EmailStr = Field(..., description="Recipient email address")
    
    # CC and BCC
    cc_emails: List[EmailStr] = Field(default_factory=list)
    bcc_emails: List[EmailStr] = Field(default_factory=list)
    
    # Content
    subject: str = Field(..., min_length=1, max_length=255)
    body_html: str = Field(..., description="HTML email body")
    body_text: Optional[str] = Field(None, description="Plain text fallback")
    
    # Attachments
    attachments: List[HttpUrl] = Field(default_factory=list, description="Attachment URLs")
    
    # Template
    template_code: Optional[str] = None
    template_variables: Optional[Dict[str, str]] = None
    
    # Settings
    reply_to: Optional[EmailStr] = None
    from_name: Optional[str] = Field(None, description="Sender name")
    
    # Tracking
    track_opens: bool = Field(True)
    track_clicks: bool = Field(True)
    
    # Priority
    priority: str = Field("normal", pattern="^(low|normal|high)$")


class EmailConfig(BaseSchema):
    """Email configuration"""
    # SMTP/Service settings
    service_provider: str = Field(..., pattern="^(sendgrid|ses|smtp)$")
    
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_username: Optional[str] = None
    
    # From address
    from_email: EmailStr
    from_name: str
    
    # Reply-to
    reply_to_email: Optional[EmailStr] = None
    
    # Rate limiting
    max_emails_per_hour: int = Field(100, ge=1)
    
    # Tracking
    enable_open_tracking: bool = Field(True)
    enable_click_tracking: bool = Field(True)


class EmailTracking(BaseSchema):
    """Email tracking information"""
    email_id: UUID
    recipient_email: str
    
    # Delivery
    sent_at: datetime
    delivered_at: Optional[datetime]
    bounced_at: Optional[datetime]
    
    delivery_status: str = Field(
        ...,
        pattern="^(sent|delivered|bounced|failed|spam)$"
    )
    
    # Engagement
    opened: bool = Field(False)
    first_opened_at: Optional[datetime]
    open_count: int = Field(0)
    
    clicked: bool = Field(False)
    first_clicked_at: Optional[datetime]
    click_count: int = Field(0)
    
    # Errors
    bounce_type: Optional[str] = Field(None, description="hard/soft bounce")
    error_message: Optional[str]


class EmailTemplate(BaseSchema):
    """Email-specific template"""
    template_code: str
    
    subject: str
    html_body: str
    text_body: Optional[str]
    
    # Styling
    header_image_url: Optional[HttpUrl]
    footer_text: Optional[str]
    
    # Variables
    required_variables: List[str]
    optional_variables: List[str] = Field(default_factory=list)


class BulkEmailRequest(BaseCreateSchema):
    """Send bulk emails"""
    recipients: List[EmailStr] = Field(..., min_items=1, max_items=1000)
    
    subject: str
    body_html: str
    
    # Template
    template_code: Optional[str] = None
    
    # Per-recipient variables
    recipient_variables: Optional[Dict[str, Dict[str, str]]] = Field(
        None,
        description="Email -> variable mapping"
    )
    
    # Batch settings
    batch_size: int = Field(100, ge=10, le=1000)
    delay_between_batches_seconds: int = Field(5, ge=1, le=60)


class EmailStats(BaseSchema):
    """Email statistics"""
    total_sent: int
    total_delivered: int
    total_bounced: int
    total_failed: int
    
    delivery_rate: Decimal
    bounce_rate: Decimal
    
    total_opened: int
    open_rate: Decimal
    
    total_clicked: int
    click_rate: Decimal
    
    # By period
    period_start: date
    period_end: date