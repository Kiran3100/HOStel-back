"""
Settings management for different environments.

This module provides environment-specific settings configurations:
- Development: Full debugging, verbose logging
- Production: Optimized, secure settings
- Testing: Isolated test database, disabled external services
- Staging: Production-like with some debugging enabled
"""

from typing import Dict, Any, Type
from app.core.config import Settings


class DevelopmentSettings(Settings):
    """Development environment settings."""
    
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    DATABASE_ECHO: bool = True
    RELOAD: bool = True
    LOG_LEVEL: str = "DEBUG"
    LOG_JSON_FORMAT: bool = False
    
    # Relaxed CORS for development
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:8000",
    ]
    
    # Disable rate limiting in development
    RATE_LIMIT_ENABLED: bool = False
    
    # Fast password hashing for development
    BCRYPT_ROUNDS: int = 4
    
    # Email testing
    EMAIL_TEST_MODE: bool = True
    
    # Disable external services by default
    SMS_ENABLED: bool = False
    ELASTICSEARCH_ENABLED: bool = False
    SENTRY_ENABLED: bool = False


class ProductionSettings(Settings):
    """Production environment settings."""
    
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    DATABASE_ECHO: bool = False
    RELOAD: bool = False
    LOG_LEVEL: str = "INFO"
    LOG_JSON_FORMAT: bool = True
    
    # Strict CORS
    CORS_ALLOW_CREDENTIALS: bool = True
    
    # Enable rate limiting
    RATE_LIMIT_ENABLED: bool = True
    
    # Secure cookies
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "strict"
    
    # Strong password hashing
    BCRYPT_ROUNDS: int = 12
    
    # Enable monitoring
    SENTRY_ENABLED: bool = True
    ENABLE_METRICS: bool = True
    
    # Production should use environment variables for sensitive data
    # Never commit production secrets to version control


class TestingSettings(Settings):
    """Testing environment settings."""
    
    DEBUG: bool = True
    ENVIRONMENT: str = "testing"
    TESTING: bool = True
    DATABASE_ECHO: bool = False
    LOG_LEVEL: str = "WARNING"
    
    # Use test database
    POSTGRES_DB: str = "hostel_management_test"
    
    # Disable rate limiting for tests
    RATE_LIMIT_ENABLED: bool = False
    
    # Fast hashing for tests
    BCRYPT_ROUNDS: int = 4
    
    # Disable external services
    EMAIL_ENABLED: bool = False
    SMS_ENABLED: bool = False
    ELASTICSEARCH_ENABLED: bool = False
    SENTRY_ENABLED: bool = False
    
    # Disable async tasks
    CELERY_TASK_ALWAYS_EAGER: bool = True
    CELERY_TASK_EAGER_PROPAGATES: bool = True
    
    # Short token expiry for tests
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1


class StagingSettings(Settings):
    """Staging environment settings."""
    
    DEBUG: bool = False
    ENVIRONMENT: str = "staging"
    DATABASE_ECHO: bool = False
    RELOAD: bool = False
    LOG_LEVEL: str = "INFO"
    LOG_JSON_FORMAT: bool = True
    
    # Enable monitoring
    SENTRY_ENABLED: bool = True
    ENABLE_METRICS: bool = True
    
    # Similar to production but less strict
    RATE_LIMIT_ENABLED: bool = True
    SESSION_COOKIE_SECURE: bool = True


def get_settings_by_environment(env: str = "development") -> Settings:
    """
    Get settings based on environment.
    
    Args:
        env: Environment name (development, production, testing, staging)
        
    Returns:
        Settings instance for the specified environment
    """
    settings_map: Dict[str, Type[Settings]] = {
        "development": DevelopmentSettings,
        "production": ProductionSettings,
        "testing": TestingSettings,
        "staging": StagingSettings,
    }
    
    settings_class = settings_map.get(env.lower(), DevelopmentSettings)
    return settings_class()


def get_database_url(env: str = "development", test: bool = False) -> str:
    """
    Get database URL for specific environment.
    
    Args:
        env: Environment name
        test: Whether to use test database
        
    Returns:
        Database URL string
    """
    settings = get_settings_by_environment(env)
    
    if test:
        return settings.TEST_DATABASE_URL or settings.DATABASE_URL.replace(
            settings.POSTGRES_DB,
            f"{settings.POSTGRES_DB}_test"
        )
    
    return str(settings.DATABASE_URL)