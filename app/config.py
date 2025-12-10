# app/config.py
from __future__ import annotations

import logging
import secrets
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from pydantic import (
    AnyHttpUrl, 
    BaseSettings, 
    EmailStr, 
    Field, 
    HttpUrl, 
    PostgresDsn, 
    SecretStr,
    validator,
    root_validator
)

from app.core.security import JWTSettings


class Environment(str, Enum):
    """Application environment types."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging levels."""
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class SMSProvider(str, Enum):
    """Supported SMS providers."""
    TWILIO = "twilio"
    MSG91 = "msg91"
    TEXTLOCAL = "textlocal"
    AWS_SNS = "aws_sns"
    GUPSHUP = "gupshup"
    FAST2SMS = "fast2sms"


class EmailProvider(str, Enum):
    """Supported email providers."""
    SMTP = "smtp"
    SENDGRID = "sendgrid"
    MAILGUN = "mailgun"
    AWS_SES = "aws_ses"


class CacheBackend(str, Enum):
    """Supported cache backends."""
    REDIS = "redis"
    MEMCACHED = "memcached"
    MEMORY = "memory"


class DatabaseSettings(BaseSettings):
    """Database configuration."""
    
    # Main database
    DATABASE_URL: str = Field("sqlite:///./app.db", env="DATABASE_URL")
    DATABASE_ECHO: bool = Field(False, env="DATABASE_ECHO")
    
    # Connection pool settings
    DATABASE_POOL_SIZE: int = Field(10, env="DATABASE_POOL_SIZE")
    DATABASE_MAX_OVERFLOW: int = Field(20, env="DATABASE_MAX_OVERFLOW")
    DATABASE_POOL_TIMEOUT: int = Field(30, env="DATABASE_POOL_TIMEOUT")
    DATABASE_POOL_RECYCLE: int = Field(3600, env="DATABASE_POOL_RECYCLE")
    
    # Connection retry settings
    DATABASE_RETRY_ATTEMPTS: int = Field(3, env="DATABASE_RETRY_ATTEMPTS")
    DATABASE_RETRY_DELAY: float = Field(1.0, env="DATABASE_RETRY_DELAY")
    
    # Read replica (optional)
    DATABASE_READ_URL: Optional[str] = Field(None, env="DATABASE_READ_URL")
    
    # Backup settings
    BACKUP_RETENTION_DAYS: int = Field(30, env="BACKUP_RETENTION_DAYS")
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v:
            raise ValueError("Database URL cannot be empty")
        
        # Basic validation for common database types
        valid_schemes = ["postgresql", "mysql", "sqlite", "oracle", "mssql"]
        scheme = v.split("://")[0].split("+")[0] if "://" in v else ""
        
        if scheme not in valid_schemes:
            logging.warning(f"Unrecognized database scheme: {scheme}")
        
        return v
    
    @property
    def is_sqlite(self) -> bool:
        """Check if using SQLite."""
        return self.DATABASE_URL.startswith("sqlite")
    
    @property
    def is_postgresql(self) -> bool:
        """Check if using PostgreSQL."""
        return "postgresql" in self.DATABASE_URL
    
    @property
    def is_mysql(self) -> bool:
        """Check if using MySQL."""
        return "mysql" in self.DATABASE_URL


