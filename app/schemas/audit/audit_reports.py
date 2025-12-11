# --- File: app/schemas/audit/audit_reports.py ---
"""
Comprehensive audit reporting schemas with advanced analytics.

Provides detailed reporting capabilities for audit logs including
summaries, trends, user activity analysis, and entity change history.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Any, Dict, List, Optional
from enum import Enum

from pydantic import Field, field_validator, computed_field, model_validator
from uuid import UUID

from app.schemas.common.base import BaseSchema
from app.schemas.common.enums import AuditActionCategory, UserRole
from app.schemas.common.filters import DateRangeFilter, DateTimeRangeFilter

__all__ = [
    "ReportFormat",
    "AuditSummary",
    "UserActivitySummary",
    "EntityChangeSummary",
    "EntityChangeRecord",
    "EntityChangeHistory",
    "CategoryAnalytics",
    "ComplianceReport",
    "SecurityAuditReport",
    "AuditReport",
    "AuditTrendAnalysis",
]


class ReportFormat(str, Enum):
    """Available report output formats."""
    
    JSON = "json"
    CSV = "csv"
    XLSX = "xlsx"
    PDF = "pdf"
    HTML = "html"


class CategoryAnalytics(BaseSchema):
    """
    Analytics for a specific audit action category.
    
    Provides detailed metrics and trends for category-level analysis.
    """
    
    category: AuditActionCategory = Field(
        ...,
        description="Action category"
    )
    category_name: Optional[str] = Field(
        None,
        description="Human-readable category name"
    )
    
    # Volume metrics
    total_events: int = Field(
        ...,
        ge=0,
        description="Total events in this category"
    )
    unique_users: int = Field(
        ...,
        ge=0,
        description="Number of unique users in this category"
    )
    unique_entities: int = Field(
        0,
        ge=0,
        description="Number of unique entities affected"
    )
    
    # Status breakdown
    successful_events: int = Field(..., ge=0)
    failed_events: int = Field(..., ge=0)
    pending_events: int = Field(0, ge=0)
    
    # Timing
    avg_events_per_day: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Average events per day"
    )
    peak_hour: Optional[int] = Field(
        None,
        ge=0,
        le=23,
        description="Hour of day with most activity (0-23)"
    )
    
    # Top action types in this category
    top_action_types: List[Dict[str, Any]] = Field(
        default_factory=list,
        max_length=10,
        description="Top 10 action types by frequency"
    )
    
    # Trend
    trend_direction: Optional[str] = Field(
        None,
        pattern="^(increasing|decreasing|stable)$",
        description="Trend direction over the period"
    )
    trend_percentage: Optional[Decimal] = Field(
        None,
        decimal_places=2,
        description="Percentage change vs previous period"
    )
    
    @computed_field
    @property
    def success_rate(self) -> Decimal:
        """Calculate success rate percentage."""
        if self.total_events == 0:
            return Decimal("100.00")
        return round(
            (Decimal(self.successful_events) / Decimal(self.total_events)) * 100,
            2
        )
    
    @computed_field
    @property
    def failure_rate(self) -> Decimal:
        """Calculate failure rate percentage."""
        if self.total_events == 0:
            return Decimal("0.00")
        return round(
            (Decimal(self.failed_events) / Decimal(self.total_events)) * 100,
            2
        )


class AuditSummary(BaseSchema):
    """
    High-level summary for audit log report.
    
    Provides aggregated statistics and distributions across
    multiple dimensions for executive overview.
    """
    
    period: DateRangeFilter = Field(
        ...,
        description="Reporting period"
    )
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Report generation timestamp"
    )
    
    # Scope
    hostel_id: Optional[UUID] = Field(
        None,
        description="Hostel scope (None = platform-wide)"
    )
    hostel_name: Optional[str] = Field(
        None,
        description="Hostel name"
    )
    
    # Overall metrics
    total_events: int = Field(
        ...,
        ge=0,
        description="Total audit events in period"
    )
    unique_users: int = Field(
        ...,
        ge=0,
        description="Number of unique users"
    )
    unique_ip_addresses: int = Field(
        0,
        ge=0,
        description="Number of unique IP addresses"
    )
    unique_sessions: int = Field(
        0,
        ge=0,
        description="Number of unique sessions"
    )
    
    # Status distribution
    successful_actions: int = Field(..., ge=0)
    failed_actions: int = Field(..., ge=0)
    pending_actions: int = Field(0, ge=0)
    partial_actions: int = Field(0, ge=0)
    
    # Distribution by category
    events_by_category: Dict[str, int] = Field(
        default_factory=dict,
        description="Event count by AuditActionCategory"
    )
    category_analytics: List[CategoryAnalytics] = Field(
        default_factory=list,
        description="Detailed analytics per category"
    )
    
    # Distribution by user role
    events_by_user_role: Dict[str, int] = Field(
        default_factory=dict,
        description="Event count by UserRole"
    )
    
    # Distribution by entity type
    events_by_entity_type: Dict[str, int] = Field(
        default_factory=dict,
        description="Event count by entity type"
    )
    
    # Top actors
    top_users_by_events: List["UserActivitySummary"] = Field(
        default_factory=list,
        max_length=10,
        description="Top 10 most active users"
    )
    
    # Security metrics
    critical_events: int = Field(0, ge=0, description="Critical severity events")
    high_severity_events: int = Field(0, ge=0, description="High severity events")
    sensitive_data_events: int = Field(
        0,
        ge=0,
        description="Events involving sensitive data"
    )
    events_requiring_review: int = Field(
        0,
        ge=0,
        description="Events flagged for review"
    )
    
    # Authentication metrics
    login_attempts: int = Field(0, ge=0)
    successful_logins: int = Field(0, ge=0)
    failed_logins: int = Field(0, ge=0)
    
    # Authorization metrics
    access_granted: int = Field(0, ge=0)
    access_denied: int = Field(0, ge=0)
    
    # Geographic distribution
    events_by_country: Dict[str, int] = Field(
        default_factory=dict,
        description="Event count by country code"
    )
    
    # Device distribution
    events_by_device_type: Dict[str, int] = Field(
        default_factory=dict,
        description="Event count by device type"
    )
    
    @computed_field
    @property
    def overall_success_rate(self) -> Decimal:
        """Calculate overall success rate."""
        if self.total_events == 0:
            return Decimal("100.00")
        return round(
            (Decimal(self.successful_actions) / Decimal(self.total_events)) * 100,
            2
        )
    
    @computed_field
    @property
    def login_success_rate(self) -> Decimal:
        """Calculate login success rate."""
        if self.login_attempts == 0:
            return Decimal("100.00")
        return round(
            (Decimal(self.successful_logins) / Decimal(self.login_attempts)) * 100,
            2
        )
    
    @computed_field
    @property
    def authorization_success_rate(self) -> Decimal:
        """Calculate authorization success rate."""
        total_auth = self.access_granted + self.access_denied
        if total_auth == 0:
            return Decimal("100.00")
        return round(
            (Decimal(self.access_granted) / Decimal(total_auth)) * 100,
            2
        )
    
    @computed_field
    @property
    def security_health_score(self) -> Decimal:
        """
        Calculate security health score (0-100).
        
        Higher score indicates better security posture.
        """
        if self.total_events == 0:
            return Decimal("100.00")
        
        # Factors that reduce score
        failure_penalty = (self.failed_actions / self.total_events) * 30
        critical_penalty = (self.critical_events / self.total_events) * 50
        access_denied_penalty = (self.access_denied / max(1, self.total_events)) * 20
        
        total_penalty = min(100, failure_penalty + critical_penalty + access_denied_penalty)
        score = 100 - total_penalty
        
        return round(Decimal(str(max(0, score))), 2)
    
    @computed_field
    @property
    def most_active_category(self) -> Optional[str]:
        """Identify the most active audit category."""
        if not self.events_by_category:
            return None
        return max(self.events_by_category, key=self.events_by_category.get)
    
    @computed_field
    @property
    def requires_attention(self) -> bool:
        """Determine if summary indicates issues requiring attention."""
        return (
            self.security_health_score < 70 or
            self.critical_events > 0 or
            self.events_requiring_review > 10 or
            self.failed_logins > 20
        )


class UserActivitySummary(BaseSchema):
    """
    Aggregate audit activity for one user.
    
    Provides comprehensive view of user's audit trail
    for activity monitoring and investigation.
    """
    
    user_id: UUID = Field(..., description="User identifier")
    user_name: Optional[str] = Field(None, description="User display name")
    user_email: Optional[str] = Field(None, description="User email")
    user_role: Optional[UserRole] = Field(None, description="User role")
    
    # Activity period
    period_start: datetime = Field(..., description="Period start")
    period_end: datetime = Field(..., description="Period end")
    first_activity: Optional[datetime] = Field(
        None,
        description="First activity timestamp in period"
    )
    last_activity: Optional[datetime] = Field(
        None,
        description="Last activity timestamp in period"
    )
    
    # Volume metrics
    total_events: int = Field(..., ge=0, description="Total events by this user")
    total_sessions: int = Field(0, ge=0, description="Number of sessions")
    unique_ip_addresses: int = Field(
        0,
        ge=0,
        description="Number of unique IPs used"
    )
    
    # Activity distribution
    events_by_category: Dict[str, int] = Field(
        default_factory=dict,
        description="Event count by category"
    )
    events_by_action_type: Dict[str, int] = Field(
        default_factory=dict,
        description="Event count by action type"
    )
    events_by_status: Dict[str, int] = Field(
        default_factory=dict,
        description="Event count by status"
    )
    
    # Entity interactions
    entities_affected: int = Field(
        0,
        ge=0,
        description="Number of unique entities affected"
    )
    entities_by_type: Dict[str, int] = Field(
        default_factory=dict,
        description="Entity count by type"
    )
    
    # Security metrics
    successful_actions: int = Field(0, ge=0)
    failed_actions: int = Field(0, ge=0)
    sensitive_data_accessed: int = Field(
        0,
        ge=0,
        description="Events involving sensitive data"
    )
    
    # Anomalies
    unusual_activity_count: int = Field(
        0,
        ge=0,
        description="Flagged unusual activities"
    )
    access_denied_count: int = Field(
        0,
        ge=0,
        description="Authorization failures"
    )
    
    # Activity patterns
    most_active_hour: Optional[int] = Field(
        None,
        ge=0,
        le=23,
        description="Hour of day with most activity"
    )
    most_active_day: Optional[str] = Field(
        None,
        description="Day of week with most activity"
    )
    avg_daily_events: Decimal = Field(
        0,
        ge=0,
        decimal_places=2,
        description="Average events per day"
    )
    
    # Geographic
    countries_accessed_from: List[str] = Field(
        default_factory=list,
        description="Country codes user accessed from"
    )
    
    # Devices
    device_types_used: List[str] = Field(
        default_factory=list,
        description="Device types used"
    )
    
    @computed_field
    @property
    def success_rate(self) -> Decimal:
        """Calculate user's success rate."""
        total = self.successful_actions + self.failed_actions
        if total == 0:
            return Decimal("100.00")
        return round(
            (Decimal(self.successful_actions) / Decimal(total)) * 100,
            2
        )
    
    @computed_field
    @property
    def activity_score(self) -> Decimal:
        """
        Calculate activity score (0-100).
        
        Based on volume and diversity of activities.
        """
        # Volume component (0-50)
        volume_score = min(50, (self.total_events / 100) * 50)
        
        # Diversity component (0-50)
        category_diversity = min(10, len(self.events_by_category)) * 5
        
        score = volume_score + category_diversity
        return round(Decimal(str(min(100, score))), 2)
    
    @computed_field
    @property
    def risk_level(self) -> str:
        """
        Assess user risk level based on activity patterns.
        
        Returns:
            'low', 'medium', 'high', or 'critical'
        """
        risk_score = 0
        
        # Failed actions
        if self.failed_actions > 10:
            risk_score += 2
        
        # Access denied
        if self.access_denied_count > 5:
            risk_score += 3
        
        # Unusual activity
        if self.unusual_activity_count > 0:
            risk_score += 4
        
        # Multiple IPs
        if self.unique_ip_addresses > 5:
            risk_score += 1
        
        # Multiple countries
        if len(self.countries_accessed_from) > 3:
            risk_score += 2
        
        if risk_score >= 8:
            return "critical"
        elif risk_score >= 5:
            return "high"
        elif risk_score >= 3:
            return "medium"
        else:
            return "low"


