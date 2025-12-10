Below is a structured, file-by-file summary. Paths are shown relative to app/schemas.

app/schemas/__init__.py
Empty package initializer; exists to mark app.schemas as a Python package.
Admin Schemas (app/schemas/admin)
admin/admin_hostel_assignment.py
Schemas for linking admins to hostels and managing their assignment:
AdminHostelAssignment: response model for a single admin–hostel assignment (permissions, primary hostel, revoke info).
AssignmentCreate, AssignmentUpdate: create/update payloads for one assignment.
BulkAssignment: assign an admin to multiple hostels at once.
RevokeAssignment: payload to revoke an assignment with reason.
AssignmentList: aggregate assignments for a given admin.
HostelAdminList, HostelAdminItem: list admins associated with a given hostel.
admin/admin_override.py
Schemas for admins overriding supervisor decisions:
AdminOverrideRequest: payload describing the override (who, what entity, original vs override action, reason).
OverrideLog: response/log entry for one override.
OverrideReason: predefined override reasons.
OverrideSummary, SupervisorOverrideStats: summarized override metrics by period, type, supervisor, hostel.
admin/admin_permissions.py
Fine-grained permission model for admins:
AdminPermissions: boolean flags for many admin capabilities (rooms, students, fees, supervisors, financials, etc.).
PermissionMatrix, RolePermissions: role-based permission mapping for the system.
PermissionCheck: result of checking whether a user has a specific permission in a hostel.
admin/hostel_context.py
Multi-hostel “active context” management for admins:
HostelContext: current active hostel and quick stats for that session.
HostelSwitchRequest: request to switch active hostel.
ActiveHostelResponse: response after switching context.
ContextHistory, ContextSwitch: history of hostel context switches.
admin/hostel_selector.py
Data models backing a hostel selector UI:
HostelSelectorResponse, HostelSelectorItem: list and per-hostel cards for selection (occupancy, tasks, favorites, permissions).
RecentHostels, RecentHostelItem: recently accessed hostels.
FavoriteHostels, FavoriteHostelItem: favorite hostels list.
UpdateFavoriteRequest: add/remove favorite.
admin/multi_hostel_dashboard.py
Unified multi-hostel dashboard models:
MultiHostelDashboard: top-level dashboard for an admin managing several hostels.
AggregatedStats: cross-hostel metrics (occupancy, revenue, complaints, maintenance).
HostelQuickStats: per-hostel key stats and health status.
CrossHostelComparison, TopPerformer, BottomPerformer, HostelMetricComparison: cross-hostel comparisons and rankings.
HostelTaskSummary: per-hostel task counts by priority.
admin/__init__.py
Re-exports core admin-related schemas for convenient import:
Assignments, context switching, selector, dashboard, overrides, permissions.
Analytics Schemas (app/schemas/analytics)
analytics/booking_analytics.py
Analytics around bookings:
BookingKPI: aggregate counts & rates (conversion, cancellation, lead time).
BookingTrendPoint: time-series point with booking & revenue per day.
BookingFunnel: funnel metrics from page views to confirmations.
CancellationAnalytics: cancellation-specific stats and reasons.
BookingAnalyticsSummary: top-level booking analytics for a hostel/period.
analytics/complaint_analytics.py (dashboard-level)
Summary models for complaint analytics:
ComplaintKPI: high-level metrics (open/resolved, SLA compliance, escalation).
ComplaintTrend, ComplaintTrendPoint: trend over time.
CategoryBreakdown: per-category stats.
ComplaintDashboard: consolidated complaint dashboard payload.
analytics/custom_reports.py
Custom report builder schemas:
CustomReportField, CustomReportFilter: define fields/filters.
CustomReportRequest: specify module, fields, filters, grouping, sorting, output format.
CustomReportDefinition: saved report configuration.
CustomReportResult: generic tabular report output with summary/charts.
analytics/dashboard_analytics.py
General KPI and dashboard metrics:
KPIResponse: flexible KPI card representation.
QuickStats: high-level quick stats.
DashboardMetrics: combined KPIs, timeseries (revenue, occupancy, bookings, complaints).
TimeseriesPoint: generic timeseries value.
RoleSpecificDashboard: sections per role with cards and KPIs.
analytics/financial_analytics.py
Financial analytics for hostels/platform:
RevenueBreakdown, ExpenseBreakdown.
ProfitAndLossReport: P&L for given scope and period.
CashflowSummary, CashflowPoint.
FinancialReport: aggregate financial report with ratios and per-student/bed metrics.
analytics/occupancy_analytics.py
Occupancy-focused analytics:
OccupancyKPI, OccupancyTrendPoint: summary and daily occupancy.
ForecastData, ForecastPoint: future occupancy forecasts.
OccupancyByRoomType, OccupancyReport: full occupancy report including breakdowns and optional forecast.
analytics/platform_analytics.py
Platform-wide (multi-tenant) analytics:
PlatformMetrics: counts of hostels, users, DAU, sessions, etc.
GrowthMetrics, MonthlyMetric: hostels, revenue, users growth over time.
PlatformUsageAnalytics: API traffic, error rates, latency, resource usage.
analytics/supervisor_analytics.py
Supervisor performance analytics:
SupervisorKPI: workload & performance per supervisor.
SupervisorTrendPoint: performance over time.
SupervisorDashboardAnalytics: dashboard payload for one supervisor.
SupervisorComparison: compare multiple supervisors.
analytics/visitor_analytics.py
Visitor behavior and funnel:
VisitorFunnel: visits → registrations → bookings with conversion rates.
TrafficSourceAnalytics: per-source visits and conversion.
VisitorBehaviorAnalytics: search & engagement patterns.
analytics/__init__.py
Re-exports core analytics models by category (dashboard, financial, occupancy, complaints, visitor, booking, supervisor, platform, custom reports).
Announcement Schemas (app/schemas/announcement)
announcement/announcement_base.py
Core models for announcements:
AnnouncementBase: shared attributes (title, content, category, priority, targeting, attachments, expiry).
AnnouncementCreate: adds creator and delivery channel flags.
AnnouncementUpdate: partial update including publish state.
announcement/announcement_response.py
Read models for announcements:
AnnouncementResponse: basic list item with counts.
AnnouncementDetail: detailed view including targeting, approvals, delivery times, engagement.
AnnouncementList, AnnouncementListItem: list + summary metrics.
announcement/announcement_filters.py
Filtering, searching, exporting announcements:
AnnouncementFilterParams, SearchRequest: query & search parameters.
ArchiveRequest: bulk archival criteria.
AnnouncementExportRequest: export options (format, included info).
announcement/announcement_targeting.py
Audience targeting configurations:
TargetingConfig, AudienceSelection: describe who should receive an announcement.
TargetRooms, TargetFloors, IndividualTargeting: specialized targeting.
TargetingSummary: counts and breakdown for recipients.
BulkTargeting: multiple targeting rules and combine mode.
announcement/announcement_scheduling.py
Scheduling and recurrence:
ScheduleRequest, ScheduleConfig: schedule single announcement with optional expiry.
RecurringAnnouncement: recurring series (daily/weekly/monthly).
ScheduleUpdate, ScheduleCancel, PublishNow.
ScheduledAnnouncementsList, ScheduledAnnouncementItem: list future schedules.
announcement/announcement_approval.py
Approval workflow for announcements:
ApprovalRequest, ApprovalResponse, RejectionRequest.
ApprovalWorkflow: current approval status and timeline.
SupervisorApprovalQueue, PendingApprovalItem: queue of pending approvals.
BulkApproval: approve/reject multiple at once.
announcement/announcement_delivery.py
Delivery configuration and status:
DeliveryConfig, DeliveryChannels: channels and batch strategies.
DeliveryStatus, DeliveryReport, ChannelDeliveryStats, FailedDelivery.
BatchDelivery: batch processing progress.
RetryDelivery: retry failed deliveries.
announcement/announcement_tracking.py
Engagement tracking:
ReadReceipt (+ response).
AcknowledgmentTracking, PendingAcknowledgment, AcknowledgmentRequest.
EngagementMetrics, ReadingTime.
AnnouncementAnalytics: comprehensive analytics combining delivery & engagement.
announcement/__init__.py
Re-exports key announcement schemas: base, response, targeting, scheduling, approval, delivery, tracking, filters.
Attendance Schemas (app/schemas/attendance)
attendance/attendance_base.py
Core attendance record model:
AttendanceBase: single-day attendance for a student.
AttendanceCreate, AttendanceUpdate: create/update payloads with optional geo/device info on create.
BulkAttendanceCreate, SingleAttendanceRecord: bulk marking structure.
attendance/attendance_response.py
Response models:
AttendanceResponse: list item with names, status, times.
AttendanceDetail: full attendance record with student info, mode, location, timestamps.
AttendanceListItem: minimal list row.
DailyAttendanceSummary: summarized statistics per day.
attendance/attendance_record.py
Higher-level commands:
AttendanceRecordRequest: simple per-student mark.
BulkAttendanceRequest: bulk mark with per-student overrides.
AttendanceCorrection: correction payload for existing record.
QuickAttendanceMarkAll: mark all present with exceptions.
attendance/attendance_filters.py
Filtering and export:
AttendanceFilterParams: hostels, students, dates, statuses, modes.
DateRangeRequest: simple validated date range.
AttendanceExportRequest: export options by format and grouping.
attendance/attendance_policy.py
Policy configuration and violations:
AttendancePolicy: hostel-specific thresholds and notifications.
PolicyConfig: calculation and leave-handling rules.
PolicyUpdate: partial changes to policy.
PolicyViolation: record of a violation instance.
attendance/attendance_alert.py
Alerts on attendance anomalies:
AttendanceAlert: alert log (low attendance, late, patterns).
AlertConfig: hostel-level alert settings.
AlertTrigger: manual trigger payload.
AlertAcknowledgment, AlertList, AlertSummary: acknowledging & summarizing alerts.
attendance/attendance_report.py
Reporting and trend analysis:
AttendanceReport: full report for a student/hostel over a period with summary, daily records, trends.
AttendanceSummary: overall stats and streaks.
DailyAttendanceRecord: per-day detail.
TrendAnalysis, WeeklyAttendance, MonthlyComparison: trends and comparisons.
MonthlyReport, StudentMonthlySummary.
AttendanceComparison, ComparisonItem: comparative attendance across entities.
attendance/__init__.py
Re-exports core attendance models (base, response, record, report, policy, alert, filters).
Audit Schemas (app/schemas/audit)
audit/admin_override_log.py
Audit logs specifically for admin overrides:
AdminOverrideBase, AdminOverrideCreate: base and create payload mirroring DB.
AdminOverrideLogResponse, AdminOverrideDetail: summarized and detailed views.
AdminOverrideSummary, AdminOverrideTimelinePoint: stats and timeline aggregation.
audit/audit_log_base.py
Generic audit log entry:
AuditLogBase, AuditLogCreate: base audit schema for all modules (action, category, entity, old/new values, request context).
audit/audit_log_response.py
Response views for generic audit logs:
AuditLogResponse: list item.
AuditLogDetail: includes old/new value snapshots.
audit/audit_filters.py
Filter criteria for querying audit logs:
AuditFilterParams: filter by user, role, hostel, entity, action, time range, paging.
audit/audit_reports.py
Reporting over audit logs:
AuditSummary, UserActivitySummary.
EntityChangeSummary, EntityChangeRecord, EntityChangeHistory.
AuditReport: top-level report with summaries by entity type.
audit/supervisor_activity_log.py
Supervisor-specific activity logging:
SupervisorActivityBase, SupervisorActivityCreate: create entries for actions by supervisors.
SupervisorActivityLogResponse, SupervisorActivityDetail.
SupervisorActivityFilter: filtering/paging.
SupervisorActivitySummary, SupervisorActivityTimelinePoint: aggregated stats.
audit/__init__.py
Re-exports generic audit, supervisor activity, and admin override log schemas.
Auth Schemas (app/schemas/auth)
auth/login.py
Login and JWT token data:
LoginRequest, PhoneLoginRequest.
TokenData: payload encoded into JWT.
LoginResponse, UserLoginInfo: tokens + basic user info.
auth/otp.py
OTP (One-Time Password) flows:
OTPGenerateRequest: generate for email/phone with purpose.
OTPVerifyRequest, OTPResponse, OTPVerifyResponse.
ResendOTPRequest.
Includes validator ensuring at least email or phone is supplied.
auth/password.py
Password reset/change and strength:
PasswordResetRequest, PasswordResetConfirm (with matching & strength validation).
PasswordChangeRequest, PasswordChangeResponse.
PasswordStrengthCheck, PasswordStrengthResponse.
auth/register.py
Registration and verification:
RegisterRequest: user creation payload with role, gender, DOB and password validation.
RegisterResponse.
VerifyEmailRequest, VerifyPhoneRequest, ResendVerificationRequest.
auth/social_auth.py
Social login via Google/Facebook:
SocialAuthRequest, GoogleAuthRequest, FacebookAuthRequest.
SocialAuthResponse, SocialUserInfo: tokens + user info.
SocialProfileData: structured profile returned from providers.
auth/token.py
Token management:
Token, TokenPayload: access/refresh representation and JWT claims.
RefreshTokenRequest, RefreshTokenResponse.
TokenValidationRequest, TokenValidationResponse.
RevokeTokenRequest, LogoutRequest.
auth/__init__.py
Re-exports main auth-related schemas: login, registration, tokens, password, OTP, social auth.
Booking Schemas (app/schemas/booking)
booking/booking_base.py
Core booking model:
BookingBase: requested room type, dates, pricing, extras, source.
Validates total_amount against (quoted_rent_monthly * stay_duration_months).
BookingCreate: embeds guest and contact details for a new booking.
BookingUpdate: modify booking attributes/status.
booking/booking_response.py
Read models:
BookingResponse: summary item.
BookingDetail: full booking details incl. hostel info, assignment, status history, cancellation, conversion, payment.
BookingListItem: list card with urgency flag.
BookingConfirmation: confirmation payload for guest.
booking/booking_request.py
Alternate booking entry points:
GuestInformation: nested guest data.
BookingRequest: more structured public booking API with validator checking future check-in date.
BookingInquiry: lighter-weight inquiry model.
QuickBookingRequest: minimal booking variant.
booking/booking_approval.py
Booking approval/rejection workflows:
BookingApprovalRequest: assign room/bed, confirm pricing, require advance.
ApprovalResponse: approval results (amounts, payment next steps).
RejectionRequest: structured rejection reasons and alternatives.
BulkApprovalRequest, ApprovalSettings: automated approvals config.
booking/booking_assignment.py
Room/bed assignment for bookings:
RoomAssignment, BedAssignment: assignment records.
AssignmentRequest, BulkAssignmentRequest, SingleAssignment: payloads for assigning/reassigning.
AssignmentResponse.
ReassignmentRequest.
booking/booking_calendar.py
Booking calendar and availability:
CalendarView, DayBookings, BookingEvent, CalendarEvent: day-wise events and bookings.
AvailabilityCalendar, DayAvailability: per-day availability tracking.
booking/booking_cancellation.py
Cancellation logic:
CancellationRequest, CancellationResponse.
RefundCalculation, CancellationPolicy, CancellationCharge.
BulkCancellation for multiple bookings.
booking/booking_conversion.py
Converting bookings into students:
ConvertToStudentRequest, ConversionResponse.
ConversionChecklist, ChecklistItem.
BulkConversion, ConversionRollback.
booking/booking_modification.py
Modifications after booking:
ModificationRequest, ModificationResponse.
Specific requests: DateChangeRequest, DurationChangeRequest, RoomTypeChangeRequest.
ModificationApproval for admin to approve/deny modifications.
booking/booking_filters.py
Filters, search, export, analytics:
BookingFilterParams, BookingSearchRequest, BookingSortOptions.
BookingExportRequest: export format & fields.
BookingAnalyticsRequest: time-grouped analytics.
booking/booking_waitlist.py
Waitlist handling when full:
WaitlistRequest, WaitlistResponse.
WaitlistStatus: per-visitor queue status.
WaitlistNotification, WaitlistConversion, WaitlistCancellation.
WaitlistManagement, WaitlistEntry: admin view & operations.
booking/__init__.py
Re-exports major booking-related schemas.
Common Schemas (app/schemas/common)
common/base.py
Base Pydantic configurations and mixins:
BaseSchema: standard config (from_orm-like, enum handling, JSON encoders).
TimestampMixin, SoftDeleteMixin, UUIDMixin.
BaseDBSchema: DB entity with ID + timestamps.
BaseCreateSchema, BaseUpdateSchema, BaseResponseSchema, BaseFilterSchema.
common/enums.py
Centralized enums for:
Roles, gender, hostel/room/bed status, booking, payment (type/method/status), complaints, maintenance, attendance, leaves, announcements, meal/dietary prefs, OTP and audit categories, subscription, student/supervisor statuses, review/referral/reward statuses, notifications, devices, search/inquiry/waitlist sources, charge types, and others.
common/filters.py
Reusable filter models:
DateRangeFilter, DateTimeRangeFilter, TimeRangeFilter.
PriceRangeFilter, NumericRangeFilter.
SearchFilter, SortOptions, StatusFilter, LocationFilter, MultiSelectFilter, BooleanFilter, TextSearchFilter.
Includes validators for consistent min/max and start/end semantics.
common/mixins.py
Small mixin models for reuse:
AddressMixin, ContactMixin, LocationMixin, MediaMixin.
EmergencyContactMixin, AuditMixin, ApprovalMixin, SEOMixin.
common/pagination.py
Pagination utilities:
PaginationParams, PaginationMeta, PaginatedResponse[T] with create helper.
CursorPaginationParams, CursorPaginationMeta, CursorPaginatedResponse[T] for cursor-based pagination.
common/response.py
Standardized API response wrappers:
SuccessResponse[T], ErrorDetail, ErrorResponse, MessageResponse.
BulkOperationResponse.
Specialized error responses: ValidationErrorResponse, NotFoundResponse, UnauthorizedResponse, ForbiddenResponse, ConflictResponse, RateLimitResponse.
common/__init__.py
Re-exports core base types, many enums, pagination, response, and basic filter types for convenience.
Complaint Schemas (app/schemas/complaint)
complaint/complaint_base.py
Core complaint model:
ComplaintBase: hostel, raiser, category, priority, location, attachments.
ComplaintCreate.
ComplaintUpdate: mutable fields and status.
ComplaintStatusUpdate: explicitly update status with notes.
complaint/complaint_response.py
Read models:
ComplaintResponse: list item with SLA/age info.
ComplaintDetail: full complaint lifecycle, assignment, escalation, override, resolution, feedback.
ComplaintListItem: simplified listing.
ComplaintSummary: dashboard summary counts and averages.
complaint/complaint_assignment.py
Assignment to staff:
AssignmentRequest, AssignmentResponse.
ReassignmentRequest, BulkAssignment, UnassignRequest.
complaint/complaint_resolution.py
Resolution/closure:
ResolutionRequest, ResolutionResponse, ResolutionUpdate.
ReopenRequest, CloseRequest.
complaint/complaint_escalation.py
Escalation handling:
EscalationRequest, EscalationResponse.
EscalationHistory, EscalationEntry.
AutoEscalationRule: SLA-based escalation settings.
complaint/complaint_feedback.py
Post-resolution feedback:
FeedbackRequest, FeedbackResponse.
FeedbackSummary: entity-level stats.
FeedbackAnalysis, RatingTrendPoint.
complaint/complaint_comments.py
Comments and mentions:
CommentCreate, CommentResponse, CommentList.
CommentUpdate, CommentDelete.
MentionNotification: mention alerts.
complaint/complaint_filters.py
Filtering/search/export:
ComplaintFilterParams, ComplaintSearchRequest, ComplaintSortOptions.
ComplaintExportRequest: export format and fields.
complaint/complaint_analytics.py (under complaint folder)
Complaint-specific analytics variants (parallel to analytics module but more detailed for this domain):
ComplaintAnalytics, ResolutionMetrics, CategoryAnalysis, CategoryMetrics, ComplaintTrendPoint.
StaffPerformance, ComplaintHeatmap, RoomComplaintCount.
complaint/__init__.py
Re-exports main complaint schemas.
Fee Structure Schemas (app/schemas/fee_structure)
fee_structure/fee_base.py
Base fee configuration:
FeeStructureBase: per-hostel/per-room-type fee attributes including mess and utilities (with ChargeType).
FeeStructureCreate, FeeStructureUpdate.
fee_structure/fee_config.py
Fee calculation configuration:
ChargesBreakdown: computed components (rent, mess, utilities).
FeeConfiguration: final configuration used to calculate total fees for a case.
fee_structure/fee_response.py
Read models:
FeeStructureResponse: one fee row.
FeeDetail: summarized first-month and recurring totals for a room type.
FeeStructureList: all structures for a hostel.
fee_structure/__init__.py
Re-exports base, response, and config schemas.
File Schemas (app/schemas/file)
file/file_upload.py
Generic upload initialization and completion:
FileUploadInitRequest, FileUploadInitResponse: for pre-signed URLs or similar.
FileUploadCompleteRequest: notify backend upload completed.
file/file_response.py
File metadata and listing:
FileMetadata: type, size, tags, custom metadata.
FileInfo: full record with ownership, URLs, audit.
FileURL: simple URL + expiry.
FileListResponse: basic paginated-ish listing.
file/image_upload.py
Image-specific uploads:
ImageUploadInitRequest: constraints and usage context.
ImageVariant, ImageUploadInitResponse: planned/generated variants.
ImageProcessingResult.
file/document_upload.py
Document uploads:
DocumentUploadInitRequest, DocumentUploadInitResponse.
DocumentValidationResult: backend validation outcome.
DocumentInfo, DocumentList: document-level views and verification flags.
file/__init__.py
Re-exports key file, image, and document upload/response types.
Hostel Schemas (app/schemas/hostel)
hostel/hostel_base.py
Base hostel definition:
HostelBase: details, address, contact, hostel type, pricing, amenities, rules, policies, SEO-like fields.
Validators for slug formatting and list cleanup.
HostelCreate: creation variant with required fields.
HostelUpdate: partial updates.
HostelMediaUpdate, HostelSEOUpdate: targeted updates.
hostel/hostel_response.py
Hostels for internal/admin views:
HostelResponse: basic card with status and key metrics.
HostelDetail: full internal details including capacity, policies, media, SEO, flags.
HostelListItem: minimal list representation.
HostelStats: aggregated stats for occupancy, revenue, complaints, bookings, reviews.
hostel/hostel_public.py
Public-facing hostel representations:
PublicHostelCard: listing card for visitors.
PublicHostelProfile: full public profile with ratings, policies, media, room types.
PublicRoomType: specific room type pricing and availability.
PublicHostelList: results with filters summary.
hostel/hostel_admin.py
Admin-specific view and settings:
HostelAdminView: summary for admins with status, stats, subscription, performance.
HostelSettings: configuration toggles (booking, payments, attendance, notifications, mess).
HostelVisibilityUpdate, HostelCapacityUpdate, HostelStatusUpdate.
hostel/hostel_analytics.py
Hostel-level analytics (duplicate name but distinct from /analytics):
HostelAnalytics: aggregate occupancy, revenue, bookings, complaints, reviews for a hostel over period.
Submodels: OccupancyAnalytics, OccupancyDataPoint, RevenueAnalytics, RevenueDataPoint, BookingAnalytics, BookingDataPoint, ComplaintAnalytics, ReviewAnalytics, RatingDataPoint.
HostelOccupancyStats, RoomTypeOccupancy, HostelRevenueStats, MonthlyRevenue, AnalyticsRequest.
hostel/hostel_filter.py
Filter, sorting, advanced filters, bulk filters for hostels:
HostelFilterParams, HostelSortOptions, AdvancedFilters, BulkFilterParams.
hostel/hostel_search.py
Search request/response, facets for hostels:
HostelSearchRequest: rich filters and sorting.
HostelSearchResponse: with facets and filters summary.
SearchFacets, FacetItem, PriceRangeFacet, RatingFacet.
HostelSearchFilters: extra advanced filters (gender, facilities, rules, date).
hostel/hostel_comparison.py
Hostel comparison tool:
HostelComparisonRequest: up to 4 hostels IDs.
ComparisonResult, ComparisonItem: detailed per-hostel comparison attributes.
RoomTypeComparison.
ComparisonSummary, PriceComparison, AmenityComparison.
hostel/__init__.py
Re-exports base, public/admin, search/filter, analytics, and comparison models.
Inquiry Schemas (app/schemas/inquiry)
inquiry/inquiry_base.py
Base visitor inquiry:
InquiryBase: contact info, preferences, message, source, status.
InquiryCreate: create payload.
inquiry/inquiry_response.py
Read models:
InquiryResponse: basic list item.
InquiryDetail: full view with status, contact details, notes.
InquiryListItem: minimal list representation.
inquiry/inquiry_status.py
Status changes and assignment:
InquiryStatusUpdate: change status with optional notes.
InquiryAssignment: assign to admin/staff.
InquiryTimelineEntry: tracks lifecycle.
inquiry/__init__.py
Exposes base, response, and status schemas.
Leave Schemas (app/schemas/leave)
leave/leave_base.py
Base leave application:
LeaveBase: type, dates, total_days, reason, contacts, document URL, with validator for total_days consistency.
LeaveCreate, LeaveUpdate.
leave/leave_application.py
Student-facing leave flows:
LeaveApplicationRequest: simplified submission.
LeaveCancellationRequest: request to cancel an existing leave.
leave/leave_approval.py
Approval workflow:
LeaveApprovalRequest: supervisor/admin approval or rejection.
LeaveApprovalResponse: updated status and metadata.
leave/leave_balance.py
Leave balances:
LeaveBalance: per-type counts.
LeaveBalanceSummary: overall annual summary per student.
leave/leave_response.py
Read models:
LeaveResponse: list item.
LeaveDetail: detailed record with approval/rejection, reasons, cancellations.
LeaveListItem: compact listing.
leave/__init__.py
Re-exports main leave schemas.
Maintenance Schemas (app/schemas/maintenance)
maintenance/maintenance_base.py
Base maintenance request:
MaintenanceBase: hostel, requester, category, priority, issue type, location, photos.
MaintenanceCreate.
MaintenanceUpdate: status and cost updates.
MaintenanceStatusUpdate.
maintenance/maintenance_response.py
Read models:
MaintenanceResponse: list item summary.
MaintenanceDetail: full lifecycle, assignment, vendor, costs, photos, QC, preventive fields.
RequestListItem, MaintenanceSummary: admin list and summary metrics.
maintenance/maintenance_request.py
Request submission flows:
MaintenanceRequest: simple request model.
RequestSubmission: richer supervisor submission including estimated cost, vendor, days.
EmergencyRequest: emergency incident details.
maintenance/maintenance_assignment.py
Task/vendor assignment:
TaskAssignment: record of assignment to staff.
VendorAssignment, AssignmentUpdate, BulkAssignment.
AssignmentHistory, AssignmentEntry.
maintenance/maintenance_approval.py
Cost approval:
ApprovalRequest, ApprovalResponse.
ThresholdConfig: cost thresholds for approvals.
ApprovalWorkflow.
RejectionRequest.
maintenance/maintenance_completion.py
Completion and QC:
CompletionRequest: work done, materials used, costs, timeline.
MaterialItem.
QualityCheck, ChecklistItem.
CompletionResponse, CompletionCertificate.
maintenance/maintenance_cost.py
Cost tracking and budgets:
CostTracking: per-request financial breakdown.
BudgetAllocation, CategoryBudget.
ExpenseReport, MonthlyExpense, ExpenseItem.
VendorInvoice, InvoiceLineItem.
CostAnalysis: trends and ratios.
maintenance/maintenance_filters.py
Filtering and exports:
MaintenanceFilterParams, SearchRequest.
MaintenanceExportRequest.
maintenance/maintenance_schedule.py
Preventive maintenance:
PreventiveSchedule, ScheduleCreate, ScheduleUpdate.
ScheduleChecklistItem.
RecurrenceConfig.
ScheduleExecution, ChecklistResult.
ScheduleHistory, ExecutionHistoryItem.
maintenance/maintenance_analytics.py
Maintenance analytics:
MaintenanceAnalytics: high-level stats, costs, performance, trends.
TrendPoint, CostTrendPoint.
CategoryBreakdown.
VendorPerformance.
maintenance/__init__.py
Re-exports core maintenance-related schemas (base, response, request, assignment, approval, completion, schedule, cost, filters, analytics). Note: PerformanceMetrics is imported but not defined here (potential missing/typo).
Mess Schemas (app/schemas/mess)
mess/mess_menu_base.py
Base mess menu definition:
MessMenuBase: meals per day, times, special flags, dietary options.
MessMenuCreate: adds created_by.
MessMenuUpdate: partial updates.
mess/mess_menu_response.py
Read models:
MenuResponse: basic daily menu card with rating and publish status.
MenuDetail: full details with times, dietary options, approvals, ratings.
WeeklyMenu, DailyMenuSummary, MonthlyMenu: aggregated menu structures.
TodayMenu: simplified daily menu for students.
mess/meal_items.py
Meal items and dietary details:
MealItems, MenuItem: define items and dietary flags/allergens.
DietaryOptions: hostel-level options and customization flags.
NutritionalInfo: macros/micros for items.
ItemMasterList, ItemCategory: master menu catalog.
mess/menu_approval.py
Menu approval:
MenuApprovalRequest, MenuApprovalResponse.
ApprovalWorkflow.
BulkApproval.
mess/menu_duplication.py
Menu duplication and bulk creation:
DuplicateMenuRequest, DuplicateResponse.
BulkMenuCreate: generate menus across a date range from templates/patterns.
CrossHostelDuplication.
mess/menu_feedback.py
Menu feedback & quality:
FeedbackRequest, FeedbackResponse.
RatingsSummary, QualityMetrics, ItemRating.
FeedbackAnalysis: sentiment and recommendations.
mess/menu_planning.py
Planning tools:
MenuPlanRequest, WeeklyPlan, DailyMenuPlan, MonthlyPlan.
SpecialMenu, SpecialDayMenu.
MenuTemplate, MenuSuggestion.
mess/__init__.py
Re-exports menu base/response, meal items, planning, feedback, approval, duplication.
Notification Schemas (app/schemas/notification)
notification/notification_base.py
Generic notification model:
NotificationBase: recipients, type, content, priority, schedule, metadata.
NotificationCreate, NotificationUpdate.
MarkAsRead, BulkMarkAsRead, NotificationDelete.
notification/notification_response.py
Notification response & listing:
NotificationResponse, NotificationDetail.
NotificationList, NotificationListItem.
UnreadCount, NotificationSummary.
notification/notification_template.py
Templates for notifications:
TemplateCreate, TemplateUpdate, TemplateResponse.
VariableMapping, TemplatePreview, TemplatePreviewResponse, TemplateList, TemplateCategory.
notification/email_notification.py
Email-specific sending:
EmailRequest, EmailConfig.
EmailTracking, EmailTemplate, BulkEmailRequest, EmailStats.
notification/sms_notification.py
SMS-specific sending:
SMSRequest, SMSConfig.
DeliveryStatus, SMSTemplate, BulkSMSRequest, SMSStats.
notification/push_notification.py
Push notifications and devices:
PushRequest, PushConfig.
DeviceToken, DeviceRegistration, DeviceUnregistration.
PushTemplate, PushDeliveryStatus, PushStats.
notification/notification_queue.py
Queue and batch processing:
QueueStatus, QueuedNotification, BatchProcessing, QueueStats.
notification/notification_preferences.py
User-level preferences:
UserPreferences, ChannelPreferences with EmailPreferences, SMSPreferences, PushPreferences.
FrequencySettings.
PreferenceUpdate, UnsubscribeRequest.
notification/notification_routing.py
Routing configurations:
RoutingConfig, RoutingRule.
HierarchicalRouting, EscalationRouting, EscalationLevel.
NotificationRoute.
notification/__init__.py
Re-exports base, responses, templates, channels, queue, preferences, routing.
Payment Schemas (app/schemas/payment)
payment/payment_base.py
Base payment schema:
PaymentBase: payer, hostel, type, amount, period, method, due_date.
PaymentCreate: adds transaction and collector.
PaymentUpdate: status, timestamps, failure, receipt info.
payment/payment_response.py
Payment read models:
PaymentResponse: list card summarizing payment.
PaymentDetail: full payment record with relationships, gateway data, refunds, reminders.
PaymentReceipt: printable receipt info.
PaymentListItem, PaymentSummary: summary for student/hostel.
payment/payment_request.py
Payment initiation and manual logging:
PaymentRequest: for online gateway payments.
PaymentInitiation: response with gateway order/token.
ManualPaymentRequest: cash/cheque/bank_transfer recording.
BulkPaymentRequest, SinglePaymentRecord.
payment/payment_gateway.py
Gateway integration:
GatewayRequest, GatewayResponse: order creation and gateway state.
GatewayWebhook, GatewayCallback: incoming webhook and handling.
GatewayRefundRequest, GatewayRefundResponse.
payment/payment_refund.py
Refund lifecycle:
RefundRequest, RefundResponse.
RefundStatus, RefundApproval, RefundList, RefundListItem.
payment/payment_ledger.py
Ledger/statement:
LedgerEntry, LedgerSummary, AccountStatement.
TransactionHistory, TransactionItem.
BalanceAdjustment, WriteOff.
payment/payment_reminder.py
Payment reminder configuration & logs:
ReminderConfig.
ReminderLog, SendReminderRequest, ReminderBatch, ReminderStats.
payment/payment_schedule.py
Recurring payment schedules:
PaymentSchedule, ScheduleCreate, ScheduleUpdate.
ScheduleGeneration, ScheduledPaymentGenerated.
BulkScheduleCreate, ScheduleSuspension.
payment/payment_filters.py
Filtering/report/export:
PaymentFilterParams, PaymentSearchRequest.
PaymentReportRequest: grouped report generation options.
PaymentExportRequest: export fields and format.
payment/__init__.py
Re-exports major payment, gateway, refund, schedule, reminder, ledger, and filter models.
Referral Schemas (app/schemas/referral)
referral/referral_base.py
Core referral record:
ReferralBase: program, referrer, referee identifiers, referral code, status.
ReferralCreate.
referral/referral_code.py
Referral code management:
ReferralCodeGenerate, ReferralCodeResponse.
CodeValidationRequest, CodeValidationResponse.
referral/referral_program_base.py
Referral program definition:
ReferralProgramBase: reward types/amounts, thresholds, validity.
ProgramCreate, ProgramUpdate.
referral/referral_program_response.py
Read-only program responses:
ProgramResponse, ProgramList.
referral/referral_response.py
Referral record read models:
ReferralResponse: details about one referral + reward statuses.
ReferralStats: per-user aggregated stats.
referral/referral_rewards.py
Reward configuration and payouts:
RewardConfig: min payout & methods.
RewardTracking: per-user accumulated rewards.
PayoutRequest, PayoutRequestResponse.
referral/__init__.py
(Empty) initializer; no exports defined in snippet.
Review Schemas (app/schemas/review)
review/review_base.py
Base review model:
ReviewBase: hostel, reviewer, ratings (overall + aspects), text, photos.
Rounds overall rating to nearest 0.5.
ReviewCreate, ReviewUpdate.
review/review_response.py
Read models:
ReviewResponse: basic review list card.
ReviewDetail: full content, ratings, moderation flags, hostel response.
HostelResponseDetail.
ReviewListItem: trimmed list view.
ReviewSummary: summary for a hostel.
review/review_submission.py
Public submission flows:
ReviewSubmissionRequest: visitor submission including verification, detailed ratings, photos, recommendations, stay details, guidelines agreement.
DetailedRatings.
VerifiedReview: marking/recording verified reviews.
ReviewGuidelines.
ReviewEligibility: logic to check if user can submit/edit.
review/review_filters.py
Filtering/search/export:
ReviewFilterParams, SearchRequest, SortOptions.
ReviewExportRequest.
review/review_moderation.py
Moderation workflow:
ModerationRequest, ModerationResponse.
ModerationQueue, PendingReview.
ApprovalWorkflow, BulkModeration, ModerationStats.
review/review_voting.py
Helpfulness voting:
VoteRequest, VoteResponse.
HelpfulnessScore.
VoteHistory, VoteHistoryItem, RemoveVote.
review/review_response_schema.py
Hostel/owner responses to reviews:
HostelResponseCreate, OwnerResponse, ResponseUpdate.
ResponseGuidelines, ResponseStats.
review/review_analytics.py
Analytics for reviews:
ReviewAnalytics, RatingDistribution, TrendAnalysis, MonthlyRating.
SentimentAnalysis, AspectAnalysis, CompetitorComparison.
review/__init__.py
Re-exports core review, submission, moderation, voting, hostel response, filters, and analytics.
Room Schemas (app/schemas/room)
room/room_base.py
Base room definition:
RoomBase: hostel, number, type, capacity, pricing, specifications, amenities, availability flags, media.
RoomCreate.
RoomUpdate, BulkRoomCreate.
RoomPricingUpdate, RoomStatusUpdate.
room/room_response.py
Room read models:
RoomResponse: summary.
RoomDetail: full details including beds.
BedDetail.
RoomListItem.
RoomWithBeds, BedInfo.
RoomOccupancyStats.
room/bed_base.py
Bed management:
BedBase, BedCreate, BedUpdate.
BulkBedCreate.
BedAssignmentRequest, BedReleaseRequest.
room/bed_response.py
Bed read models:
BedResponse: single bed record.
BedAvailability.
BedAssignment.
BedHistory, BedAssignmentHistory.
room/room_availability.py
Availability checking/calendar:
RoomAvailabilityRequest, AvailabilityResponse.
AvailableRoom.
AvailabilityCalendar, DayAvailability, BookingInfo.
room/__init__.py
Re-exports core room and bed schemas plus availability.
Search Schemas (app/schemas/search)
search/search_analytics.py
Stats around search terms:
SearchTermStats: counts, avg results, zero-result stats.
SearchAnalytics: aggregated metrics and lists of top and zero-result terms.
search/search_autocomplete.py
Autocomplete:
AutocompleteRequest: prefix-based request.
Suggestion, AutocompleteResponse.
search/search_filters.py
Simple filter blocks:
PriceFilter, RatingFilter, AmenityFilter.
search/search_request.py
Search API request shapes:
BasicSearchRequest.
AdvancedSearchRequest: multiple filters, geo radius, sort, pagination.
search/search_response.py
Search results:
SearchResultItem: attaches a score to PublicHostelCard.
FacetBucket, FacetedSearchResponse.
search/search_sort.py
Sort criteria:
SortCriteria: simple sort-by and order.
search/__init__.py
Empty initializer (no exports shown).
Student Schemas (app/schemas/student)
student/student_base.py
Base student model (hostel context):
StudentBase: linking user to hostel, room, bed; guardian, institutional or employment info; dates; finances; mess and dietary details, with validation for checkout after check-in.
StudentCreate: includes optional origin booking.
StudentUpdate: partial updates including status.
student/student_response.py
Read models:
StudentResponse: list view summarizing status and key fields.
StudentDetail: full profile including guardian, institution, employment, financials, documents.
StudentProfile: public-facing minimal profile.
StudentListItem: admin list row.
StudentFinancialInfo: detailed financials.
StudentContactInfo: contact/guardian/emergency info.
student/student_profile.py
Student profile (as extension of user):
StudentProfileCreate, StudentProfileUpdate: for initial capture and updates (guardian, institution, employment, preferences).
StudentDocuments, DocumentInfo: document management.
DocumentUploadRequest, DocumentVerificationRequest.
StudentPreferences: toggles on mess, notifications, privacy.
student/student_dashboard.py
Student dashboard view:
StudentDashboard: overview.
StudentFinancialSummary, AttendanceSummary, StudentStats.
RecentPayment, RecentComplaint, PendingLeave, RecentAnnouncement, TodayMessMenu.
student/student_filters.py
Filtering/search/bulk ops:
StudentFilterParams, StudentSearchRequest, StudentSortOptions.
StudentExportRequest, StudentBulkActionRequest.
student/student_room_history.py
Room history and transfers:
RoomHistoryResponse, RoomHistoryItem.
RoomTransferRequest, RoomTransferApproval, RoomTransferStatus.
BulkRoomTransfer, SingleTransfer.
student/__init__.py
Re-exports primary base, response, profile, room history, dashboard, and filter schemas.
Subscription Schemas (app/schemas/subscription)
subscription/subscription_plan_base.py
Plan definition:
SubscriptionPlanBase: plan name, type, pricing, feature flags, limits, visibility.
PlanCreate, PlanUpdate.
subscription/subscription_plan_response.py
Plan read models:
PlanResponse.
PlanFeatures: user-friendly feature labels.
PlanComparison: cross-plan feature matrix.
subscription/subscription_base.py
Hostel subscription instance:
SubscriptionBase: which hostel, which plan, billing cycle, period, auto-renew, status.
SubscriptionCreate: adds optional trial.
SubscriptionUpdate.
subscription/subscription_response.py
Subscription read models:
SubscriptionResponse: details for one subscription.
BillingHistoryItem, BillingHistory: historical billing info.
subscription/subscription_billing.py
Billing & invoicing:
BillingCycleInfo.
GenerateInvoiceRequest, InvoiceInfo.
subscription/subscription_cancellation.py
Cancellation:
CancellationRequest, CancellationResponse.
subscription/commission.py
Booking commission logic:
CommissionConfig: global defaults and per-plan overrides.
BookingCommissionResponse.
CommissionSummary.
subscription/subscription_upgrade.py
Upgrade/downgrade:
UpgradeRequest, UpgradePreview, DowngradeRequest.
subscription/__init__.py
(Empty) initializer; no explicit exports shown.
Supervisor Schemas (app/schemas/supervisor)
supervisor/supervisor_base.py
Base supervisor model:
SupervisorBase: relationship to user and hostel, employment details.
SupervisorCreate: includes assigner and initial permissions.
SupervisorUpdate.
SupervisorStatusUpdate.
SupervisorReassignment.
supervisor/supervisor_response.py
Read models:
SupervisorResponse.
SupervisorDetail: full details including permissions and performance metrics.
SupervisorListItem, SupervisorSummary.
supervisor/supervisor_profile.py
Supervisor profile and employment summary:
SupervisorProfile: aggregated view with employment, permissions, performance.
SupervisorEmployment.
PerformanceSummary.
SupervisorProfileUpdate: self-editable fields.
supervisor/supervisor_permissions.py
Supervisor permissions:
SupervisorPermissions: boolean flags and thresholds across many modules.
PermissionUpdate: generic update by key, with validation.
PermissionCheckRequest, PermissionCheckResponse.
BulkPermissionUpdate.
PermissionTemplate, ApplyPermissionTemplate.
supervisor/supervisor_assignment.py
Assignment to hostels:
SupervisorAssignment: response model.
AssignmentRequest, AssignmentUpdate.
RevokeAssignmentRequest, AssignmentTransfer.
supervisor/supervisor_activity.py
Activity logs & analytics (distinct from audit version):
SupervisorActivityLog: list item response.
ActivityDetail, ActivitySummary, TopActivity, ActivityTimelinePoint.
ActivityFilterParams.
ActivityExportRequest.
supervisor/supervisor_dashboard.py
Supervisor dashboard:
SupervisorDashboard, DashboardMetrics, TaskSummary.
RecentComplaintItem, RecentMaintenanceItem, PendingLeaveItem.
TodaySchedule, ScheduledMaintenanceItem, ScheduledMeeting, DashboardAlert.
QuickActions, QuickAction.
supervisor/supervisor_performance.py
Performance metrics & reviews:
PerformanceMetrics, PerformanceReport.
ComplaintPerformance, AttendancePerformance, MaintenancePerformance.
PerformanceTrendPoint, PeerComparison, MetricComparison, PeriodComparison.
PerformanceReview, PerformanceReviewResponse.
PerformanceGoal, PerformanceGoalProgress.
supervisor/__init__.py
Re-exports key supervisor base, response, profile, permissions, assignment, activity, dashboard, and performance schemas.
User Schemas (app/schemas/user)
user/user_base.py
Base user model:
UserBase: email, phone, full name, role, gender, DOB, profile image; age validator.
UserCreate: adds password with strength validation.
UserUpdate.
UserAddressUpdate, UserEmergencyContactUpdate (via mixins).
user/user_profile.py
Profile updates:
ProfileUpdate: personal and address fields.
ProfileImageUpdate.
ContactInfoUpdate.
NotificationPreferencesUpdate: top-level toggles for per-user notifications.
user/user_response.py
User read models:
UserResponse: basic info.
UserDetail: extended info including address and verification states.
UserListItem: admin list.
UserProfile: public profile.
user/user_session.py
Sessions management:
UserSession: DB record for sessions.
SessionInfo, ActiveSessionsList.
RevokeSessionRequest, RevokeAllSessionsRequest.
user/__init__.py
Re-exports user base, responses, profile updates, and session schemas.
Visitor Schemas (app/schemas/visitor)
visitor/visitor_base.py
Base visitor profile:
VisitorBase: preferences (room type, budget, cities, amenities), favorites, notification preferences.
VisitorCreate, VisitorUpdate.
visitor/visitor_response.py
Visitor read models:
VisitorResponse: summary of preferences and stats.
VisitorProfile: public info.
VisitorDetail: full visitor activity and preferences.
visitor/visitor_preferences.py
Detailed preferences & saved searches:
VisitorPreferences: comprehensive preference model and notification triggers; budget validator.
PreferenceUpdate.
SearchPreferences, SavedSearch.
visitor/visitor_dashboard.py
Visitor dashboard:
VisitorDashboard: high-level overview.
SavedHostels, SavedHostelItem.
BookingHistory, BookingHistoryItem.
RecentSearch, RecentlyViewedHostel, RecommendedHostel.
PriceDropAlert, AvailabilityAlert.
visitor/visitor_favorites.py
Favorites/wishlist:
FavoriteRequest, FavoritesList, FavoriteHostelItem, FavoriteUpdate, FavoritesExport, FavoriteComparison.
visitor/__init__.py
Re-exports core visitor base, response, preferences, dashboard, and favorites schemas.
