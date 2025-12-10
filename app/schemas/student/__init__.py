"""
Student schemas package
"""
from app.schemas.student.student_base import (
    StudentBase,
    StudentCreate,
    StudentUpdate
)
from app.schemas.student.student_response import (
    StudentResponse,
    StudentDetail,
    StudentProfile,
    StudentListItem
)
from app.schemas.student.student_profile import (
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentDocuments
)
from app.schemas.student.student_room_history import (
    RoomHistoryResponse,
    RoomTransferRequest,
    RoomTransferApproval
)
from app.schemas.student.student_dashboard import (
    StudentDashboard,
    StudentStats,
    StudentFinancialSummary
)
from app.schemas.student.student_filters import (
    StudentFilterParams,
    StudentSearchRequest,
    StudentSortOptions
)

__all__ = [
    # Base
    "StudentBase",
    "StudentCreate",
    "StudentUpdate",
    
    # Response
    "StudentResponse",
    "StudentDetail",
    "StudentProfile",
    "StudentListItem",
    
    # Profile
    "StudentProfileCreate",
    "StudentProfileUpdate",
    "StudentDocuments",
    
    # Room history
    "RoomHistoryResponse",
    "RoomTransferRequest",
    "RoomTransferApproval",
    
    # Dashboard
    "StudentDashboard",
    "StudentStats",
    "StudentFinancialSummary",
    
    # Filters
    "StudentFilterParams",
    "StudentSearchRequest",
    "StudentSortOptions",
]