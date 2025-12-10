"""
JWT (JSON Web Token) management for authentication.

This module handles:
- Access token creation and verification
- Refresh token management
- Token payload encoding/decoding
- Token expiration handling
- Token revocation support
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Union
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError
from app.core.config import settings
from app.core.exceptions.auth_exceptions import (
    InvalidTokenException,
    TokenExpiredException,
    AuthenticationException
)


class JWTManager:
    """
    JWT token manager for handling authentication tokens.
    
    This class provides methods for:
    - Creating access and refresh tokens
    - Verifying and decoding tokens
    - Managing token lifecycle
    - Extracting token payload information
    """
    
    def __init__(self):
        """Initialize JWT manager with application settings."""
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
    
    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Dictionary containing user data to encode in token
            expires_delta: Custom expiration time delta (optional)
            
        Returns:
            Encoded JWT access token string
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> token_data = {"user_id": "123", "email": "user@example.com"}
            >>> token = jwt_manager.create_access_token(token_data)
        """
        to_encode = data.copy()
        
        # Calculate expiration time
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )
        
        # Add standard claims
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "nbf": datetime.utcnow(),  # Not before
            "type": "access",
            "jti": self._generate_jti()  # JWT ID for tracking
        })
        
        # Encode token
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        return encoded_jwt
    
    def create_refresh_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT refresh token.
        
        Args:
            data: Dictionary containing user data to encode in token
            expires_delta: Custom expiration time delta (optional)
            
        Returns:
            Encoded JWT refresh token string
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> token_data = {"user_id": "123"}
            >>> refresh_token = jwt_manager.create_refresh_token(token_data)
        """
        to_encode = data.copy()
        
        # Calculate expiration time
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=self.refresh_token_expire_days
            )
        
        # Add standard claims
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "nbf": datetime.utcnow(),
            "type": "refresh",
            "jti": self._generate_jti()
        })
        
        # Encode token
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        return encoded_jwt
    
    def decode_token(self, token: str, verify: bool = True) -> Dict[str, Any]:
        """
        Decode and verify a JWT token.
        
        Args:
            token: JWT token to decode
            verify: Whether to verify signature and expiration
            
        Returns:
            Decoded token payload dictionary
            
        Raises:
            TokenExpiredException: If token has expired
            InvalidTokenException: If token is invalid or malformed
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> payload = jwt_manager.decode_token(token)
            >>> user_id = payload.get("user_id")
        """
        try:
            if verify:
                payload = jwt.decode(
                    token,
                    self.secret_key,
                    algorithms=[self.algorithm]
                )
            else:
                payload = jwt.decode(
                    token,
                    options={"verify_signature": False}
                )
            
            return payload
            
        except ExpiredSignatureError:
            raise TokenExpiredException("Token has expired")
        except DecodeError as e:
            raise InvalidTokenException(f"Token decode error: {str(e)}")
        except InvalidTokenError as e:
            raise InvalidTokenException(f"Invalid token: {str(e)}")
    
    def verify_token(
        self,
        token: str,
        token_type: Optional[str] = None
    ) -> bool:
        """
        Verify if a token is valid.
        
        Args:
            token: JWT token to verify
            token_type: Expected token type ('access' or 'refresh')
            
        Returns:
            True if token is valid, False otherwise
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> is_valid = jwt_manager.verify_token(token, "access")
        """
        try:
            payload = self.decode_token(token, verify=True)
            
            # Verify token type if specified
            if token_type and payload.get("type") != token_type:
                return False
            
            # Verify expiration
            exp = payload.get("exp")
            if not exp:
                return False
            
            if datetime.fromtimestamp(exp) < datetime.utcnow():
                return False
            
            # Verify not before
            nbf = payload.get("nbf")
            if nbf and datetime.fromtimestamp(nbf) > datetime.utcnow():
                return False
            
            return True
            
        except (InvalidTokenException, TokenExpiredException):
            return False
    
    def extract_payload(self, token: str) -> Dict[str, Any]:
        """
        Extract payload from token without verification.
        
        Args:
            token: JWT token
            
        Returns:
            Token payload dictionary
            
        Note:
            This method does not verify the token signature or expiration.
            Use only when you need to inspect expired or unverified tokens.
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> payload = jwt_manager.extract_payload(expired_token)
        """
        try:
            return self.decode_token(token, verify=False)
        except Exception:
            return {}
    
    def get_token_expiry(self, token: str) -> Optional[datetime]:
        """
        Get token expiration time.
        
        Args:
            token: JWT token
            
        Returns:
            Expiration datetime or None if not found
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> expiry = jwt_manager.get_token_expiry(token)
            >>> print(f"Token expires at: {expiry}")
        """
        try:
            payload = self.extract_payload(token)
            exp = payload.get("exp")
            if exp:
                return datetime.fromtimestamp(exp)
            return None
        except Exception:
            return None
    
    def get_token_issued_at(self, token: str) -> Optional[datetime]:
        """
        Get token issue time.
        
        Args:
            token: JWT token
            
        Returns:
            Issue datetime or None if not found
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> issued_at = jwt_manager.get_token_issued_at(token)
        """
        try:
            payload = self.extract_payload(token)
            iat = payload.get("iat")
            if iat:
                return datetime.fromtimestamp(iat)
            return None
        except Exception:
            return None
    
    def is_token_expired(self, token: str) -> bool:
        """
        Check if token is expired.
        
        Args:
            token: JWT token
            
        Returns:
            True if expired, False otherwise
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> if jwt_manager.is_token_expired(token):
            >>>     print("Token has expired")
        """
        expiry = self.get_token_expiry(token)
        if not expiry:
            return True
        return expiry < datetime.utcnow()
    
    def get_remaining_time(self, token: str) -> Optional[timedelta]:
        """
        Get remaining time until token expires.
        
        Args:
            token: JWT token
            
        Returns:
            Remaining time as timedelta or None if expired/invalid
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> remaining = jwt_manager.get_remaining_time(token)
            >>> if remaining:
            >>>     print(f"Token valid for {remaining.seconds} more seconds")
        """
        expiry = self.get_token_expiry(token)
        if not expiry:
            return None
        
        remaining = expiry - datetime.utcnow()
        return remaining if remaining.total_seconds() > 0 else None
    
    def refresh_access_token(
        self,
        refresh_token: str
    ) -> Optional[str]:
        """
        Create new access token from valid refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New access token or None if refresh token is invalid
            
        Raises:
            InvalidTokenException: If refresh token is invalid
            TokenExpiredException: If refresh token has expired
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> new_access_token = jwt_manager.refresh_access_token(refresh_token)
        """
        try:
            # Verify refresh token
            if not self.verify_token(refresh_token, token_type="refresh"):
                raise InvalidTokenException("Invalid refresh token")
            
            # Decode refresh token
            payload = self.decode_token(refresh_token)
            
            # Extract user data (exclude token-specific claims)
            user_data = {
                k: v for k, v in payload.items()
                if k not in ["exp", "iat", "nbf", "type", "jti"]
            }
            
            # Create new access token
            return self.create_access_token(user_data)
            
        except (InvalidTokenException, TokenExpiredException):
            raise
        except Exception as e:
            raise InvalidTokenException(f"Failed to refresh token: {str(e)}")
    
    def create_token_pair(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Create both access and refresh tokens.
        
        Args:
            data: User data to encode in tokens
            
        Returns:
            Dictionary with 'access_token' and 'refresh_token'
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> tokens = jwt_manager.create_token_pair({"user_id": "123"})
            >>> access_token = tokens["access_token"]
            >>> refresh_token = tokens["refresh_token"]
        """
        access_token = self.create_access_token(data)
        refresh_token = self.create_refresh_token(data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def get_user_id(self, token: str) -> Optional[str]:
        """
        Extract user ID from token.
        
        Args:
            token: JWT token
            
        Returns:
            User ID or None if not found
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> user_id = jwt_manager.get_user_id(token)
        """
        try:
            payload = self.extract_payload(token)
            return payload.get("user_id") or payload.get("sub")
        except Exception:
            return None
    
    def get_user_email(self, token: str) -> Optional[str]:
        """
        Extract user email from token.
        
        Args:
            token: JWT token
            
        Returns:
            User email or None if not found
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> email = jwt_manager.get_user_email(token)
        """
        try:
            payload = self.extract_payload(token)
            return payload.get("email")
        except Exception:
            return None
    
    def get_user_type(self, token: str) -> Optional[str]:
        """
        Extract user type from token.
        
        Args:
            token: JWT token
            
        Returns:
            User type or None if not found
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> user_type = jwt_manager.get_user_type(token)
        """
        try:
            payload = self.extract_payload(token)
            return payload.get("user_type")
        except Exception:
            return None
    
    def _generate_jti(self) -> str:
        """
        Generate unique JWT ID for token tracking.
        
        Returns:
            Unique token identifier
        """
        import uuid
        return str(uuid.uuid4())
    
    def blacklist_token(self, token: str, redis_client=None) -> bool:
        """
        Add token to blacklist (requires Redis).
        
        Args:
            token: Token to blacklist
            redis_client: Redis client instance
            
        Returns:
            True if successfully blacklisted
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> jwt_manager.blacklist_token(token, redis_client)
        """
        if not redis_client:
            return False
        
        try:
            payload = self.extract_payload(token)
            jti = payload.get("jti")
            exp = payload.get("exp")
            
            if not jti or not exp:
                return False
            
            # Calculate TTL for blacklist entry
            expiry_time = datetime.fromtimestamp(exp)
            ttl = int((expiry_time - datetime.utcnow()).total_seconds())
            
            if ttl > 0:
                redis_client.setex(
                    f"blacklist:{jti}",
                    ttl,
                    "1"
                )
                return True
            
            return False
            
        except Exception:
            return False
    
    def is_token_blacklisted(self, token: str, redis_client=None) -> bool:
        """
        Check if token is blacklisted.
        
        Args:
            token: Token to check
            redis_client: Redis client instance
            
        Returns:
            True if token is blacklisted
            
        Example:
            >>> jwt_manager = JWTManager()
            >>> if jwt_manager.is_token_blacklisted(token, redis_client):
            >>>     print("Token has been revoked")
        """
        if not redis_client:
            return False
        
        try:
            payload = self.extract_payload(token)
            jti = payload.get("jti")
            
            if not jti:
                return False
            
            return redis_client.exists(f"blacklist:{jti}") > 0
            
        except Exception:
            return False


# Global JWT manager instance
jwt_manager = JWTManager()