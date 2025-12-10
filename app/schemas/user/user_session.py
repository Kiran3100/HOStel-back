"""
User session schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import Field, IPvAnyAddress
from uuid import UUID

from app.schemas.common.base import BaseResponseSchema, BaseSchema


class UserSession(BaseResponseSchema):
    """User session information"""
    user_id: UUID = Field(..., description="User ID")
    device_info: Optional[dict] = Field(None, description="Device information")
    ip_address: Optional[str] = Field(None, description="IP address")
    is_revoked: bool = Field(False, description="Session revoked status")
    expires_at: datetime = Field(..., description="Session expiration")
    last_activity: datetime = Field(..., description="Last activity timestamp")


class SessionInfo(BaseSchema):
    """Session information for display"""
    session_id: UUID = Field(..., description="Session ID")
    device_name: Optional[str] = Field(None, description="Device name")
    device_type: Optional[str] = Field(None, description="Device type (mobile/desktop/tablet)")
    browser: Optional[str] = Field(None, description="Browser name")
    os: Optional[str] = Field(None, description="Operating system")
    ip_address: Optional[str] = Field(None, description="IP address")
    location: Optional[str] = Field(None, description="Approximate location")
    is_current: bool = Field(False, description="Is current session")
    created_at: datetime = Field(..., description="Session start time")
    last_activity: datetime = Field(..., description="Last activity")
    expires_at: datetime = Field(..., description="Expiration time")


class ActiveSessionsList(BaseSchema):
    """List of active sessions"""
    sessions: List[SessionInfo] = Field(..., description="Active sessions")
    total_sessions: int = Field(..., description="Total number of sessions")


class RevokeSessionRequest(BaseSchema):
    """Revoke specific session"""
    session_id: UUID = Field(..., description="Session ID to revoke")


class RevokeAllSessionsRequest(BaseSchema):
    """Revoke all sessions except current"""
    keep_current: bool = Field(True, description="Keep current session active")