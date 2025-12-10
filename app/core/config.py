"""
Application configuration management.

This module handles all application settings including:
- Database configuration
- Security settings
- Third-party service credentials
- Feature flags
- Environment-specific settings
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseSettings, Field, validator, PostgresDsn, RedisDsn, AnyHttpUrl
from functools import lru_cache
import os
from pathlib import Path
import secrets


class Settings(BaseSettings):
    """
    Application settings with validation.
    
    All settings can be overridden via environment variables.
    Settings are loaded from .env file in development.
    """

    # ==================== API Configuration ====================
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Hostel Management System"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Comprehensive hostel management platform with multi-tenant support"
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # API Documentation
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"
    SWAGGER_UI_OAUTH2_REDIRECT_URL: str = "/docs/oauth2-redirect"

    # ==================== Server Configuration ====================
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    WORKERS: int = Field(default=4, env="WORKERS")
    RELOAD: bool = Field(default=True, env="RELOAD")
    LOG_LEVEL: str = Field(default="info", env="LOG_LEVEL")

    # ==================== CORS Settings ====================
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:3001",
            "http://localhost:8000",
            "http://127.0.0.1:3000",
        ],
        env="BACKEND_CORS_ORIGINS"
    )

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    CORS_MAX_AGE: int = 600

    # ==================== Database Configuration ====================
    # PostgreSQL
    POSTGRES_HOST: str = Field(default="localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(default=5432, env="POSTGRES_PORT")
    POSTGRES_USER: str = Field(default="postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="postgres", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(default="hostel_management", env="POSTGRES_DB")
    POSTGRES_SCHEMA: str = Field(default="public", env="POSTGRES_SCHEMA")
    DATABASE_URL: Optional[PostgresDsn] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """Construct database URL from components."""
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=str(values.get("POSTGRES_PORT")),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # Database Pool Settings
    DATABASE_ECHO: bool = Field(default=False, env="DATABASE_ECHO")
    DATABASE_POOL_SIZE: int = Field(default=20, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")
    DATABASE_POOL_RECYCLE: int = Field(default=3600, env="DATABASE_POOL_RECYCLE")
    DATABASE_POOL_PRE_PING: bool = Field(default=True, env="DATABASE_POOL_PRE_PING")
    DATABASE_POOL_TIMEOUT: int = Field(default=30, env="DATABASE_POOL_TIMEOUT")

    # ==================== Redis Configuration ====================
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_DB: int = Field(default=0, env="REDIS_DB")
    REDIS_PASSWORD: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    REDIS_URL: Optional[str] = None
    
    # Redis Pool Settings
    REDIS_MAX_CONNECTIONS: int = Field(default=50, env="REDIS_MAX_CONNECTIONS")
    REDIS_SOCKET_TIMEOUT: int = Field(default=5, env="REDIS_SOCKET_TIMEOUT")
    REDIS_SOCKET_CONNECT_TIMEOUT: int = Field(default=5, env="REDIS_SOCKET_CONNECT_TIMEOUT")

    @validator("REDIS_URL", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """Construct Redis URL from components."""
        if isinstance(v, str):
            return v
        
        password = values.get("REDIS_PASSWORD")
        auth = f":{password}@" if password else ""
        
        return f"redis://{auth}{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}/{values.get('REDIS_DB')}"

    # Cache Settings
    REDIS_CACHE_TTL: int = Field(default=300, env="REDIS_CACHE_TTL")
    REDIS_CACHE_PREFIX: str = Field(default="hms:", env="REDIS_CACHE_PREFIX")

    # ==================== JWT & Security Settings ====================
    SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        env="SECRET_KEY"
    )
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # Token Settings
    TOKEN_TYPE: str = "Bearer"
    TOKEN_URL: str = f"{API_V1_PREFIX}/auth/login"

    # Password Policy
    PASSWORD_MIN_LENGTH: int = Field(default=8, env="PASSWORD_MIN_LENGTH")
    PASSWORD_MAX_LENGTH: int = Field(default=128, env="PASSWORD_MAX_LENGTH")
    PASSWORD_REQUIRE_UPPERCASE: bool = Field(default=True, env="PASSWORD_REQUIRE_UPPERCASE")
    PASSWORD_REQUIRE_LOWERCASE: bool = Field(default=True, env="PASSWORD_REQUIRE_LOWERCASE")
    PASSWORD_REQUIRE_DIGIT: bool = Field(default=True, env="PASSWORD_REQUIRE_DIGIT")
    PASSWORD_REQUIRE_SPECIAL: bool = Field(default=True, env="PASSWORD_REQUIRE_SPECIAL")
    PASSWORD_EXPIRY_DAYS: int = Field(default=90, env="PASSWORD_EXPIRY_DAYS")
    PASSWORD_HISTORY_LIMIT: int = Field(default=5, env="PASSWORD_HISTORY_LIMIT")
    
    # Hashing
    BCRYPT_ROUNDS: int = Field(default=12, env="BCRYPT_ROUNDS")

    # ==================== Email Configuration ====================
    # SMTP Settings
    SMTP_HOST: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: str = Field(default="", env="SMTP_USER")
    SMTP_PASSWORD: str = Field(default="", env="SMTP_PASSWORD")
    SMTP_FROM_EMAIL: str = Field(default="noreply@hostel.com", env="SMTP_FROM_EMAIL")
    SMTP_FROM_NAME: str = Field(default="Hostel Management System", env="SMTP_FROM_NAME")
    SMTP_TLS: bool = Field(default=True, env="SMTP_TLS")
    SMTP_SSL: bool = Field(default=False, env="SMTP_SSL")
    
    # Email Settings
    EMAIL_ENABLED: bool = Field(default=True, env="EMAIL_ENABLED")
    EMAIL_TEST_MODE: bool = Field(default=False, env="EMAIL_TEST_MODE")
    EMAIL_TEMPLATES_DIR: str = Field(default="app/templates/emails", env="EMAIL_TEMPLATES_DIR")
    EMAIL_MAX_RETRIES: int = Field(default=3, env="EMAIL_MAX_RETRIES")

    # ==================== SMS Configuration (Twilio) ====================
    SMS_ENABLED: bool = Field(default=False, env="SMS_ENABLED")
    TWILIO_ACCOUNT_SID: Optional[str] = Field(default=None, env="TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: Optional[str] = Field(default=None, env="TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: Optional[str] = Field(default=None, env="TWILIO_PHONE_NUMBER")
    SMS_MAX_RETRIES: int = Field(default=3, env="SMS_MAX_RETRIES")

    # ==================== File Upload Configuration ====================
    UPLOAD_DIR: Path = Field(default=Path("storage/uploads"), env="UPLOAD_DIR")
    MAX_UPLOAD_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_UPLOAD_SIZE")  # 10MB
    MAX_IMAGE_SIZE: int = Field(default=5 * 1024 * 1024, env="MAX_IMAGE_SIZE")  # 5MB
    MAX_DOCUMENT_SIZE: int = Field(default=10 * 1024 * 1024, env="MAX_DOCUMENT_SIZE")  # 10MB
    
    ALLOWED_IMAGE_EXTENSIONS: List[str] = Field(
        default=[".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
        env="ALLOWED_IMAGE_EXTENSIONS"
    )
    ALLOWED_DOCUMENT_EXTENSIONS: List[str] = Field(
        default=[".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".txt"],
        env="ALLOWED_DOCUMENT_EXTENSIONS"
    )
    
    # Image Processing
    IMAGE_THUMBNAIL_SIZE: tuple = (150, 150)
    IMAGE_MEDIUM_SIZE: tuple = (500, 500)
    IMAGE_LARGE_SIZE: tuple = (1200, 1200)
    IMAGE_QUALITY: int = Field(default=85, env="IMAGE_QUALITY")

    # ==================== AWS S3 Configuration ====================
    USE_S3: bool = Field(default=False, env="USE_S3")
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(default="us-east-1", env="AWS_REGION")
    AWS_S3_BUCKET: Optional[str] = Field(default=None, env="AWS_S3_BUCKET")
    AWS_S3_CUSTOM_DOMAIN: Optional[str] = Field(default=None, env="AWS_S3_CUSTOM_DOMAIN")
    AWS_S3_ENDPOINT_URL: Optional[str] = Field(default=None, env="AWS_S3_ENDPOINT_URL")

    # ==================== Payment Gateway Configuration ====================
    # Razorpay
    RAZORPAY_ENABLED: bool = Field(default=False, env="RAZORPAY_ENABLED")
    RAZORPAY_KEY_ID: Optional[str] = Field(default=None, env="RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET: Optional[str] = Field(default=None, env="RAZORPAY_KEY_SECRET")
    RAZORPAY_WEBHOOK_SECRET: Optional[str] = Field(default=None, env="RAZORPAY_WEBHOOK_SECRET")

    # Stripe
    STRIPE_ENABLED: bool = Field(default=False, env="STRIPE_ENABLED")
    STRIPE_PUBLISHABLE_KEY: Optional[str] = Field(default=None, env="STRIPE_PUBLISHABLE_KEY")
    STRIPE_SECRET_KEY: Optional[str] = Field(default=None, env="STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET: Optional[str] = Field(default=None, env="STRIPE_WEBHOOK_SECRET")

    # PayTM
    PAYTM_ENABLED: bool = Field(default=False, env="PAYTM_ENABLED")
    PAYTM_MERCHANT_ID: Optional[str] = Field(default=None, env="PAYTM_MERCHANT_ID")
    PAYTM_MERCHANT_KEY: Optional[str] = Field(default=None, env="PAYTM_MERCHANT_KEY")
    PAYTM_WEBSITE: str = Field(default="WEBSTAGING", env="PAYTM_WEBSITE")
    PAYTM_INDUSTRY_TYPE: str = Field(default="Retail", env="PAYTM_INDUSTRY_TYPE")

    # ==================== Elasticsearch Configuration ====================
    ELASTICSEARCH_ENABLED: bool = Field(default=False, env="ELASTICSEARCH_ENABLED")
    ELASTICSEARCH_HOST: str = Field(default="localhost", env="ELASTICSEARCH_HOST")
    ELASTICSEARCH_PORT: int = Field(default=9200, env="ELASTICSEARCH_PORT")
    ELASTICSEARCH_INDEX_PREFIX: str = Field(default="hms", env="ELASTICSEARCH_INDEX_PREFIX")
    ELASTICSEARCH_USER: Optional[str] = Field(default=None, env="ELASTICSEARCH_USER")
    ELASTICSEARCH_PASSWORD: Optional[str] = Field(default=None, env="ELASTICSEARCH_PASSWORD")

    # ==================== Celery Configuration ====================
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/1",
        env="CELERY_BROKER_URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/2",
        env="CELERY_RESULT_BACKEND"
    )
    CELERY_TASK_TRACK_STARTED: bool = True
    CELERY_TASK_TIME_LIMIT: int = Field(default=30 * 60, env="CELERY_TASK_TIME_LIMIT")  # 30 minutes
    CELERY_TASK_SOFT_TIME_LIMIT: int = Field(default=25 * 60, env="CELERY_TASK_SOFT_TIME_LIMIT")  # 25 minutes

    # ==================== Rate Limiting Configuration ====================
    RATE_LIMIT_ENABLED: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")
    RATE_LIMIT_PER_DAY: int = Field(default=10000, env="RATE_LIMIT_PER_DAY")
    
    # Specific rate limits
    RATE_LIMIT_LOGIN: int = Field(default=5, env="RATE_LIMIT_LOGIN")  # per minute
    RATE_LIMIT_UPLOAD: int = Field(default=10, env="RATE_LIMIT_UPLOAD")  # per minute
    RATE_LIMIT_API: int = Field(default=100, env="RATE_LIMIT_API")  # per minute

    # ==================== Logging Configuration ====================
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    LOG_FILE: Optional[Path] = Field(default=Path("logs/app.log"), env="LOG_FILE")
    LOG_ROTATION: str = Field(default="1 day", env="LOG_ROTATION")
    LOG_RETENTION: str = Field(default="30 days", env="LOG_RETENTION")
    LOG_COMPRESSION: str = Field(default="zip", env="LOG_COMPRESSION")
    
    # Structured Logging
    LOG_JSON_FORMAT: bool = Field(default=False, env="LOG_JSON_FORMAT")
    LOG_INCLUDE_TRACE: bool = Field(default=True, env="LOG_INCLUDE_TRACE")

    # ==================== Monitoring & Observability ====================
    # Sentry
    SENTRY_ENABLED: bool = Field(default=False, env="SENTRY_ENABLED")
    SENTRY_DSN: Optional[str] = Field(default=None, env="SENTRY_DSN")
    SENTRY_ENVIRONMENT: Optional[str] = Field(default=None, env="SENTRY_ENVIRONMENT")
    SENTRY_TRACES_SAMPLE_RATE: float = Field(default=1.0, env="SENTRY_TRACES_SAMPLE_RATE")
    
    # Metrics
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(default=9090, env="METRICS_PORT")

    # ==================== Business Logic Configuration ====================
    # Currency
    DEFAULT_CURRENCY: str = Field(default="INR", env="DEFAULT_CURRENCY")
    SUPPORTED_CURRENCIES: List[str] = Field(default=["INR", "USD"], env="SUPPORTED_CURRENCIES")
    
    # Booking
    BOOKING_ADVANCE_PERCENTAGE: float = Field(default=20.0, env="BOOKING_ADVANCE_PERCENTAGE")
    BOOKING_EXPIRY_HOURS: int = Field(default=24, env="BOOKING_EXPIRY_HOURS")
    MIN_BOOKING_DURATION_DAYS: int = Field(default=30, env="MIN_BOOKING_DURATION_DAYS")
    MAX_BOOKING_DURATION_DAYS: int = Field(default=365, env="MAX_BOOKING_DURATION_DAYS")
    BOOKING_CANCELLATION_DEADLINE_HOURS: int = Field(default=48, env="BOOKING_CANCELLATION_DEADLINE_HOURS")
    
    # Payment
    PAYMENT_REMINDER_DAYS_BEFORE: int = Field(default=3, env="PAYMENT_REMINDER_DAYS_BEFORE")
    LATE_FEE_PERCENTAGE: float = Field(default=5.0, env="LATE_FEE_PERCENTAGE")
    REFUND_PROCESSING_DAYS: int = Field(default=7, env="REFUND_PROCESSING_DAYS")
    
    # Supervisor Approval Thresholds
    SUPERVISOR_COMPLAINT_APPROVAL_THRESHOLD: float = Field(
        default=5000.0,
        env="SUPERVISOR_COMPLAINT_APPROVAL_THRESHOLD"
    )
    SUPERVISOR_MAINTENANCE_APPROVAL_THRESHOLD: float = Field(
        default=10000.0,
        env="SUPERVISOR_MAINTENANCE_APPROVAL_THRESHOLD"
    )
    AUTO_APPROVE_THRESHOLD: float = Field(default=1000.0, env="AUTO_APPROVE_THRESHOLD")

    # ==================== Pagination Configuration ====================
    DEFAULT_PAGE: int = Field(default=1, env="DEFAULT_PAGE")
    DEFAULT_PAGE_SIZE: int = Field(default=20, env="DEFAULT_PAGE_SIZE")
    MAX_PAGE_SIZE: int = Field(default=100, env="MAX_PAGE_SIZE")

    # ==================== Session Configuration ====================
    SESSION_EXPIRE_MINUTES: int = Field(default=60, env="SESSION_EXPIRE_MINUTES")
    SESSION_COOKIE_NAME: str = Field(default="session_id", env="SESSION_COOKIE_NAME")
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SECURE: bool = Field(default=False, env="SESSION_COOKIE_SECURE")  # Set to True in production
    SESSION_COOKIE_SAMESITE: str = Field(default="lax", env="SESSION_COOKIE_SAMESITE")

    # ==================== OTP Configuration ====================
    OTP_LENGTH: int = Field(default=6, env="OTP_LENGTH")
    OTP_EXPIRE_MINUTES: int = Field(default=10, env="OTP_EXPIRE_MINUTES")
    OTP_MAX_ATTEMPTS: int = Field(default=3, env="OTP_MAX_ATTEMPTS")
    OTP_RESEND_DELAY_SECONDS: int = Field(default=60, env="OTP_RESEND_DELAY_SECONDS")

    # ==================== External Services ====================
    # Google Maps
    GOOGLE_MAPS_API_KEY: Optional[str] = Field(default=None, env="GOOGLE_MAPS_API_KEY")
    GOOGLE_MAPS_ENABLED: bool = Field(default=False, env="GOOGLE_MAPS_ENABLED")
    
    # Firebase (Push Notifications)
    FIREBASE_ENABLED: bool = Field(default=False, env="FIREBASE_ENABLED")
    FIREBASE_CREDENTIALS_PATH: Optional[Path] = Field(
        default=None,
        env="FIREBASE_CREDENTIALS_PATH"
    )
    
    # OAuth
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None, env="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(default=None, env="GOOGLE_CLIENT_SECRET")
    FACEBOOK_APP_ID: Optional[str] = Field(default=None, env="FACEBOOK_APP_ID")
    FACEBOOK_APP_SECRET: Optional[str] = Field(default=None, env="FACEBOOK_APP_SECRET")

    # ==================== Feature Flags ====================
    FEATURE_ONLINE_BOOKING: bool = Field(default=True, env="FEATURE_ONLINE_BOOKING")
    FEATURE_PAYMENT_GATEWAY: bool = Field(default=True, env="FEATURE_PAYMENT_GATEWAY")
    FEATURE_SMS_NOTIFICATIONS: bool = Field(default=False, env="FEATURE_SMS_NOTIFICATIONS")
    FEATURE_PUSH_NOTIFICATIONS: bool = Field(default=False, env="FEATURE_PUSH_NOTIFICATIONS")
    FEATURE_ANALYTICS: bool = Field(default=True, env="FEATURE_ANALYTICS")
    FEATURE_REVIEWS: bool = Field(default=True, env="FEATURE_REVIEWS")
    FEATURE_REFERRALS: bool = Field(default=True, env="FEATURE_REFERRALS")

    # ==================== Search Configuration ====================
    SEARCH_MIN_QUERY_LENGTH: int = Field(default=2, env="SEARCH_MIN_QUERY_LENGTH")
    SEARCH_MAX_RESULTS: int = Field(default=100, env="SEARCH_MAX_RESULTS")
    SEARCH_FUZZY_DISTANCE: int = Field(default=2, env="SEARCH_FUZZY_DISTANCE")
    DEFAULT_SEARCH_RADIUS_KM: int = Field(default=10, env="DEFAULT_SEARCH_RADIUS_KM")
    MAX_SEARCH_RADIUS_KM: int = Field(default=50, env="MAX_SEARCH_RADIUS_KM")

    # ==================== Review Configuration ====================
    MIN_REVIEW_LENGTH: int = Field(default=10, env="MIN_REVIEW_LENGTH")
    MAX_REVIEW_LENGTH: int = Field(default=1000, env="MAX_REVIEW_LENGTH")
    MIN_RATING: int = Field(default=1, env="MIN_RATING")
    MAX_RATING: int = Field(default=5, env="MAX_RATING")
    REVIEW_MODERATION_ENABLED: bool = Field(default=True, env="REVIEW_MODERATION_ENABLED")

    # ==================== Complaint Configuration ====================
    COMPLAINT_AUTO_ESCALATE_DAYS: int = Field(default=3, env="COMPLAINT_AUTO_ESCALATE_DAYS")
    COMPLAINT_AUTO_CLOSE_DAYS: int = Field(default=30, env="COMPLAINT_AUTO_CLOSE_DAYS")

    # ==================== Maintenance Configuration ====================
    PREVENTIVE_MAINTENANCE_ADVANCE_DAYS: int = Field(
        default=7,
        env="PREVENTIVE_MAINTENANCE_ADVANCE_DAYS"
    )

    # ==================== Attendance Configuration ====================
    LATE_ARRIVAL_THRESHOLD_MINUTES: int = Field(default=30, env="LATE_ARRIVAL_THRESHOLD_MINUTES")
    ABSENCE_NOTIFICATION_DELAY_HOURS: int = Field(default=2, env="ABSENCE_NOTIFICATION_DELAY_HOURS")

    # ==================== Data Retention ====================
    REPORT_RETENTION_DAYS: int = Field(default=90, env="REPORT_RETENTION_DAYS")
    AUDIT_LOG_RETENTION_DAYS: int = Field(default=365, env="AUDIT_LOG_RETENTION_DAYS")
    SESSION_CLEANUP_DAYS: int = Field(default=30, env="SESSION_CLEANUP_DAYS")
    NOTIFICATION_RETENTION_DAYS: int = Field(default=90, env="NOTIFICATION_RETENTION_DAYS")

    # ==================== Testing Configuration ====================
    TESTING: bool = Field(default=False, env="TESTING")
    TEST_DATABASE_URL: Optional[str] = Field(default=None, env="TEST_DATABASE_URL")

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing."""
        return self.ENVIRONMENT.lower() == "testing" or self.TESTING


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Cached Settings instance
    """
    return Settings()


# Global settings instance
settings = get_settings()


# Validate critical settings on import
def validate_settings():
    """Validate critical settings."""
    if settings.is_production:
        # Check critical production settings
        if settings.SECRET_KEY == secrets.token_urlsafe(32):
            raise ValueError("SECRET_KEY must be set in production")
        
        if not settings.DATABASE_URL:
            raise ValueError("DATABASE_URL must be set in production")
        
        if settings.DEBUG:
            raise ValueError("DEBUG must be False in production")


# Run validation
if settings.is_production:
    validate_settings()