class EntityChangeSummary(BaseSchema):
    """
    Summary of changes for one entity type.
    
    Provides overview of how frequently entities of a
    specific type are being modified.
    """
    
    entity_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Entity type name"
    )
    entity_type_display: Optional[str] = Field(
        None,
        description="Human-readable entity type name"
    )
    
    # Volume
    total_changes: int = Field(
        ...,
        ge=0,
        description="Total change events"
    )
    unique_entities_changed: int = Field(
        ...,
        ge=0,
        description="Number of unique entities modified"
    )
    
    # Change types
    creates: int = Field(0, ge=0, description="Create operations")
    updates: int = Field(0, ge=0, description="Update operations")
    deletes: int = Field(0, ge=0, description="Delete operations")
    restores: int = Field(0, ge=0, description="Restore operations")
    
    # Timing
    last_change_at: Optional[datetime] = Field(
        None,
        description="Timestamp of most recent change"
    )
    first_change_at: Optional[datetime] = Field(
        None,
        description="Timestamp of first change in period"
    )
    avg_changes_per_day: Decimal = Field(
        0,
        ge=0,
        decimal_places=2,
        description="Average changes per day"
    )
    
    # Most changed entities
    most_changed_entities: List[Dict[str, Any]] = Field(
        default_factory=list,
        max_length=10,
        description="Entities with most changes"
    )
    
    # Most active users
    top_users: List[UUID] = Field(
        default_factory=list,
        max_length=5,
        description="Top 5 users modifying this entity type"
    )
    
    @computed_field
    @property
    def change_rate(self) -> Decimal:
        """Calculate average changes per entity."""
        if self.unique_entities_changed == 0:
            return Decimal("0.00")
        return round(
            Decimal(self.total_changes) / Decimal(self.unique_entities_changed),
            2
        )
    
    @computed_field
    @property
    def volatility_score(self) -> Decimal:
        """
        Calculate volatility score (0-100).
        
        Higher score indicates more frequent changes.
        """
        if self.unique_entities_changed == 0:
            return Decimal("0.00")
        
        # Changes per entity
        changes_per_entity = self.total_changes / self.unique_entities_changed
        
        # Normalize to 0-100
        score = min(100, changes_per_entity * 10)
        return round(Decimal(str(score)), 2)


