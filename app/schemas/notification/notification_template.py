"""
Notification template schemas
"""
from typing import Dict, List, Optional
from pydantic import Field
from uuid import UUID

from app.schemas.common.base import BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema, BaseSchema
from app.schemas.common.enums import NotificationType


class TemplateCreate(BaseCreateSchema):
    """Create notification template"""
    template_code: str = Field(..., min_length=3, max_length=100, description="Unique template code")
    template_name: str = Field(..., min_length=3, max_length=255, description="Template name")
    
    template_type: NotificationType = Field(..., description="Email, SMS, or Push")
    
    # Content
    subject: Optional[str] = Field(None, max_length=255, description="Subject (for email/push)")
    body_template: str = Field(..., description="Template with {{variable}} placeholders")
    
    # Variables
    variables: List[str] = Field(..., description="List of required variables")
    
    # Settings
    is_active: bool = Field(True)
    
    # Description
    description: Optional[str] = Field(None, max_length=500)


class TemplateUpdate(BaseUpdateSchema):
    """Update template"""
    template_name: Optional[str] = Field(None, min_length=3, max_length=255)
    subject: Optional[str] = None
    body_template: Optional[str] = None
    variables: Optional[List[str]] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None


class TemplateResponse(BaseResponseSchema):
    """Template response"""
    template_code: str
    template_name: str
    template_type: NotificationType
    
    subject: Optional[str]
    body_template: str
    
    variables: List[str]
    
    is_active: bool
    description: Optional[str]
    
    # Usage stats
    usage_count: int = Field(0, description="Times this template has been used")
    last_used_at: Optional[datetime]


class VariableMapping(BaseSchema):
    """Variable mapping for template rendering"""
    template_code: str
    variables: Dict[str, str] = Field(..., description="Variable name -> value mapping")


class TemplatePreview(BaseCreateSchema):
    """Preview rendered template"""
    template_code: str
    variables: Dict[str, str]


class TemplatePreviewResponse(BaseSchema):
    """Rendered template preview"""
    subject: Optional[str]
    rendered_body: str
    
    # Validation
    all_variables_provided: bool
    missing_variables: List[str] = Field(default_factory=list)


class TemplateList(BaseSchema):
    """List of templates"""
    total_templates: int
    active_templates: int
    
    templates: List[TemplateResponse]


class TemplateCategory(BaseSchema):
    """Template category/group"""
    category_name: str
    templates: List[TemplateResponse]