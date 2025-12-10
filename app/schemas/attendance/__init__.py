"""
Attendance schemas package
"""
from app.schemas.attendance.attendance_base import (
    AttendanceBase,
    AttendanceCreate,
    AttendanceUpdate,
    BulkAttendanceCreate
)
from app.schemas.attendance.attendance_response import (
    AttendanceResponse,
    AttendanceDetail,
    AttendanceListItem
)
from app.schemas.attendance.attendance_record import (
    AttendanceRecordRequest,
    BulkAttendanceRequest,
    AttendanceCorrection
)
from app.schemas.attendance.attendance_report import (
    AttendanceReport,
    AttendanceSummary,
    TrendAnalysis,
    MonthlyReport
)
from app.schemas.attendance.attendance_policy import (
    AttendancePolicy,
    PolicyConfig,
    PolicyUpdate
)
from app.schemas.attendance.attendance_alert import (
    AttendanceAlert,
    AlertConfig,
    AlertTrigger
)
from app.schemas.attendance.attendance_filters import (
    AttendanceFilterParams,
    DateRangeRequest,
    AttendanceExportRequest
)

__all__ = [
    # Base
    "AttendanceBase",
    "AttendanceCreate",
    "AttendanceUpdate",
    "BulkAttendanceCreate",
    
    # Response
    "AttendanceResponse",
    "AttendanceDetail",
    "AttendanceListItem",
    
    # Record
    "AttendanceRecordRequest",
    "BulkAttendanceRequest",
    "AttendanceCorrection",
    
    # Report
    "AttendanceReport",
    "AttendanceSummary",
    "TrendAnalysis",
    "MonthlyReport",
    
    # Policy
    "AttendancePolicy",
    "PolicyConfig",
    "PolicyUpdate",
    
    # Alert
    "AttendanceAlert",
    "AlertConfig",
    "AlertTrigger",
    
    # Filters
    "AttendanceFilterParams",
    "DateRangeRequest",
    "AttendanceExportRequest",
]