class EntityChangeRecord(BaseSchema):
    """
    Single change record for entity change history.
    
    Represents one modification event in an entity's lifecycle.
    """
    
    log_id: UUID = Field(..., description="Audit log entry ID")
    
    # Action details
    action_type: str = Field(..., description="Action type")
    action_category: AuditActionCategory = Field(..., description="Action category")
    description: str = Field(..., description="Change description")
    
    # Change data
    old_values: Optional[Dict[str, Any]] = Field(
        None,
        description="Previous values"
    )
    new_values: Optional[Dict[str, Any]] = Field(
        None,
        description="New values"
    )
    changed_fields: List[str] = Field(
        default_factory=list,
        description="List of fields that changed"
    )
    
    # Actor
    changed_by: Optional[UUID] = Field(None, description="User who made the change")
    changed_by_name: Optional[str] = Field(None, description="User display name")
    changed_by_role: Optional[UserRole] = Field(None, description="User role")
    
    # Context
    changed_at: datetime = Field(..., description="Change timestamp")
    ip_address: Optional[str] = Field(None, description="IP address")
    request_id: Optional[str] = Field(None, description="Request ID")
    
    # Status
    status: str = Field(..., description="Change status")
    
    @computed_field
    @property
    def change_summary(self) -> str:
        """Generate human-readable change summary."""
        if not self.changed_fields:
            return self.description
        
        field_list = ", ".join(self.changed_fields[:3])
        if len(self.changed_fields) > 3:
            field_list += f" and {len(self.changed_fields) - 3} more"
        
        return f"Changed: {field_list}"
    
    @computed_field
    @property
    def actor_display(self) -> str:
        """Get display string for actor."""
        if self.changed_by_name:
            return self.changed_by_name
        elif self.changed_by:
            return str(self.changed_by)
        else:
            return "System"


