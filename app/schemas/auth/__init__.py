"""
Authentication schemas package
"""
from app.schemas.auth.login import (
    LoginRequest,
    LoginResponse,
    TokenData
)
from app.schemas.auth.register import (
    RegisterRequest,
    RegisterResponse,
    VerifyEmailRequest,
    VerifyPhoneRequest
)
from app.schemas.auth.token import (
    Token,
    TokenPayload,
    RefreshTokenRequest,
    RefreshTokenResponse
)
from app.schemas.auth.password import (
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordChangeRequest,
    PasswordChangeResponse
)
from app.schemas.auth.otp import (
    OTPGenerateRequest,
    OTPVerifyRequest,
    OTPResponse
)
from app.schemas.auth.social_auth import (
    SocialAuthRequest,
    SocialAuthResponse,
    GoogleAuthRequest,
    FacebookAuthRequest
)

__all__ = [
    # Login
    "LoginRequest",
    "LoginResponse",
    "TokenData",
    
    # Register
    "RegisterRequest",
    "RegisterResponse",
    "VerifyEmailRequest",
    "VerifyPhoneRequest",
    
    # Token
    "Token",
    "TokenPayload",
    "RefreshTokenRequest",
    "RefreshTokenResponse",
    
    # Password
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "PasswordChangeRequest",
    "PasswordChangeResponse",
    
    # OTP
    "OTPGenerateRequest",
    "OTPVerifyRequest",
    "OTPResponse",
    
    # Social Auth
    "SocialAuthRequest",
    "SocialAuthResponse",
    "GoogleAuthRequest",
    "FacebookAuthRequest",
]