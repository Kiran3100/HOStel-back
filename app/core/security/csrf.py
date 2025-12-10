"""
CSRF (Cross-Site Request Forgery) protection utilities.

This module provides:
- CSRF token generation
- CSRF token validation
- Token lifecycle management
"""

import secrets
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from app.core.config import settings


class CSRFManager:
    """
    CSRF token manager for protecting against cross-site request forgery attacks.
    
    Implements double-submit cookie pattern with HMAC signing.
    """
    
    def __init__(self):
        """Initialize CSRF manager with settings."""
        self.secret_key = settings.SECRET_KEY
        self.token_expiry_hours = 24
        self.token_length = 32
    
    def generate_csrf_token(
        self,
        session_id: Optional[str] = None
    ) -> str:
        """
        Generate a CSRF token.
        
        Args:
            session_id: User session ID (optional, for additional binding)
            
        Returns:
            CSRF token string
            
        Example:
            >>> csrf = CSRFManager()
            >>> token = csrf.generate_csrf_token(session_id="abc123")
            >>> # Store token in user's session
        """
        # Generate random token
        random_token = secrets.token_urlsafe(self.token_length)
        
        # Create timestamp
        timestamp = datetime.utcnow().isoformat()
        
        # Create signature
        message = f"{session_id or 'anonymous'}:{random_token}:{timestamp}"
        signature = self._create_signature(message)
        
        # Combine all parts
        csrf_token = f"{random_token}:{timestamp}:{signature}"
        
        return csrf_token
    
    def validate_csrf_token(
        self,
        csrf_token: str,
        session_id: Optional[str] = None
    ) -> bool:
        """
        Validate a CSRF token.
        
        Args:
            csrf_token: CSRF token to validate
            session_id: User session ID (must match generation)
            
        Returns:
            True if token is valid, False otherwise
            
        Example:
            >>> csrf = CSRFManager()
            >>> is_valid = csrf.validate_csrf_token(token, session_id="abc123")
            >>> if not is_valid:
            >>>     raise SecurityException("Invalid CSRF token")
        """
        try:
            # Parse token
            parts = csrf_token.split(':')
            if len(parts) != 3:
                return False
            
            random_token, timestamp, signature = parts
            
            # Verify timestamp
            try:
                token_time = datetime.fromisoformat(timestamp)
            except ValueError:
                return False
            
            expiry_time = token_time + timedelta(hours=self.token_expiry_hours)
            
            if datetime.utcnow() > expiry_time:
                return False
            
            # Verify signature
            message = f"{session_id or 'anonymous'}:{random_token}:{timestamp}"
            expected_signature = self._create_signature(message)
            
            return self._constant_time_compare(signature, expected_signature)
            
        except Exception:
            return False
    
    def _create_signature(self, message: str) -> str:
        """
        Create HMAC signature for message.
        
        Args:
            message: Message to sign
            
        Returns:
            Hexadecimal signature
        """
        return hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _constant_time_compare(self, a: str, b: str) -> bool:
        """
        Compare two strings in constant time.
        
        Args:
            a: First string
            b: Second string
            
        Returns:
            True if strings match
        """
        return hmac.compare_digest(a, b)
    
    def generate_token_pair(
        self,
        session_id: Optional[str] = None
    ) -> tuple[str, str]:
        """
        Generate a pair of CSRF tokens (for cookie and form).
        
        Args:
            session_id: User session ID
            
        Returns:
            Tuple of (cookie_token, form_token)
            
        Example:
            >>> csrf = CSRFManager()
            >>> cookie_token, form_token = csrf.generate_token_pair(session_id)
            >>> # Set cookie_token in HTTP-only cookie
            >>> # Include form_token in forms
        """
        token = self.generate_csrf_token(session_id)
        return token, token
    
    def is_token_expired(self, csrf_token: str) -> bool:
        """
        Check if CSRF token is expired.
        
        Args:
            csrf_token: CSRF token to check
            
        Returns:
            True if expired, False otherwise
            
        Example:
            >>> csrf = CSRFManager()
            >>> if csrf.is_token_expired(token):
            >>>     print("Token has expired")
        """
        try:
            parts = csrf_token.split(':')
            if len(parts) != 3:
                return True
            
            _, timestamp, _ = parts
            token_time = datetime.fromisoformat(timestamp)
            expiry_time = token_time + timedelta(hours=self.token_expiry_hours)
            
            return datetime.utcnow() > expiry_time
            
        except Exception:
            return True
    
    def get_token_age(self, csrf_token: str) -> Optional[timedelta]:
        """
        Get age of CSRF token.
        
        Args:
            csrf_token: CSRF token
            
        Returns:
            Token age as timedelta or None if invalid
            
        Example:
            >>> csrf = CSRFManager()
            >>> age = csrf.get_token_age(token)
            >>> if age and age.total_seconds() > 3600:
            >>>     print("Token is more than 1 hour old")
        """
        try:
            parts = csrf_token.split(':')
            if len(parts) != 3:
                return None
            
            _, timestamp, _ = parts
            token_time = datetime.fromisoformat(timestamp)
            
            return datetime.utcnow() - token_time
            
        except Exception:
            return None


# Global CSRF manager instance
csrf_manager = CSRFManager()