class EntityChangeHistory(BaseSchema):
    """
    Complete change history for a specific entity instance.
    
    Provides full audit trail for a single entity showing
    all modifications throughout its lifecycle.
    """
    
    entity_type: str = Field(..., description="Entity type")
    entity_id: UUID = Field(..., description="Entity ID")
    entity_name: Optional[str] = Field(None, description="Entity display name")
    
    # Lifecycle
    created_at: Optional[datetime] = Field(None, description="Entity creation time")
    created_by: Optional[UUID] = Field(None, description="Creator user ID")
    last_modified_at: Optional[datetime] = Field(
        None,
        description="Last modification time"
    )
    last_modified_by: Optional[UUID] = Field(None, description="Last modifier user ID")
    
    # Change records
    total_changes: int = Field(..., ge=0, description="Total number of changes")
    changes: List[EntityChangeRecord] = Field(
        default_factory=list,
        description="Chronological list of changes"
    )
    
    # Statistics
    unique_modifiers: int = Field(
        0,
        ge=0,
        description="Number of unique users who modified this entity"
    )
    fields_modified: List[str] = Field(
        default_factory=list,
        description="List of all fields ever modified"
    )
    
    # Current state
    is_deleted: bool = Field(False, description="Whether entity is deleted")
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp")
    deleted_by: Optional[UUID] = Field(None, description="User who deleted")
    
    @computed_field
    @property
    def entity_age_days(self) -> Optional[int]:
        """Calculate entity age in days."""
        if not self.created_at:
            return None
        return (datetime.utcnow() - self.created_at).days
    
    @computed_field
    @property
    def change_frequency(self) -> Optional[Decimal]:
        """Calculate average changes per day."""
        if not self.created_at or self.total_changes == 0:
            return None
        
        age_days = self.entity_age_days or 1
        return round(Decimal(self.total_changes) / Decimal(max(1, age_days)), 2)
    
    def get_field_history(self, field_name: str) -> List[Dict[str, Any]]:
        """
        Get change history for a specific field.
        
        Args:
            field_name: Name of the field
            
        Returns:
            List of changes for that field
        """
        field_changes = []
        
        for change in self.changes:
            if field_name in change.changed_fields:
                field_changes.append({
                    "timestamp": change.changed_at,
                    "old_value": change.old_values.get(field_name) if change.old_values else None,
                    "new_value": change.new_values.get(field_name) if change.new_values else None,
                    "changed_by": change.changed_by,
                })
        
        return field_changes