class SecuritySettings(BaseSettings):
    """Security configuration."""
    
    # JWT Settings
    JWT_SECRET_KEY: SecretStr = Field("CHANGE_ME_IN_PRODUCTION", env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(30, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # Password settings
    PASSWORD_MIN_LENGTH: int = Field(8, env="PASSWORD_MIN_LENGTH")
    PASSWORD_REQUIRE_UPPERCASE: bool = Field(True, env="PASSWORD_REQUIRE_UPPERCASE")
    PASSWORD_REQUIRE_LOWERCASE: bool = Field(True, env="PASSWORD_REQUIRE_LOWERCASE")
    PASSWORD_REQUIRE_NUMBERS: bool = Field(True, env="PASSWORD_REQUIRE_NUMBERS")
    PASSWORD_REQUIRE_SPECIAL: bool = Field(True, env="PASSWORD_REQUIRE_SPECIAL")
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = Field(60, env="RATE_LIMIT_PER_MINUTE")
    RATE_LIMIT_PER_HOUR: int = Field(1000, env="RATE_LIMIT_PER_HOUR")
    RATE_LIMIT_PER_DAY: int = Field(10000, env="RATE_LIMIT_PER_DAY")
    
    # Account security
    MAX_LOGIN_ATTEMPTS: int = Field(5, env="MAX_LOGIN_ATTEMPTS")
    ACCOUNT_LOCKOUT_DURATION_MINUTES: int = Field(30, env="ACCOUNT_LOCKOUT_DURATION_MINUTES")
    
    # Session settings
    SESSION_TIMEOUT_MINUTES: int = Field(480, env="SESSION_TIMEOUT_MINUTES")  # 8 hours
    REMEMBER_ME_DAYS: int = Field(30, env="REMEMBER_ME_DAYS")
    
    # HTTPS settings
    FORCE_HTTPS: bool = Field(False, env="FORCE_HTTPS")
    SECURE_COOKIES: bool = Field(False, env="SECURE_COOKIES")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default_factory=list,
        env="BACKEND_CORS_ORIGINS",
        description="Comma-separated list of allowed CORS origins",
    )
    
    # API Security
    API_KEY_HEADER: str = Field("X-API-Key", env="API_KEY_HEADER")
    REQUIRE_API_KEY: bool = Field(False, env="REQUIRE_API_KEY")
    
    @validator("JWT_SECRET_KEY")
    def validate_jwt_secret(cls, v: SecretStr) -> SecretStr:
        """Validate JWT secret key."""
        secret = v.get_secret_value()
        if secret == "CHANGE_ME_IN_PRODUCTION":
            logging.warning("Using default JWT secret key - CHANGE THIS IN PRODUCTION!")
        
        if len(secret) < 32:
            raise ValueError("JWT secret key must be at least 32 characters long")
        
        return v
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError("Invalid CORS origins format")
    
    @property
    def jwt_settings(self) -> JWTSettings:
        """Build JWTSettings instance."""
        return JWTSettings(
            secret_key=self.JWT_SECRET_KEY.get_secret_value(),
            algorithm=self.JWT_ALGORITHM,
            access_token_expires_minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token_expires_days=self.REFRESH_TOKEN_EXPIRE_DAYS,
        )


class EmailSettings(BaseSettings):
    """Email configuration."""
    
    # Provider settings
    EMAIL_PROVIDER: EmailProvider = Field(EmailProvider.SMTP, env="EMAIL_PROVIDER")
    
    # SMTP settings
    SMTP_HOST: str = Field("localhost", env="SMTP_HOST")
    SMTP_PORT: int = Field(587, env="SMTP_PORT")
    SMTP_USERNAME: str = Field("", env="SMTP_USERNAME")
    SMTP_PASSWORD: SecretStr = Field("", env="SMTP_PASSWORD")
    SMTP_USE_TLS: bool = Field(True, env="SMTP_USE_TLS")
    SMTP_USE_SSL: bool = Field(False, env="SMTP_USE_SSL")
    
    # Email settings
    FROM_EMAIL: EmailStr = Field("noreply@example.com", env="FROM_EMAIL")
    FROM_NAME: str = Field("Hostel Management", env="FROM_NAME")
    
    # SendGrid
    SENDGRID_API_KEY: SecretStr = Field("", env="SENDGRID_API_KEY")
    
    # Mailgun
    MAILGUN_API_KEY: SecretStr = Field("", env="MAILGUN_API_KEY")
    MAILGUN_DOMAIN: str = Field("", env="MAILGUN_DOMAIN")
    
    # AWS SES
    AWS_ACCESS_KEY_ID: str = Field("", env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: SecretStr = Field("", env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field("us-east-1", env="AWS_REGION")
    
    # Email limits
    EMAIL_RATE_LIMIT_PER_HOUR: int = Field(100, env="EMAIL_RATE_LIMIT_PER_HOUR")
    EMAIL_BATCH_SIZE: int = Field(50, env="EMAIL_BATCH_SIZE")
    
    # Templates
    EMAIL_TEMPLATE_DIR: str = Field("templates/email", env="EMAIL_TEMPLATE_DIR")
    
    @root_validator
    def validate_email_config(cls, values):
        """Validate email configuration based on provider."""
        provider = values.get("EMAIL_PROVIDER")
        
        if provider == EmailProvider.SMTP:
            required = ["SMTP_HOST", "SMTP_PORT"]
            for field in required:
                if not values.get(field):
                    raise ValueError(f"{field} is required for SMTP provider")
        
        elif provider == EmailProvider.SENDGRID:
            if not values.get("SENDGRID_API_KEY"):
                raise ValueError("SENDGRID_API_KEY is required for SendGrid provider")
        
        elif provider == EmailProvider.MAILGUN:
            required = ["MAILGUN_API_KEY", "MAILGUN_DOMAIN"]
            for field in required:
                if not values.get(field):
                    raise ValueError(f"{field} is required for Mailgun provider")
        
        return values


class SMSSettings(BaseSettings):
    """SMS configuration."""
    
    # Provider settings
    SMS_PROVIDER: SMSProvider = Field(SMSProvider.TWILIO, env="SMS_PROVIDER")
    
    # Twilio
    TWILIO_ACCOUNT_SID: str = Field("", env="TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: SecretStr = Field("", env="TWILIO_AUTH_TOKEN")
    TWILIO_FROM_NUMBER: str = Field("", env="TWILIO_FROM_NUMBER")
    
    # MSG91
    MSG91_API_KEY: SecretStr = Field("", env="MSG91_API_KEY")
    MSG91_SENDER_ID: str = Field("", env="MSG91_SENDER_ID")
    
    # TextLocal
    TEXTLOCAL_API_KEY: SecretStr = Field("", env="TEXTLOCAL_API_KEY")
    TEXTLOCAL_SENDER: str = Field("", env="TEXTLOCAL_SENDER")
    
    # SMS limits
    SMS_RATE_LIMIT_PER_MINUTE: int = Field(100, env="SMS_RATE_LIMIT_PER_MINUTE")
    SMS_RATE_LIMIT_PER_HOUR: int = Field(1000, env="SMS_RATE_LIMIT_PER_HOUR")
    SMS_RATE_LIMIT_PER_DAY: int = Field(10000, env="SMS_RATE_LIMIT_PER_DAY")
    
    # Retry settings
    SMS_RETRY_ATTEMPTS: int = Field(3, env="SMS_RETRY_ATTEMPTS")
    SMS_RETRY_DELAY: float = Field(1.0, env="SMS_RETRY_DELAY")
    SMS_TIMEOUT: int = Field(30, env="SMS_TIMEOUT")
    
    @root_validator
    def validate_sms_config(cls, values):
        """Validate SMS configuration based on provider."""
        provider = values.get("SMS_PROVIDER")
        
        if provider == SMSProvider.TWILIO:
            required = ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN"]
            for field in required:
                if not values.get(field):
                    raise ValueError(f"{field} is required for Twilio provider")
        
        elif provider == SMSProvider.MSG91:
            if not values.get("MSG91_API_KEY"):
                raise ValueError("MSG91_API_KEY is required for MSG91 provider")
        
        elif provider == SMSProvider.TEXTLOCAL:
            if not values.get("TEXTLOCAL_API_KEY"):
                raise ValueError("TEXTLOCAL_API_KEY is required for TextLocal provider")
        
        return values


class FileStorageSettings(BaseSettings):
    """File storage configuration."""
    
    # Local storage
    UPLOAD_DIR: str = Field("uploads", env="UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    ALLOWED_FILE_EXTENSIONS: Set[str] = Field(
        default_factory=lambda: {".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx"},
        env="ALLOWED_FILE_EXTENSIONS"
    )
    
    # AWS S3
    AWS_S3_BUCKET: str = Field("", env="AWS_S3_BUCKET")
    AWS_S3_REGION: str = Field("us-east-1", env="AWS_S3_REGION")
    AWS_S3_ACCESS_KEY: str = Field("", env="AWS_S3_ACCESS_KEY")
    AWS_S3_SECRET_KEY: SecretStr = Field("", env="AWS_S3_SECRET_KEY")
    AWS_S3_CUSTOM_DOMAIN: Optional[str] = Field(None, env="AWS_S3_CUSTOM_DOMAIN")
    
    # File processing
    IMAGE_MAX_WIDTH: int = Field(1920, env="IMAGE_MAX_WIDTH")
    IMAGE_MAX_HEIGHT: int = Field(1080, env="IMAGE_MAX_HEIGHT")
    IMAGE_QUALITY: int = Field(85, env="IMAGE_QUALITY")
    
    @validator("ALLOWED_FILE_EXTENSIONS", pre=True)
    def parse_file_extensions(cls, v):
        """Parse file extensions from string or set."""
        if isinstance(v, str):
            return {ext.strip() for ext in v.split(",") if ext.strip()}
        return v


class CacheSettings(BaseSettings):
    """Cache configuration."""
    
    CACHE_BACKEND: CacheBackend = Field(CacheBackend.MEMORY, env="CACHE_BACKEND")
    
    # Redis
    REDIS_URL: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    REDIS_PASSWORD: SecretStr = Field("", env="REDIS_PASSWORD")
    REDIS_DB: int = Field(0, env="REDIS_DB")
    REDIS_MAX_CONNECTIONS: int = Field(20, env="REDIS_MAX_CONNECTIONS")
    
    # Memcached
    MEMCACHED_SERVERS: List[str] = Field(
        default_factory=lambda: ["127.0.0.1:11211"],
        env="MEMCACHED_SERVERS"
    )
    
    # Cache TTL (seconds)
    CACHE_DEFAULT_TTL: int = Field(300, env="CACHE_DEFAULT_TTL")  # 5 minutes
    CACHE_USER_TTL: int = Field(900, env="CACHE_USER_TTL")  # 15 minutes
    CACHE_SETTINGS_TTL: int = Field(3600, env="CACHE_SETTINGS_TTL")  # 1 hour


class MonitoringSettings(BaseSettings):
    """Monitoring and logging configuration."""
    
    # Logging
    LOG_LEVEL: LogLevel = Field(LogLevel.INFO, env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    LOG_FILE: Optional[str] = Field(None, env="LOG_FILE")
    LOG_ROTATION: str = Field("midnight", env="LOG_ROTATION")
    LOG_RETENTION: int = Field(30, env="LOG_RETENTION")  # days
    
    # Sentry
    SENTRY_DSN: Optional[str] = Field(None, env="SENTRY_DSN")
    SENTRY_ENVIRONMENT: Optional[str] = Field(None, env="SENTRY_ENVIRONMENT")
    SENTRY_RELEASE: Optional[str] = Field(None, env="SENTRY_RELEASE")
    
    # Metrics
    ENABLE_METRICS: bool = Field(True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(9090, env="METRICS_PORT")
    
    # Health checks
    HEALTH_CHECK_ENABLED: bool = Field(True, env="HEALTH_CHECK_ENABLED")
    HEALTH_CHECK_TIMEOUT: int = Field(30, env="HEALTH_CHECK_TIMEOUT")


class PaymentSettings(BaseSettings):
    """Payment gateway configuration."""
    
    # Razorpay (popular in India)
    RAZORPAY_KEY_ID: str = Field("", env="RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET: SecretStr = Field("", env="RAZORPAY_KEY_SECRET")
    RAZORPAY_WEBHOOK_SECRET: SecretStr = Field("", env="RAZORPAY_WEBHOOK_SECRET")
    
    # Stripe
    STRIPE_PUBLISHABLE_KEY: str = Field("", env="STRIPE_PUBLISHABLE_KEY")
    STRIPE_SECRET_KEY: SecretStr = Field("", env="STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET: SecretStr = Field("", env="STRIPE_WEBHOOK_SECRET")
    
    # PayPal
    PAYPAL_CLIENT_ID: str = Field("", env="PAYPAL_CLIENT_ID")
    PAYPAL_CLIENT_SECRET: SecretStr = Field("", env="PAYPAL_CLIENT_SECRET")
    PAYPAL_MODE: str = Field("sandbox", env="PAYPAL_MODE")  # sandbox or live
    
    # Payment settings
    CURRENCY: str = Field("INR", env="CURRENCY")
    PAYMENT_TIMEOUT_MINUTES: int = Field(15, env="PAYMENT_TIMEOUT_MINUTES")


class Settings(BaseSettings):
    """Main application settings."""
    
    # ------------------------------------------------------------------ #
    # General
    # ------------------------------------------------------------------ #
    PROJECT_NAME: str = Field("Hostel Management SaaS API", env="PROJECT_NAME")
    PROJECT_VERSION: str = Field("1.0.0", env="PROJECT_VERSION")
    PROJECT_DESCRIPTION: str = Field(
        "Complete hostel management solution with booking, payments, and analytics",
        env="PROJECT_DESCRIPTION"
    )
    
    ENVIRONMENT: Environment = Field(Environment.DEVELOPMENT, env="ENVIRONMENT")
    DEBUG: bool = Field(False, env="DEBUG")
    
    # API settings
    API_V1_STR: str = Field("/api/v1", env="API_V1_STR")
    API_DOCS_URL: Optional[str] = Field("/docs", env="API_DOCS_URL")
    API_REDOC_URL: Optional[str] = Field("/redoc", env="API_REDOC_URL")
    
    # Server settings
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")
    WORKERS: int = Field(1, env="WORKERS")
    
    # Timezone
    TIMEZONE: str = Field("Asia/Kolkata", env="TIMEZONE")
    
    # ------------------------------------------------------------------ #
    # Sub-configurations
    # ------------------------------------------------------------------ #
    database: DatabaseSettings = DatabaseSettings()
    security: SecuritySettings = SecuritySettings()
    email: EmailSettings = EmailSettings()
    sms: SMSSettings = SMSSettings()
    storage: FileStorageSettings = FileStorageSettings()
    cache: CacheSettings = CacheSettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    payment: PaymentSettings = PaymentSettings()
    
    # ------------------------------------------------------------------ #
    # Feature Flags
    # ------------------------------------------------------------------ #
    FEATURE_REGISTRATION: bool = Field(True, env="FEATURE_REGISTRATION")
    FEATURE_EMAIL_VERIFICATION: bool = Field(True, env="FEATURE_EMAIL_VERIFICATION")
    FEATURE_SMS_VERIFICATION: bool = Field(True, env="FEATURE_SMS_VERIFICATION")
    FEATURE_PAYMENTS: bool = Field(True, env="FEATURE_PAYMENTS")
    FEATURE_ANALYTICS: bool = Field(True, env="FEATURE_ANALYTICS")
    FEATURE_NOTIFICATIONS: bool = Field(True, env="FEATURE_NOTIFICATIONS")
    
    # ------------------------------------------------------------------ #
    # Business Logic
    # ------------------------------------------------------------------ #
    # Booking settings
    BOOKING_ADVANCE_DAYS: int = Field(365, env="BOOKING_ADVANCE_DAYS")
    BOOKING_CANCELLATION_HOURS: int = Field(24, env="BOOKING_CANCELLATION_HOURS")
    BOOKING_MODIFICATION_HOURS: int = Field(2, env="BOOKING_MODIFICATION_HOURS")
    
    # Payment settings
    ADVANCE_PAYMENT_PERCENTAGE: int = Field(20, env="ADVANCE_PAYMENT_PERCENTAGE")
    LATE_PAYMENT_PENALTY_PERCENTAGE: int = Field(5, env="LATE_PAYMENT_PENALTY_PERCENTAGE")
    
    # Notification settings
    NOTIFICATION_REMINDER_HOURS: List[int] = Field(
        default_factory=lambda: [72, 24, 2],
        env="NOTIFICATION_REMINDER_HOURS"
    )
    
    @validator("ENVIRONMENT", pre=True)
    def validate_environment(cls, v):
        """Validate environment."""
        if isinstance(v, str):
            return Environment(v.lower())
        return v
    
    @validator("DEBUG")
    def validate_debug(cls, v, values):
        """Debug should be False in production."""
        env = values.get("ENVIRONMENT")
        if env == Environment.PRODUCTION and v:
            logging.warning("Debug mode is enabled in production environment!")
        return v
    
    @root_validator
    def validate_production_settings(cls, values):
        """Validate production-specific settings."""
        env = values.get("ENVIRONMENT")
        
        if env == Environment.PRODUCTION:
            # Check critical production settings
            security = values.get("security", {})
            if isinstance(security, SecuritySettings):
                jwt_secret = security.JWT_SECRET_KEY.get_secret_value()
                if jwt_secret == "CHANGE_ME_IN_PRODUCTION":
                    raise ValueError("JWT secret must be changed in production")
                
                if not security.FORCE_HTTPS:
                    logging.warning("HTTPS is not enforced in production")
                
                if not security.SECURE_COOKIES:
                    logging.warning("Secure cookies are not enabled in production")
        
        return values
    
    # ------------------------------------------------------------------ #
    # Backward Compatibility Properties
    # ------------------------------------------------------------------ #
    @property
    def DATABASE_URL(self) -> str:
        """Backward compatibility for DATABASE_URL."""
        return self.database.DATABASE_URL
    
    @property
    def JWT_SECRET_KEY(self) -> str:
        """Backward compatibility for JWT_SECRET_KEY."""
        return self.security.JWT_SECRET_KEY.get_secret_value()
    
    @property
    def JWT_ALGORITHM(self) -> str:
        """Backward compatibility for JWT_ALGORITHM."""
        return self.security.JWT_ALGORITHM
    
    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        """Backward compatibility for ACCESS_TOKEN_EXPIRE_MINUTES."""
        return self.security.ACCESS_TOKEN_EXPIRE_MINUTES
    
    @property
    def REFRESH_TOKEN_EXPIRE_DAYS(self) -> int:
        """Backward compatibility for REFRESH_TOKEN_EXPIRE_DAYS."""
        return self.security.REFRESH_TOKEN_EXPIRE_DAYS
    
    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        """Backward compatibility for BACKEND_CORS_ORIGINS."""
        return self.security.BACKEND_CORS_ORIGINS
    
    @property
    def jwt_settings(self) -> JWTSettings:
        """Backward compatibility for jwt_settings."""
        return self.security.jwt_settings
    
    # ------------------------------------------------------------------ #
    # Utility Methods
    # ------------------------------------------------------------------ #
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == Environment.PRODUCTION
    
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT == Environment.DEVELOPMENT
    
    def is_testing(self) -> bool:
        """Check if running in testing."""
        return self.ENVIRONMENT == Environment.TESTING
    
    def get_database_url(self, read_replica: bool = False) -> str:
        """Get database URL (with optional read replica)."""
        if read_replica and self.database.DATABASE_READ_URL:
            return self.database.DATABASE_READ_URL
        return self.database.DATABASE_URL
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins based on environment."""
        if self.is_development():
            return self.security.BACKEND_CORS_ORIGINS + [
                "http://localhost:3000",
                "http://localhost:3001",
                "http://127.0.0.1:3000",
            ]
        return self.security.BACKEND_CORS_ORIGINS
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # Allow extra fields for flexibility
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance.
    
    The @lru_cache decorator ensures this function is only called once,
    and the same Settings instance is returned on subsequent calls.
    """
    try:
        settings = Settings()
        
        # Log configuration summary
        logging.info(f"Application starting with environment: {settings.ENVIRONMENT}")
        logging.info(f"Debug mode: {settings.DEBUG}")
        logging.info(f"Database: {settings.database.DATABASE_URL.split('@')[-1] if '@' in settings.database.DATABASE_URL else 'Local'}")
        
        return settings
        
    except Exception as e:
        logging.error(f"Failed to load settings: {e}")
        raise


def get_test_settings() -> Settings:
    """Get settings for testing (not cached)."""
    return Settings(
        ENVIRONMENT=Environment.TESTING,
        DEBUG=True,
        database=DatabaseSettings(
            DATABASE_URL="sqlite:///./test.db",
            DATABASE_ECHO=False
        ),
        security=SecuritySettings(
            JWT_SECRET_KEY=SecretStr("test-secret-key-32-chars-minimum"),
            ACCESS_TOKEN_EXPIRE_MINUTES=15
        ),
    )


# Global settings instance
settings: Settings = get_settings()


# Configuration validation on import
def validate_configuration() -> None:
    """Validate configuration on application startup."""
    try:
        settings = get_settings()
        
        # Check required directories exist
        upload_dir = Path(settings.storage.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate critical settings in production
        if settings.is_production():
            critical_checks = [
                (settings.security.JWT_SECRET_KEY.get_secret_value() != "CHANGE_ME_IN_PRODUCTION", "JWT secret must be changed"),
                (settings.database.DATABASE_URL != "sqlite:///./app.db", "Production database should not be SQLite"),
                (settings.security.FORCE_HTTPS, "HTTPS should be enforced in production"),
                (settings.monitoring.SENTRY_DSN is not None, "Sentry should be configured in production"),
            ]
            
            for check, message in critical_checks:
                if not check:
                    logging.warning(f"Production configuration warning: {message}")
        
        logging.info("Configuration validation completed successfully")
        
    except Exception as e:
        logging.error(f"Configuration validation failed: {e}")
        raise


# Validate configuration on import
if __name__ != "__main__":
    validate_configuration()