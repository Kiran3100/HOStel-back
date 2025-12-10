"""
Notification schemas package
"""
from app.schemas.notification.notification_base import (
    NotificationBase,
    NotificationCreate,
    NotificationUpdate
)
from app.schemas.notification.notification_response import (
    NotificationResponse,
    NotificationList,
    UnreadCount,
    NotificationDetail
)
from app.schemas.notification.notification_template import (
    TemplateCreate,
    TemplateUpdate,
    TemplateResponse,
    VariableMapping
)
from app.schemas.notification.email_notification import (
    EmailRequest,
    EmailConfig,
    EmailTracking,
    EmailTemplate
)
from app.schemas.notification.sms_notification import (
    SMSRequest,
    SMSConfig,
    DeliveryStatus,
    SMSTemplate
)
from app.schemas.notification.push_notification import (
    PushRequest,
    PushConfig,
    DeviceToken,
    DeviceRegistration,
    PushTemplate
)
from app.schemas.notification.notification_queue import (
    QueueStatus,
    QueuedNotification,
    BatchProcessing,
    QueueStats
)
from app.schemas.notification.notification_preferences import (
    UserPreferences,
    ChannelPreferences,
    FrequencySettings,
    PreferenceUpdate
)
from app.schemas.notification.notification_routing import (
    RoutingConfig,
    HierarchicalRouting,
    EscalationRouting,
    RoutingRule
)

__all__ = [
    # Base
    "NotificationBase",
    "NotificationCreate",
    "NotificationUpdate",
    
    # Response
    "NotificationResponse",
    "NotificationList",
    "UnreadCount",
    "NotificationDetail",
    
    # Template
    "TemplateCreate",
    "TemplateUpdate",
    "TemplateResponse",
    "VariableMapping",
    
    # Email
    "EmailRequest",
    "EmailConfig",
    "EmailTracking",
    "EmailTemplate",
    
    # SMS
    "SMSRequest",
    "SMSConfig",
    "DeliveryStatus",
    "SMSTemplate",
    
    # Push
    "PushRequest",
    "PushConfig",
    "DeviceToken",
    "DeviceRegistration",
    "PushTemplate",
    
    # Queue
    "QueueStatus",
    "QueuedNotification",
    "BatchProcessing",
    "QueueStats",
    
    # Preferences
    "UserPreferences",
    "ChannelPreferences",
    "FrequencySettings",
    "PreferenceUpdate",
    
    # Routing
    "RoutingConfig",
    "HierarchicalRouting",
    "EscalationRouting",
    "RoutingRule",
]