class ComplianceReport(BaseSchema):
    """
    Compliance-focused audit report.
    
    Provides audit trail information organized for
    regulatory compliance and certification.
    """
    
    period: DateRangeFilter = Field(..., description="Reporting period")
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Report generation time"
    )
    
    # Compliance framework
    framework: str = Field(
        ...,
        max_length=50,
        description="Compliance framework (GDPR, HIPAA, SOC2, etc.)"
    )
    
    # Scope
    hostel_id: Optional[UUID] = None
    scope_description: str = Field(
        ...,
        description="Description of report scope"
    )
    
    # Access control metrics
    authentication_events: int = Field(0, ge=0)
    authorization_events: int = Field(0, ge=0)
    access_violations: int = Field(0, ge=0)
    privileged_access_events: int = Field(0, ge=0)
    
    # Data access metrics
    sensitive_data_access: int = Field(0, ge=0)
    pii_access_events: int = Field(0, ge=0)
    data_export_events: int = Field(0, ge=0)
    data_deletion_events: int = Field(0, ge=0)
    
    # Change management
    configuration_changes: int = Field(0, ge=0)
    user_changes: int = Field(0, ge=0)
    permission_changes: int = Field(0, ge=0)
    
    # Anomalies and incidents
    failed_login_attempts: int = Field(0, ge=0)
    unusual_access_patterns: int = Field(0, ge=0)
    policy_violations: int = Field(0, ge=0)
    security_incidents: int = Field(0, ge=0)
    
    # User activity
    unique_users: int = Field(0, ge=0)
    admin_users_active: int = Field(0, ge=0)
    external_access_count: int = Field(0, ge=0)
    
    # Compliance status
    compliant_events: int = Field(0, ge=0)
    non_compliant_events: int = Field(0, ge=0)
    compliance_rate: Decimal = Field(
        ...,
        ge=0,
        le=100,
        decimal_places=2,
        description="Percentage of compliant events"
    )
    
    # Recommendations
    findings: List[str] = Field(
        default_factory=list,
        description="Compliance findings and issues"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Recommended actions"
    )
    
    @computed_field
    @property
    def compliance_grade(self) -> str:
        """Get compliance grade based on compliance rate."""
        rate = float(self.compliance_rate)
        
        if rate >= 99:
            return "A+"
        elif rate >= 95:
            return "A"
        elif rate >= 90:
            return "B"
        elif rate >= 80:
            return "C"
        elif rate >= 70:
            return "D"
        else:
            return "F"
    
    @computed_field
    @property
    def risk_assessment(self) -> str:
        """Assess overall compliance risk."""
        if self.compliance_rate >= 95 and self.security_incidents == 0:
            return "low"
        elif self.compliance_rate >= 85 and self.security_incidents <= 2:
            return "medium"
        elif self.compliance_rate >= 70:
            return "high"
        else:
            return "critical"


