"""
OAuth authentication management.

This module handles:
- Google OAuth authentication
- Facebook OAuth authentication
- OAuth token verification
- User info extraction from OAuth providers
"""

from typing import Dict, Any, Optional
import httpx
from app.core.config import settings
from app.core.exceptions.auth_exceptions import AuthenticationException


class OAuthManager:
    """
    OAuth authentication manager for third-party login providers.
    
    Supports:
    - Google OAuth 2.0
    - Facebook OAuth 2.0
    """
    
    def __init__(self):
        """Initialize OAuth manager with settings."""
        self.google_client_id = settings.GOOGLE_CLIENT_ID
        self.google_client_secret = settings.GOOGLE_CLIENT_SECRET
        self.facebook_app_id = settings.FACEBOOK_APP_ID
        self.facebook_app_secret = settings.FACEBOOK_APP_SECRET
    
    async def google_oauth(self, access_token: str) -> Dict[str, Any]:
        """
        Authenticate with Google OAuth and get user info.
        
        Args:
            access_token: Google access token
            
        Returns:
            Dictionary containing user information from Google
            
        Raises:
            AuthenticationException: If authentication fails
            
        Example:
            >>> oauth = OAuthManager()
            >>> user_info = await oauth.google_oauth(access_token)
            >>> email = user_info.get("email")
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    raise AuthenticationException(
                        f"Failed to authenticate with Google: {response.text}"
                    )
                
                user_info = response.json()
                
                # Validate required fields
                if not user_info.get("email"):
                    raise AuthenticationException("Email not provided by Google")
                
                return {
                    "provider": "google",
                    "provider_id": user_info.get("id"),
                    "email": user_info.get("email"),
                    "name": user_info.get("name"),
                    "first_name": user_info.get("given_name"),
                    "last_name": user_info.get("family_name"),
                    "picture": user_info.get("picture"),
                    "verified_email": user_info.get("verified_email", False),
                    "locale": user_info.get("locale"),
                }
                
        except httpx.HTTPError as e:
            raise AuthenticationException(f"Google OAuth error: {str(e)}")
        except Exception as e:
            raise AuthenticationException(f"Google OAuth failed: {str(e)}")
    
    async def facebook_oauth(self, access_token: str) -> Dict[str, Any]:
        """
        Authenticate with Facebook OAuth and get user info.
        
        Args:
            access_token: Facebook access token
            
        Returns:
            Dictionary containing user information from Facebook
            
        Raises:
            AuthenticationException: If authentication fails
            
        Example:
            >>> oauth = OAuthManager()
            >>> user_info = await oauth.facebook_oauth(access_token)
            >>> email = user_info.get("email")
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://graph.facebook.com/me",
                    params={
                        "access_token": access_token,
                        "fields": "id,name,email,picture,first_name,last_name"
                    },
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    raise AuthenticationException(
                        f"Failed to authenticate with Facebook: {response.text}"
                    )
                
                user_info = response.json()
                
                # Extract picture URL
                picture_url = None
                if user_info.get("picture"):
                    picture_data = user_info["picture"].get("data", {})
                    picture_url = picture_data.get("url")
                
                return {
                    "provider": "facebook",
                    "provider_id": user_info.get("id"),
                    "email": user_info.get("email"),
                    "name": user_info.get("name"),
                    "first_name": user_info.get("first_name"),
                    "last_name": user_info.get("last_name"),
                    "picture": picture_url,
                }
                
        except httpx.HTTPError as e:
            raise AuthenticationException(f"Facebook OAuth error: {str(e)}")
        except Exception as e:
            raise AuthenticationException(f"Facebook OAuth failed: {str(e)}")
    
    async def verify_google_token(self, id_token: str) -> Dict[str, Any]:
        """
        Verify Google ID token.
        
        Args:
            id_token: Google ID token
            
        Returns:
            Verified token payload
            
        Raises:
            AuthenticationException: If verification fails
            
        Example:
            >>> oauth = OAuthManager()
            >>> payload = await oauth.verify_google_token(id_token)
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://oauth2.googleapis.com/tokeninfo",
                    params={"id_token": id_token},
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    raise AuthenticationException("Invalid Google ID token")
                
                token_info = response.json()
                
                # Verify audience (client ID)
                if token_info.get("aud") != self.google_client_id:
                    raise AuthenticationException("Invalid token audience")
                
                return token_info
                
        except httpx.HTTPError as e:
            raise AuthenticationException(f"Google token verification error: {str(e)}")
    
    async def verify_facebook_token(self, access_token: str) -> Dict[str, Any]:
        """
        Verify Facebook access token.
        
        Args:
            access_token: Facebook access token
            
        Returns:
            Verified token info
            
        Raises:
            AuthenticationException: If verification fails
            
        Example:
            >>> oauth = OAuthManager()
            >>> token_info = await oauth.verify_facebook_token(access_token)
        """
        try:
            app_token = f"{self.facebook_app_id}|{self.facebook_app_secret}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://graph.facebook.com/debug_token",
                    params={
                        "input_token": access_token,
                        "access_token": app_token
                    },
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    raise AuthenticationException("Invalid Facebook access token")
                
                result = response.json()
                data = result.get("data", {})
                
                if not data.get("is_valid"):
                    raise AuthenticationException("Facebook token is not valid")
                
                if data.get("app_id") != self.facebook_app_id:
                    raise AuthenticationException("Invalid token app ID")
                
                return data
                
        except httpx.HTTPError as e:
            raise AuthenticationException(f"Facebook token verification error: {str(e)}")
    
    async def verify_oauth_token(
        self,
        provider: str,
        access_token: str
    ) -> bool:
        """
        Verify OAuth token for any provider.
        
        Args:
            provider: OAuth provider (google, facebook)
            access_token: Access token to verify
            
        Returns:
            True if token is valid, False otherwise
            
        Example:
            >>> oauth = OAuthManager()
            >>> is_valid = await oauth.verify_oauth_token("google", token)
        """
        try:
            if provider.lower() == "google":
                await self.google_oauth(access_token)
                return True
            elif provider.lower() == "facebook":
                await self.facebook_oauth(access_token)
                return True
            else:
                return False
        except AuthenticationException:
            return False
    
    async def get_user_info(
        self,
        provider: str,
        access_token: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get user information from OAuth provider.
        
        Args:
            provider: OAuth provider (google, facebook)
            access_token: Access token
            
        Returns:
            User information dictionary or None if failed
            
        Example:
            >>> oauth = OAuthManager()
            >>> user_info = await oauth.get_user_info("google", token)
            >>> if user_info:
            >>>     email = user_info.get("email")
        """
        try:
            if provider.lower() == "google":
                return await self.google_oauth(access_token)
            elif provider.lower() == "facebook":
                return await self.facebook_oauth(access_token)
            else:
                return None
        except AuthenticationException:
            return None
    
    async def exchange_code_for_token(
        self,
        provider: str,
        code: str,
        redirect_uri: str
    ) -> Optional[str]:
        """
        Exchange authorization code for access token.
        
        Args:
            provider: OAuth provider
            code: Authorization code
            redirect_uri: Redirect URI used in authorization
            
        Returns:
            Access token or None
            
        Example:
            >>> oauth = OAuthManager()
            >>> token = await oauth.exchange_code_for_token(
            ...     "google", auth_code, redirect_uri
            ... )
        """
        try:
            if provider.lower() == "google":
                return await self._exchange_google_code(code, redirect_uri)
            elif provider.lower() == "facebook":
                return await self._exchange_facebook_code(code, redirect_uri)
            else:
                return None
        except Exception:
            return None
    
    async def _exchange_google_code(
        self,
        code: str,
        redirect_uri: str
    ) -> Optional[str]:
        """Exchange Google authorization code for access token."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://oauth2.googleapis.com/token",
                    data={
                        "code": code,
                        "client_id": self.google_client_id,
                        "client_secret": self.google_client_secret,
                        "redirect_uri": redirect_uri,
                        "grant_type": "authorization_code"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("access_token")
                
                return None
                
        except Exception:
            return None
    
    async def _exchange_facebook_code(
        self,
        code: str,
        redirect_uri: str
    ) -> Optional[str]:
        """Exchange Facebook authorization code for access token."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://graph.facebook.com/v12.0/oauth/access_token",
                    params={
                        "code": code,
                        "client_id": self.facebook_app_id,
                        "client_secret": self.facebook_app_secret,
                        "redirect_uri": redirect_uri
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("access_token")
                
                return None
                
        except Exception:
            return None


# Global OAuth manager instance
oauth_manager = OAuthManager()