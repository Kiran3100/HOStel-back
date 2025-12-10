"""
Security module for authentication, authorization, and cryptographic operations.

This module provides:
- Password hashing and verification
- JWT token management
- Encryption/decryption utilities
- OAuth integration
- CSRF protection
- Security utilities
"""

from app.core.security.security import SecurityManager, security_manager
from app.core.security.jwt import JWTManager, jwt_manager
from app.core.security.password import PasswordManager, password_manager
from app.core.security.encryption import EncryptionManager, encryption_manager
from app.core.security.oauth import OAuthManager, oauth_manager
from app.core.security.csrf import CSRFManager, csrf_manager

__all__ = [
    "SecurityManager",
    "security_manager",
    "JWTManager",
    "jwt_manager",
    "PasswordManager",
    "password_manager",
    "EncryptionManager",
    "encryption_manager",
    "OAuthManager",
    "oauth_manager",
    "CSRFManager",
    "csrf_manager",
]