class SecurityAuditReport(BaseSchema):
    """
    Security-focused audit report.
    
    Provides detailed security metrics and threat analysis
    based on audit trail data.
    """
    
    period: DateRangeFilter = Field(..., description="Reporting period")
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Report generation time"
    )
    
    # Authentication security
    total_login_attempts: int = Field(0, ge=0)
    successful_logins: int = Field(0, ge=0)
    failed_logins: int = Field(0, ge=0)
    brute_force_attempts: int = Field(0, ge=0)
    compromised_accounts: int = Field(0, ge=0)
    
    # Authorization security
    total_access_attempts: int = Field(0, ge=0)
    unauthorized_access_attempts: int = Field(0, ge=0)
    privilege_escalation_attempts: int = Field(0, ge=0)
    
    # Data security
    sensitive_data_exposures: int = Field(0, ge=0)
    data_exfiltration_attempts: int = Field(0, ge=0)
    suspicious_data_access: int = Field(0, ge=0)
    
    # Threat indicators
    suspicious_ips: List[str] = Field(
        default_factory=list,
        description="IP addresses with suspicious activity"
    )
    suspicious_users: List[UUID] = Field(
        default_factory=list,
        description="Users with suspicious activity"
    )
    anomalous_patterns: int = Field(0, ge=0)
    
    # Security events
    critical_events: int = Field(0, ge=0)
    security_policy_violations: int = Field(0, ge=0)
    configuration_changes: int = Field(0, ge=0)
    
    # Risk metrics
    overall_risk_score: Decimal = Field(
        ...,
        ge=0,
        le=100,
        decimal_places=2,
        description="Overall security risk score (0=best, 100=worst)"
    )
    
    # Recommendations
    critical_findings: List[str] = Field(
        default_factory=list,
        description="Critical security findings"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Security recommendations"
    )
    
    @computed_field
    @property
    def threat_level(self) -> str:
        """Assess overall threat level."""
        score = float(self.overall_risk_score)
        
        if score >= 80:
            return "critical"
        elif score >= 60:
            return "high"
        elif score >= 40:
            return "medium"
        elif score >= 20:
            return "low"
        else:
            return "minimal"
    
    @computed_field
    @property
    def login_success_rate(self) -> Decimal:
        """Calculate login success rate."""
        if self.total_login_attempts == 0:
            return Decimal("100.00")
        return round(
            (Decimal(self.successful_logins) / Decimal(self.total_login_attempts)) * 100,
            2
        )


