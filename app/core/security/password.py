# --- File: app/core/security/password.py ---
"""
Password management utilities.

This module provides:
- Password hashing and verification
- Password strength validation
- Temporary password generation
- Password history management
- Password expiration checking
"""

import re
import secrets
import string
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from app.core.config import settings
from app.core.security.security import security_manager
from app.core.exceptions.validation_exceptions import ValidationException


class PasswordManager:
    """
    Password management system with comprehensive security features.
    
    This class handles:
    - Password hashing and verification
    - Password strength validation
    - Password history tracking
    - Temporary password generation
    - Password expiration management
    """
    
    def __init__(self):
        """Initialize password manager with settings."""
        self.min_length = settings.PASSWORD_MIN_LENGTH
        self.max_length = settings.PASSWORD_MAX_LENGTH
        self.require_uppercase = settings.PASSWORD_REQUIRE_UPPERCASE
        self.require_lowercase = settings.PASSWORD_REQUIRE_LOWERCASE
        self.require_digit = settings.PASSWORD_REQUIRE_DIGIT
        self.require_special = settings.PASSWORD_REQUIRE_SPECIAL
        self.expiry_days = settings.PASSWORD_EXPIRY_DAYS
        self.history_limit = settings.PASSWORD_HISTORY_LIMIT
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using the security manager.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
            
        Example:
            >>> pm = PasswordManager()
            >>> hashed = pm.hash_password("SecurePass123!")
        """
        return security_manager.hash_password(password)
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            hashed_password: Hashed password to verify against
            
        Returns:
            True if password matches, False otherwise
            
        Example:
            >>> pm = PasswordManager()
            >>> is_valid = pm.verify_password("SecurePass123!", hashed)
        """
        return security_manager.verify_password(password, hashed_password)
    
    def generate_temporary_password(self, length: int = 12) -> str:
        """
        Generate a temporary password that meets strength requirements.
        
        Args:
            length: Length of the password (minimum 8)
            
        Returns:
            Generated temporary password
            
        Example:
            >>> pm = PasswordManager()
            >>> temp_pass = pm.generate_temporary_password()
        """
        if length < 8:
            length = 8
        
        # Ensure we have at least one of each required character type
        password_chars = []
        
        if self.require_uppercase:
            password_chars.append(secrets.choice(string.ascii_uppercase))
        
        if self.require_lowercase:
            password_chars.append(secrets.choice(string.ascii_lowercase))
        
        if self.require_digit:
            password_chars.append(secrets.choice(string.digits))
        
        if self.require_special:
            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            password_chars.append(secrets.choice(special_chars))
        
        # Fill the rest with random characters
        all_chars = string.ascii_letters + string.digits
        if self.require_special:
            all_chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        remaining_length = length - len(password_chars)
        for _ in range(remaining_length):
            password_chars.append(secrets.choice(all_chars))
        
        # Shuffle the password characters
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Validate password strength against configured requirements.
        
        Args:
            password: Password to validate
            
        Returns:
            Dictionary with validation results
            
        Example:
            >>> pm = PasswordManager()
            >>> result = pm.validate_password_strength("weak")
            >>> if not result["is_valid"]:
            >>>     print(result["errors"])
        """
        errors = []
        warnings = []
        score = 0
        
        if not password:
            return {
                "is_valid": False,
                "score": 0,
                "strength": "invalid",
                "errors": ["Password cannot be empty"],
                "warnings": []
            }
        
        # Length validation
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters long")
        elif len(password) > self.max_length:
            errors.append(f"Password must not exceed {self.max_length} characters")
        else:
            score += min(len(password) * 2, 20)  # Max 20 points for length
        
        # Character type validation
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        
        if self.require_uppercase and not has_uppercase:
            errors.append("Password must contain at least one uppercase letter")
        elif has_uppercase:
            score += 10
        
        if self.require_lowercase and not has_lowercase:
            errors.append("Password must contain at least one lowercase letter")
        elif has_lowercase:
            score += 10
        
        if self.require_digit and not has_digit:
            errors.append("Password must contain at least one digit")
        elif has_digit:
            score += 10
        
        if self.require_special and not has_special:
            errors.append("Password must contain at least one special character")
        elif has_special:
            score += 15
        
        # Additional strength checks
        if len(set(password)) < len(password) * 0.7:
            warnings.append("Password has too many repeated characters")
            score -= 5
        
        # Check for common patterns
        common_patterns = [
            r'123456',
            r'password',
            r'qwerty',
            r'abc123',
            r'admin',
            r'letmein'
        ]
        
        for pattern in common_patterns:
            if re.search(pattern, password.lower()):
                warnings.append("Password contains common patterns")
                score -= 10
                break
        
        # Check for sequential characters
        if self._has_sequential_chars(password):
            warnings.append("Password contains sequential characters")
            score -= 5
        
        # Determine strength level
        if score >= 70:
            strength = "very_strong"
        elif score >= 50:
            strength = "strong"
        elif score >= 30:
            strength = "medium"
        elif score >= 10:
            strength = "weak"
        else:
            strength = "very_weak"
        
        return {
            "is_valid": len(errors) == 0,
            "score": max(0, score),
            "strength": strength,
            "errors": errors,
            "warnings": warnings,
            "details": {
                "has_uppercase": has_uppercase,
                "has_lowercase": has_lowercase,
                "has_digit": has_digit,
                "has_special": has_special,
                "length": len(password)
            }
        }
    
    def check_password_history(
        self,
        new_password: str,
        password_history: List[str]
    ) -> bool:
        """
        Check if password was used recently.
        
        Args:
            new_password: New password to check
            password_history: List of recent password hashes
            
        Returns:
            True if password is not in history, False if it was used recently
            
        Example:
            >>> pm = PasswordManager()
            >>> is_new = pm.check_password_history(new_pass, user.password_history)
        """
        if not password_history:
            return True
        
        # Check against recent passwords
        recent_passwords = password_history[-self.history_limit:]
        
        for old_password_hash in recent_passwords:
            if self.verify_password(new_password, old_password_hash):
                return False
        
        return True
    
    def is_password_expired(
        self,
        password_created_at: datetime,
        last_changed_at: Optional[datetime] = None
    ) -> bool:
        """
        Check if password has expired.
        
        Args:
            password_created_at: When password was created
            last_changed_at: When password was last changed
            
        Returns:
            True if password has expired
            
        Example:
            >>> pm = PasswordManager()
            >>> is_expired = pm.is_password_expired(user.password_created_at)
        """
        if self.expiry_days <= 0:
            return False  # Password expiry disabled
        
        reference_date = last_changed_at or password_created_at
        expiry_date = reference_date + timedelta(days=self.expiry_days)
        
        return datetime.utcnow() > expiry_date
    
    def get_password_expiry_date(
        self,
        password_created_at: datetime,
        last_changed_at: Optional[datetime] = None
    ) -> Optional[datetime]:
        """
        Get password expiry date.
        
        Args:
            password_created_at: When password was created
            last_changed_at: When password was last changed
            
        Returns:
            Password expiry date or None if expiry is disabled
            
        Example:
            >>> pm = PasswordManager()
            >>> expiry = pm.get_password_expiry_date(user.password_created_at)
        """
        if self.expiry_days <= 0:
            return None
        
        reference_date = last_changed_at or password_created_at
        return reference_date + timedelta(days=self.expiry_days)
    
    def days_until_expiry(
        self,
        password_created_at: datetime,
        last_changed_at: Optional[datetime] = None
    ) -> Optional[int]:
        """
        Get number of days until password expires.
        
        Args:
            password_created_at: When password was created
            last_changed_at: When password was last changed
            
        Returns:
            Days until expiry or None if expiry is disabled
            
        Example:
            >>> pm = PasswordManager()
            >>> days = pm.days_until_expiry(user.password_created_at)
            >>> if days and days <= 7:
            >>>     send_password_expiry_warning(user)
        """
        expiry_date = self.get_password_expiry_date(password_created_at, last_changed_at)
        
        if not expiry_date:
            return None
        
        days_remaining = (expiry_date - datetime.utcnow()).days
        return max(0, days_remaining)
    
    def generate_reset_token(self, length: int = 32) -> str:
        """
        Generate a secure password reset token.
        
        Args:
            length: Length of the token
            
        Returns:
            Secure reset token
            
        Example:
            >>> pm = PasswordManager()
            >>> reset_token = pm.generate_reset_token()
        """
        return security_manager.generate_random_string(
            length=length,
            include_symbols=False,
            exclude_ambiguous=True
        )
    
    def validate_reset_token_format(self, token: str) -> bool:
        """
        Validate reset token format.
        
        Args:
            token: Reset token to validate
            
        Returns:
            True if token format is valid
            
        Example:
            >>> pm = PasswordManager()
            >>> is_valid = pm.validate_reset_token_format(token)
        """
        if not token:
            return False
        
        # Check length and characters
        if len(token) < 16 or len(token) > 64:
            return False
        
        # Should only contain alphanumeric characters
        return re.match(r'^[a-zA-Z0-9]+$', token) is not None
    
    def _has_sequential_chars(self, password: str, min_sequence: int = 3) -> bool:
        """
        Check if password contains sequential characters.
        
        Args:
            password: Password to check
            min_sequence: Minimum sequence length to flag
            
        Returns:
            True if sequential characters found
        """
        password_lower = password.lower()
        
        # Check for ascending sequences
        for i in range(len(password_lower) - min_sequence + 1):
            sequence = password_lower[i:i + min_sequence]
            
            # Check if characters are sequential
            is_sequential = True
            for j in range(1, len(sequence)):
                if ord(sequence[j]) != ord(sequence[j-1]) + 1:
                    is_sequential = False
                    break
            
            if is_sequential:
                return True
        
        # Check for descending sequences
        for i in range(len(password_lower) - min_sequence + 1):
            sequence = password_lower[i:i + min_sequence]
            
            # Check if characters are sequential (descending)
            is_sequential = True
            for j in range(1, len(sequence)):
                if ord(sequence[j]) != ord(sequence[j-1]) - 1:
                    is_sequential = False
                    break
            
            if is_sequential:
                return True
        
        return False
    
    def create_password_policy_message(self) -> str:
        """
        Create a human-readable password policy message.
        
        Returns:
            Password policy description
            
        Example:
            >>> pm = PasswordManager()
            >>> policy = pm.create_password_policy_message()
            >>> print(policy)
        """
        requirements = []
        
        requirements.append(f"Be between {self.min_length} and {self.max_length} characters long")
        
        if self.require_uppercase:
            requirements.append("Contain at least one uppercase letter")
        
        if self.require_lowercase:
            requirements.append("Contain at least one lowercase letter")
        
        if self.require_digit:
            requirements.append("Contain at least one digit")
        
        if self.require_special:
            requirements.append("Contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)")
        
        if self.expiry_days > 0:
            requirements.append(f"Be changed every {self.expiry_days} days")
        
        if self.history_limit > 0:
            requirements.append(f"Not match any of your last {self.history_limit} passwords")
        
        policy = "Your password must:\n"
        for i, req in enumerate(requirements, 1):
            policy += f"{i}. {req}\n"
        
        return policy.strip()


# Global password manager instance
password_manager = PasswordManager()