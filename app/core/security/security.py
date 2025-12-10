# --- File: app/core/security/security.py ---
"""
Core security utilities.

This module provides:
- Password hashing and verification
- Data encryption and decryption
- Input sanitization
- Security validation functions
- Random string generation
"""

import re
import secrets
import string
import hashlib
import hmac
from typing import Optional, Union, Dict, Any
import bcrypt
from email_validator import validate_email as email_validate, EmailNotValidError
from app.core.config import settings
from app.core.security.encryption import encryption_manager
from app.core.exceptions.validation_exceptions import ValidationException


class SecurityManager:
    """
    Core security manager providing various security utilities.
    
    This class handles:
    - Password hashing and verification
    - Data encryption and decryption
    - Input sanitization
    - Security validations
    - Random string generation
    """
    
    def __init__(self):
        """Initialize security manager with settings."""
        self.bcrypt_rounds = settings.BCRYPT_ROUNDS
        self.secret_key = settings.SECRET_KEY
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
            
        Example:
            >>> security = SecurityManager()
            >>> hashed = security.hash_password("mypassword123")
        """
        if not password:
            raise ValidationException("Password cannot be empty")
        
        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=self.bcrypt_rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            hashed_password: Hashed password to verify against
            
        Returns:
            True if password matches, False otherwise
            
        Example:
            >>> security = SecurityManager()
            >>> is_valid = security.verify_password("mypassword123", hashed)
        """
        if not password or not hashed_password:
            return False
        
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False
    
    def generate_salt(self, length: int = 32) -> str:
        """
        Generate a random salt.
        
        Args:
            length: Length of the salt
            
        Returns:
            Random salt string
            
        Example:
            >>> security = SecurityManager()
            >>> salt = security.generate_salt(16)
        """
        return secrets.token_hex(length)
    
    def generate_random_string(
        self,
        length: int = 32,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_symbols: bool = False,
        exclude_ambiguous: bool = True
    ) -> str:
        """
        Generate a cryptographically secure random string.
        
        Args:
            length: Length of the string
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_symbols: Include symbols
            exclude_ambiguous: Exclude ambiguous characters (0, O, l, 1, etc.)
            
        Returns:
            Random string
            
        Example:
            >>> security = SecurityManager()
            >>> random_str = security.generate_random_string(16, include_symbols=True)
        """
        characters = ""
        
        if include_lowercase:
            chars = string.ascii_lowercase
            if exclude_ambiguous:
                chars = chars.replace('l', '').replace('o', '')
            characters += chars
        
        if include_uppercase:
            chars = string.ascii_uppercase
            if exclude_ambiguous:
                chars = chars.replace('I', '').replace('O', '')
            characters += chars
        
        if include_digits:
            chars = string.digits
            if exclude_ambiguous:
                chars = chars.replace('0', '').replace('1', '')
            characters += chars
        
        if include_symbols:
            chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            characters += chars
        
        if not characters:
            raise ValidationException("At least one character type must be included")
        
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    def encrypt_data(self, data: Union[str, Dict[str, Any]]) -> str:
        """
        Encrypt data using the encryption manager.
        
        Args:
            data: Data to encrypt (string or dictionary)
            
        Returns:
            Encrypted data string
            
        Example:
            >>> security = SecurityManager()
            >>> encrypted = security.encrypt_data("sensitive information")
        """
        if isinstance(data, dict):
            return encryption_manager.encrypt_dict(data)
        else:
            return encryption_manager.encrypt(str(data))
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Decrypt data using the encryption manager.
        
        Args:
            encrypted_data: Encrypted data string
            
        Returns:
            Decrypted data
            
        Example:
            >>> security = SecurityManager()
            >>> decrypted = security.decrypt_data(encrypted_data)
        """
        return encryption_manager.decrypt(encrypted_data)
    
    def sanitize_input(self, input_string: str, allow_html: bool = False) -> str:
        """
        Sanitize user input to prevent XSS and injection attacks.
        
        Args:
            input_string: Input string to sanitize
            allow_html: Whether to allow HTML tags
            
        Returns:
            Sanitized string
            
        Example:
            >>> security = SecurityManager()
            >>> clean = security.sanitize_input("<script>alert('xss')</script>")
        """
        if not input_string:
            return ""
        
        # Remove null bytes
        sanitized = input_string.replace('\x00', '')
        
        if not allow_html:
            # Escape HTML characters
            sanitized = (sanitized
                        .replace('&', '&amp;')
                        .replace('<', '&lt;')
                        .replace('>', '&gt;')
                        .replace('"', '&quot;')
                        .replace("'", '&#x27;')
                        .replace('/', '&#x2F;'))
        
        # Remove potentially dangerous patterns
        dangerous_patterns = [
            r'javascript:',
            r'vbscript:',
            r'onload=',
            r'onerror=',
            r'onclick=',
            r'onmouseover=',
            r'<script',
            r'</script>',
            r'<iframe',
            r'<object',
            r'<embed',
            r'<link',
            r'<meta',
        ]
        
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
            
        Example:
            >>> security = SecurityManager()
            >>> is_valid = security.validate_email("user@example.com")
        """
        if not email:
            return False
        
        try:
            # Use email-validator library for comprehensive validation
            valid = email_validate(email)
            return True
        except EmailNotValidError:
            return False
    
    def validate_phone(self, phone: str, country_code: str = "IN") -> bool:
        """
        Validate phone number format.
        
        Args:
            phone: Phone number to validate
            country_code: Country code for validation
            
        Returns:
            True if valid, False otherwise
            
        Example:
            >>> security = SecurityManager()
            >>> is_valid = security.validate_phone("+919876543210")
        """
        if not phone:
            return False
        
        # Remove all non-digit characters except +
        cleaned_phone = re.sub(r'[^\d+]', '', phone)
        
        if country_code.upper() == "IN":
            # Indian phone number validation
            patterns = [
                r'^\+91[6-9]\d{9}$',  # +91 followed by 10 digits starting with 6-9
                r'^[6-9]\d{9}$',      # 10 digits starting with 6-9
                r'^0[6-9]\d{9}$',     # 0 followed by 10 digits starting with 6-9
            ]
        else:
            # Generic international format
            patterns = [
                r'^\+\d{10,15}$',     # + followed by 10-15 digits
                r'^\d{10,15}$',       # 10-15 digits
            ]
        
        return any(re.match(pattern, cleaned_phone) for pattern in patterns)
    
    def create_signature(self, data: str, secret: Optional[str] = None) -> str:
        """
        Create HMAC signature for data.
        
        Args:
            data: Data to sign
            secret: Secret key (uses app secret if not provided)
            
        Returns:
            HMAC signature
            
        Example:
            >>> security = SecurityManager()
            >>> signature = security.create_signature("important data")
        """
        if secret is None:
            secret = self.secret_key
        
        return hmac.new(
            secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def verify_signature(
        self,
        data: str,
        signature: str,
        secret: Optional[str] = None
    ) -> bool:
        """
        Verify HMAC signature.
        
        Args:
            data: Original data
            signature: Signature to verify
            secret: Secret key (uses app secret if not provided)
            
        Returns:
            True if signature is valid
            
        Example:
            >>> security = SecurityManager()
            >>> is_valid = security.verify_signature(data, signature)
        """
        expected_signature = self.create_signature(data, secret)
        return hmac.compare_digest(signature, expected_signature)
    
    def hash_data(self, data: str, algorithm: str = "sha256") -> str:
        """
        Hash data using specified algorithm.
        
        Args:
            data: Data to hash
            algorithm: Hash algorithm (sha256, sha512, md5)
            
        Returns:
            Hexadecimal hash string
            
        Example:
            >>> security = SecurityManager()
            >>> hash_value = security.hash_data("data to hash")
        """
        if algorithm == "sha256":
            return hashlib.sha256(data.encode()).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(data.encode()).hexdigest()
        elif algorithm == "md5":
            return hashlib.md5(data.encode()).hexdigest()
        else:
            raise ValidationException(f"Unsupported hash algorithm: {algorithm}")
    
    def generate_api_key(self, prefix: str = "hms") -> str:
        """
        Generate API key with prefix.
        
        Args:
            prefix: Prefix for the API key
            
        Returns:
            Generated API key
            
        Example:
            >>> security = SecurityManager()
            >>> api_key = security.generate_api_key("hms")
            >>> # Returns: hms_1234567890abcdef...
        """
        random_part = self.generate_random_string(32, include_symbols=False)
        return f"{prefix}_{random_part}"
    
    def mask_sensitive_data(self, data: str, mask_char: str = "*") -> str:
        """
        Mask sensitive data for logging/display.
        
        Args:
            data: Data to mask
            mask_char: Character to use for masking
            
        Returns:
            Masked data string
            
        Example:
            >>> security = SecurityManager()
            >>> masked = security.mask_sensitive_data("1234567890")
            >>> # Returns: "******7890"
        """
        if not data or len(data) <= 4:
            return mask_char * len(data) if data else ""
        
        # Show last 4 characters, mask the rest
        visible_part = data[-4:]
        masked_part = mask_char * (len(data) - 4)
        
        return masked_part + visible_part
    
    def is_safe_url(self, url: str, allowed_hosts: Optional[list] = None) -> bool:
        """
        Check if URL is safe for redirects.
        
        Args:
            url: URL to check
            allowed_hosts: List of allowed hosts
            
        Returns:
            True if URL is safe
            
        Example:
            >>> security = SecurityManager()
            >>> is_safe = security.is_safe_url("https://example.com/path")
        """
        if not url:
            return False
        
        # Check for dangerous protocols
        dangerous_protocols = ['javascript:', 'data:', 'vbscript:', 'file:']
        url_lower = url.lower()
        
        if any(url_lower.startswith(proto) for proto in dangerous_protocols):
            return False
        
        # If allowed_hosts is specified, validate against them
        if allowed_hosts:
            from urllib.parse import urlparse
            try:
                parsed = urlparse(url)
                if parsed.hostname and parsed.hostname not in allowed_hosts:
                    return False
            except Exception:
                return False
        
        return True
    
    def constant_time_compare(self, a: str, b: str) -> bool:
        """
        Compare two strings in constant time to prevent timing attacks.
        
        Args:
            a: First string
            b: Second string
            
        Returns:
            True if strings are equal
            
        Example:
            >>> security = SecurityManager()
            >>> is_equal = security.constant_time_compare(token1, token2)
        """
        return hmac.compare_digest(a, b)


# Global security manager instance
security_manager = SecurityManager()