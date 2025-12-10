"""
Core application components package.

This package contains fundamental application components including:
- Configuration management
- Security utilities
- Permission and authorization
- Middleware components
- Exception handling
- Utilities and helpers
"""

from app.core.config import settings, get_settings
from app.core.constants import *
from app.core.enums import *

__version__ = "1.0.0"

__all__ = [
    "settings",
    "get_settings",
]