"""
Maintenance schemas package
"""
from app.schemas.maintenance.maintenance_base import (
    MaintenanceBase,
    MaintenanceCreate,
    MaintenanceUpdate
)
from app.schemas.maintenance.maintenance_response import (
    MaintenanceResponse,
    MaintenanceDetail,
    RequestListItem
)
from app.schemas.maintenance.maintenance_request import (
    MaintenanceRequest,
    RequestSubmission,
    EmergencyRequest
)
from app.schemas.maintenance.maintenance_assignment import (
    TaskAssignment,
    VendorAssignment,
    AssignmentUpdate
)
from app.schemas.maintenance.maintenance_approval import (
    ApprovalRequest,
    ApprovalResponse,
    ThresholdConfig
)
from app.schemas.maintenance.maintenance_completion import (
    CompletionRequest,
    QualityCheck,
    CompletionResponse
)
from app.schemas.maintenance.maintenance_schedule import (
    PreventiveSchedule,
    ScheduleCreate,
    RecurrenceConfig,
    ScheduleExecution
)
from app.schemas.maintenance.maintenance_cost import (
    CostTracking,
    BudgetAllocation,
    ExpenseReport
)
from app.schemas.maintenance.maintenance_filters import (
    MaintenanceFilterParams,
    SearchRequest,
    MaintenanceExportRequest
)
from app.schemas.maintenance.maintenance_analytics import (
    MaintenanceAnalytics,
    CostAnalysis,
    PerformanceMetrics
)

__all__ = [
    # Base
    "MaintenanceBase",
    "MaintenanceCreate",
    "MaintenanceUpdate",
    
    # Response
    "MaintenanceResponse",
    "MaintenanceDetail",
    "RequestListItem",
    
    # Request
    "MaintenanceRequest",
    "RequestSubmission",
    "EmergencyRequest",
    
    # Assignment
    "TaskAssignment",
    "VendorAssignment",
    "AssignmentUpdate",
    
    # Approval
    "ApprovalRequest",
    "ApprovalResponse",
    "ThresholdConfig",
    
    # Completion
    "CompletionRequest",
    "QualityCheck",
    "CompletionResponse",
    
    # Schedule
    "PreventiveSchedule",
    "ScheduleCreate",
    "RecurrenceConfig",
    "ScheduleExecution",
    
    # Cost
    "CostTracking",
    "BudgetAllocation",
    "ExpenseReport",
    
    # Filters
    "MaintenanceFilterParams",
    "SearchRequest",
    "MaintenanceExportRequest",
    
    # Analytics
    "MaintenanceAnalytics",
    "CostAnalysis",
    "PerformanceMetrics",
]