class AuditTrendAnalysis(BaseSchema):
    """
    Trend analysis for audit metrics over time.
    
    Provides time-series data and trend indicators for
    identifying patterns and anomalies.
    """
    
    period: DateRangeFilter = Field(..., description="Analysis period")
    granularity: str = Field(
        ...,
        pattern="^(hourly|daily|weekly|monthly)$",
        description="Time granularity"
    )
    
    # Data points
    data_points: List[Dict[str, Any]] = Field(
        ...,
        description="Time-series data points"
    )
    
    # Trend metrics
    trend_direction: str = Field(
        ...,
        pattern="^(increasing|decreasing|stable)$",
        description="Overall trend direction"
    )
    trend_strength: Decimal = Field(
        ...,
        ge=0,
        le=100,
        decimal_places=2,
        description="Trend strength (0-100)"
    )
    percentage_change: Decimal = Field(
        ...,
        decimal_places=2,
        description="Percentage change over period"
    )
    
    # Statistical metrics
    average_value: Decimal = Field(..., decimal_places=2)
    median_value: Decimal = Field(..., decimal_places=2)
    std_deviation: Decimal = Field(..., ge=0, decimal_places=2)
    
    # Anomalies
    anomaly_count: int = Field(0, ge=0, description="Number of detected anomalies")
    anomaly_dates: List[date] = Field(
        default_factory=list,
        description="Dates with anomalous activity"
    )
    
    # Peak/low points
    peak_value: Decimal = Field(..., description="Highest value in period")
    peak_date: Optional[date] = Field(None, description="Date of peak value")
    low_value: Decimal = Field(..., description="Lowest value in period")
    low_date: Optional[date] = Field(None, description="Date of lowest value")
    
    @computed_field
    @property
    def volatility_score(self) -> Decimal:
        """Calculate volatility score based on standard deviation."""
        if float(self.average_value) == 0:
            return Decimal("0.00")
        
        cv = (float(self.std_deviation) / float(self.average_value)) * 100
        return round(Decimal(str(min(100, cv))), 2)
    
    @computed_field
    @property
    def is_anomalous_period(self) -> bool:
        """Determine if the period shows anomalous patterns."""
        return self.anomaly_count > 0 or self.volatility_score > 50


class AuditReport(BaseSchema):
    """
    Complete comprehensive audit report.
    
    Consolidates all audit analytics into a single
    comprehensive report for executive review.
    """
    
    # Report metadata
    report_id: UUID = Field(default_factory=lambda: UUID(int=0), description="Report ID")
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Report generation timestamp"
    )
    generated_by: Optional[UUID] = Field(None, description="User who generated report")
    
    period: DateRangeFilter = Field(..., description="Reporting period")
    
    # Scope
    hostel_id: Optional[UUID] = None
    hostel_name: Optional[str] = None
    scope_description: str = Field(
        "Platform-wide audit report",
        description="Report scope description"
    )
    
    # Core sections
    summary: AuditSummary = Field(..., description="Executive summary")
    entity_summaries: List[EntityChangeSummary] = Field(
        default_factory=list,
        description="Entity change summaries"
    )
    user_activities: List[UserActivitySummary] = Field(
        default_factory=list,
        max_length=50,
        description="User activity summaries"
    )
    
    # Specialized reports
    compliance_report: Optional[ComplianceReport] = Field(
        None,
        description="Compliance report (if applicable)"
    )
    security_report: Optional[SecurityAuditReport] = Field(
        None,
        description="Security audit report"
    )
    
    # Trends
    trends: List[AuditTrendAnalysis] = Field(
        default_factory=list,
        description="Trend analyses"
    )
    
    # Insights
    key_findings: List[str] = Field(
        default_factory=list,
        description="Key findings from the audit"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Recommended actions"
    )
    action_items: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Actionable items with priorities"
    )
    
    # Attachments
    export_formats: List[ReportFormat] = Field(
        default_factory=list,
        description="Available export formats"
    )
    
    @computed_field
    @property
    def executive_summary_text(self) -> str:
        """Generate executive summary text."""
        parts = []
        
        parts.append(
            f"Audit report for period {self.period.start_date} to {self.period.end_date}"
        )
        parts.append(f"Total events: {self.summary.total_events:,}")
        parts.append(
            f"Success rate: {self.summary.overall_success_rate}%"
        )
        
        if self.summary.requires_attention:
            parts.append("⚠️  Requires attention: Security or compliance issues detected")
        
        return " | ".join(parts)
    
    @computed_field
    @property
    def overall_health_score(self) -> Decimal:
        """Calculate overall audit health score."""
        scores = [float(self.summary.security_health_score)]
        
        if self.compliance_report:
            scores.append(float(self.compliance_report.compliance_rate))
        
        if self.security_report:
            scores.append(100 - float(self.security_report.overall_risk_score))
        
        avg_score = sum(scores) / len(scores)
        return round(Decimal(str(avg_score)), 2)