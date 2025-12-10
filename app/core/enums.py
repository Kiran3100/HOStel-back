"""
Core application enumerations.

This module contains all enumeration classes used throughout the application.
Enums provide type safety and ensure consistent values across the system.
"""

from enum import Enum


# ==================== User Enumerations ====================

class UserType(str, Enum):
    """User type enumeration."""
    SUPER_ADMIN = "super_admin"
    HOSTEL_ADMIN = "hostel_admin"
    SUPERVISOR = "supervisor"
    STUDENT = "student"
    VISITOR = "visitor"
    GUEST = "guest"
    STAFF = "staff"


class UserStatus(str, Enum):
    """User account status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"
    DELETED = "deleted"
    LOCKED = "locked"
    VERIFICATION_PENDING = "verification_pending"


class GenderType(str, Enum):
    """Gender type enumeration."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


# ==================== Payment Enumerations ====================

class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    INITIATED = "initiated"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class PaymentMethod(str, Enum):
    """Payment method enumeration."""
    CASH = "cash"
    CARD = "card"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    UPI = "upi"
    NET_BANKING = "net_banking"
    WALLET = "wallet"
    CHEQUE = "cheque"
    BANK_TRANSFER = "bank_transfer"
    EMI = "emi"


class FeeType(str, Enum):
    """Fee type enumeration."""
    ROOM_RENT = "room_rent"
    MESS_FEE = "mess_fee"
    SECURITY_DEPOSIT = "security_deposit"
    MAINTENANCE = "maintenance"
    UTILITY_BILLS = "utility_bills"
    ELECTRICITY = "electricity"
    WATER = "water"
    LATE_FEE = "late_fee"
    REGISTRATION_FEE = "registration_fee"
    ADMISSION_FEE = "admission_fee"
    PARKING_FEE = "parking_fee"
    INTERNET_FEE = "internet_fee"
    OTHER = "other"


class TransactionType(str, Enum):
    """Transaction type enumeration."""
    CREDIT = "credit"
    DEBIT = "debit"


class RefundStatus(str, Enum):
    """Refund status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


# ==================== Booking Enumerations ====================

class BookingStatus(str, Enum):
    """Booking status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    COMPLETED = "completed"
    EXPIRED = "expired"
    REJECTED = "rejected"
    ON_HOLD = "on_hold"
    AWAITING_PAYMENT = "awaiting_payment"


class BookingType(str, Enum):
    """Booking type enumeration."""
    REGULAR = "regular"
    PREMIUM = "premium"
    EMERGENCY = "emergency"
    TEMPORARY = "temporary"
    LONG_TERM = "long_term"


# ==================== Complaint Enumerations ====================

class ComplaintCategory(str, Enum):
    """Complaint category enumeration."""
    MAINTENANCE = "maintenance"
    CLEANLINESS = "cleanliness"
    SECURITY = "security"
    FOOD = "food"
    FACILITIES = "facilities"
    STAFF_BEHAVIOR = "staff_behavior"
    NOISE = "noise"
    ELECTRICITY = "electricity"
    WATER_SUPPLY = "water_supply"
    INTERNET = "internet"
    SAFETY = "safety"
    HARASSMENT = "harassment"
    OTHER = "other"


class ComplaintStatus(str, Enum):
    """Complaint status enumeration."""
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    PENDING_APPROVAL = "pending_approval"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    REOPENED = "reopened"


class Priority(str, Enum):
    """Priority level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    URGENT = "urgent"


# ==================== Room & Bed Enumerations ====================

class RoomType(str, Enum):
    """Room type enumeration."""
    SINGLE = "single"
    DOUBLE = "double"
    TRIPLE = "triple"
    QUAD = "quad"
    DORMITORY = "dormitory"
    SUITE = "suite"
    STUDIO = "studio"
    DELUXE = "deluxe"
    PREMIUM = "premium"


class BedStatus(str, Enum):
    """Bed status enumeration."""
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    UNDER_MAINTENANCE = "under_maintenance"
    BLOCKED = "blocked"
    OUT_OF_SERVICE = "out_of_service"


class RoomStatus(str, Enum):
    """Room status enumeration."""
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    PARTIALLY_OCCUPIED = "partially_occupied"
    UNDER_MAINTENANCE = "under_maintenance"
    RESERVED = "reserved"
    OUT_OF_SERVICE = "out_of_service"


# ==================== Maintenance Enumerations ====================

class MaintenanceStatus(str, Enum):
    """Maintenance status enumeration."""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    APPROVED = "approved"
    REJECTED = "rejected"
    ON_HOLD = "on_hold"
    AWAITING_PARTS = "awaiting_parts"


class MaintenanceCategory(str, Enum):
    """Maintenance category enumeration."""
    PLUMBING = "plumbing"
    ELECTRICAL = "electrical"
    FURNITURE = "furniture"
    CLEANING = "cleaning"
    HVAC = "hvac"
    PEST_CONTROL = "pest_control"
    PAINTING = "painting"
    CARPENTRY = "carpentry"
    APPLIANCE_REPAIR = "appliance_repair"
    STRUCTURAL = "structural"
    RENOVATION = "renovation"
    LANDSCAPING = "landscaping"
    OTHER = "other"


class MaintenanceType(str, Enum):
    """Maintenance type enumeration."""
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    EMERGENCY = "emergency"
    ROUTINE = "routine"


# ==================== Notice Enumerations ====================

class NoticeType(str, Enum):
    """Notice type enumeration."""
    GENERAL = "general"
    EMERGENCY = "emergency"
    EVENT = "event"
    MAINTENANCE = "maintenance"
    RULE_CHANGE = "rule_change"
    HOLIDAY = "holiday"
    ANNOUNCEMENT = "announcement"
    WARNING = "warning"
    CELEBRATION = "celebration"
    MEETING = "meeting"


class TargetAudience(str, Enum):
    """Target audience enumeration."""
    ALL = "all"
    STUDENTS = "students"
    STAFF = "staff"
    ADMINS = "admins"
    SUPERVISORS = "supervisors"
    VISITORS = "visitors"
    SPECIFIC_HOSTEL = "specific_hostel"
    SPECIFIC_ROOM = "specific_room"
    SPECIFIC_FLOOR = "specific_floor"


class NoticeStatus(str, Enum):
    """Notice status enumeration."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    EXPIRED = "expired"


# ==================== Subscription Enumerations ====================

class SubscriptionPlan(str, Enum):
    """Subscription plan enumeration."""
    FREE = "free"
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    TRIAL = "trial"


class SubscriptionStatus(str, Enum):
    """Subscription status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    TRIAL = "trial"
    PENDING = "pending"


class BillingCycle(str, Enum):
    """Billing cycle enumeration."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    HALF_YEARLY = "half_yearly"
    YEARLY = "yearly"
    BIENNIAL = "biennial"


# ==================== Attendance Enumerations ====================

class AttendanceStatus(str, Enum):
    """Attendance status enumeration."""
    PRESENT = "present"
    ABSENT = "absent"
    ON_LEAVE = "on_leave"
    LATE = "late"
    HALF_DAY = "half_day"
    EXCUSED = "excused"
    UNEXCUSED = "unexcused"


class AttendanceMode(str, Enum):
    """Attendance mode enumeration."""
    CHECK_IN = "check_in"
    CHECK_OUT = "check_out"
    BOTH = "both"
    MANUAL = "manual"
    AUTOMATIC = "automatic"


class LeaveStatus(str, Enum):
    """Leave status enumeration."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class LeaveType(str, Enum):
    """Leave type enumeration."""
    CASUAL = "casual"
    SICK = "sick"
    EMERGENCY = "emergency"
    VACATION = "vacation"
    MEDICAL = "medical"
    FAMILY = "family"
    OTHER = "other"


# ==================== Menu Enumerations ====================

class MealType(str, Enum):
    """Meal type enumeration."""
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACKS = "snacks"
    BRUNCH = "brunch"
    SUPPER = "supper"


class DietType(str, Enum):
    """Diet type enumeration."""
    VEGETARIAN = "vegetarian"
    NON_VEGETARIAN = "non_vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    JAIN = "jain"
    HALAL = "halal"
    KOSHER = "kosher"
    KETO = "keto"
    PALEO = "paleo"


class MenuStatus(str, Enum):
    """Menu status enumeration."""
    DRAFT = "draft"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


# ==================== Hostel Enumerations ====================

class HostelType(str, Enum):
    """Hostel type enumeration."""
    BOYS = "boys"
    GIRLS = "girls"
    CO_ED = "co_ed"
    WORKING_PROFESSIONALS = "working_professionals"
    STUDENTS = "students"
    PG = "pg"


class HostelStatus(str, Enum):
    """Hostel status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNDER_CONSTRUCTION = "under_construction"
    MAINTENANCE = "maintenance"
    CLOSED = "closed"
    COMING_SOON = "coming_soon"


class VisibilityStatus(str, Enum):
    """Visibility status enumeration."""
    PUBLIC = "public"
    PRIVATE = "private"
    HIDDEN = "hidden"
    UNLISTED = "unlisted"


# ==================== Approval Enumerations ====================

class ApprovalStatus(str, Enum):
    """Approval status enumeration."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"


class ApprovalType(str, Enum):
    """Approval type enumeration."""
    BOOKING = "booking"
    PAYMENT = "payment"
    MAINTENANCE = "maintenance"
    COMPLAINT = "complaint"
    LEAVE = "leave"
    EXPENSE = "expense"
    REFUND = "refund"
    STUDENT_ADMISSION = "student_admission"


# ==================== Notification Enumerations ====================

class NotificationStatus(str, Enum):
    """Notification status enumeration."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    BOUNCED = "bounced"


class NotificationPriority(str, Enum):
    """Notification priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class NotificationType(str, Enum):
    """Notification type enumeration."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"
    WEBHOOK = "webhook"
    SLACK = "slack"


class NotificationChannel(str, Enum):
    """Notification channel enumeration."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"
    ALL = "all"


# ==================== File Enumerations ====================

class FileType(str, Enum):
    """File type enumeration."""
    IMAGE = "image"
    DOCUMENT = "document"
    PDF = "pdf"
    VIDEO = "video"
    AUDIO = "audio"
    SPREADSHEET = "spreadsheet"
    PRESENTATION = "presentation"
    ARCHIVE = "archive"
    OTHER = "other"


class FileStatus(str, Enum):
    """File status enumeration."""
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
    DELETED = "deleted"


# ==================== Review Enumerations ====================

class ReviewStatus(str, Enum):
    """Review status enumeration."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FLAGGED = "flagged"
    REMOVED = "removed"


class ReviewCategory(str, Enum):
    """Review category enumeration."""
    HOSTEL_FACILITIES = "hostel_facilities"
    FOOD_QUALITY = "food_quality"
    SECURITY = "security"
    CLEANLINESS = "cleanliness"
    MANAGEMENT = "management"
    STAFF_BEHAVIOR = "staff_behavior"
    VALUE_FOR_MONEY = "value_for_money"
    LOCATION = "location"
    OVERALL_EXPERIENCE = "overall_experience"


# ==================== Supervisor Enumerations ====================

class SupervisorRole(str, Enum):
    """Supervisor role enumeration."""
    MANAGER = "manager"
    WARDEN = "warden"
    ASSISTANT_WARDEN = "assistant_warden"
    SECURITY = "security"
    MAINTENANCE_STAFF = "maintenance_staff"
    KITCHEN_STAFF = "kitchen_staff"
    HOUSEKEEPING = "housekeeping"
    RECEPTIONIST = "receptionist"


class Department(str, Enum):
    """Department enumeration."""
    ADMINISTRATION = "administration"
    MAINTENANCE = "maintenance"
    SECURITY = "security"
    FOOD_SERVICE = "food_service"
    HOUSEKEEPING = "housekeeping"
    IT = "it"
    ACCOUNTS = "accounts"
    HR = "hr"


class AccessLevel(str, Enum):
    """Access level enumeration."""
    READ = "read"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    FULL_ACCESS = "full_access"


# ==================== Invitation Enumerations ====================

class InvitationStatus(str, Enum):
    """Invitation status enumeration."""
    PENDING = "pending"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


# ==================== Log Enumerations ====================

class LogLevel(str, Enum):
    """Log level enumeration."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditAction(str, Enum):
    """Audit action enumeration."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    APPROVE = "approve"
    REJECT = "reject"
    EXPORT = "export"
    IMPORT = "import"
    DOWNLOAD = "download"
    UPLOAD = "upload"
    SEND = "send"
    RECEIVE = "receive"


# ==================== Currency Enumerations ====================

class Currency(str, Enum):
    """Currency enumeration."""
    INR = "INR"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    AUD = "AUD"
    CAD = "CAD"
    SGD = "SGD"
    AED = "AED"


# ==================== Day & Time Enumerations ====================

class DayOfWeek(str, Enum):
    """Day of week enumeration."""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class Month(str, Enum):
    """Month enumeration."""
    JANUARY = "january"
    FEBRUARY = "february"
    MARCH = "march"
    APRIL = "april"
    MAY = "may"
    JUNE = "june"
    JULY = "july"
    AUGUST = "august"
    SEPTEMBER = "september"
    OCTOBER = "october"
    NOVEMBER = "november"
    DECEMBER = "december"


# ==================== Sort & Filter Enumerations ====================

class SortOrder(str, Enum):
    """Sort order enumeration."""
    ASC = "asc"
    DESC = "desc"
    ASCENDING = "ascending"
    DESCENDING = "descending"


class FilterOperator(str, Enum):
    """Filter operator enumeration."""
    EQUALS = "eq"
    NOT_EQUALS = "ne"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    CONTAINS = "contains"
    STARTS_WITH = "startswith"
    ENDS_WITH = "endswith"
    IN = "in"
    NOT_IN = "notin"
    BETWEEN = "between"
    IS_NULL = "isnull"
    IS_NOT_NULL = "isnotnull"


# ==================== Export Enumerations ====================

class ExportFormat(str, Enum):
    """Export format enumeration."""
    CSV = "csv"
    EXCEL = "excel"
    XLSX = "xlsx"
    PDF = "pdf"
    JSON = "json"
    XML = "xml"


class ReportType(str, Enum):
    """Report type enumeration."""
    FINANCIAL = "financial"
    OCCUPANCY = "occupancy"
    ATTENDANCE = "attendance"
    COMPLAINT = "complaint"
    MAINTENANCE = "maintenance"
    PAYMENT = "payment"
    BOOKING = "booking"
    CUSTOM = "custom"


# ==================== Student Enumerations ====================

class StudentStatus(str, Enum):
    """Student status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CHECKED_OUT = "checked_out"
    SUSPENDED = "suspended"
    GRADUATED = "graduated"
    TRANSFERRED = "transferred"
    EXPELLED = "expelled"


class BloodGroup(str, Enum):
    """Blood group enumeration."""
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"


# ==================== Analytics Enumerations ====================

class AnalyticsPeriod(str, Enum):
    """Analytics period enumeration."""
    TODAY = "today"
    YESTERDAY = "yesterday"
    THIS_WEEK = "this_week"
    LAST_WEEK = "last_week"
    THIS_MONTH = "this_month"
    LAST_MONTH = "last_month"
    THIS_QUARTER = "this_quarter"
    LAST_QUARTER = "last_quarter"
    THIS_YEAR = "this_year"
    LAST_YEAR = "last_year"
    CUSTOM = "custom"


class MetricType(str, Enum):
    """Metric type enumeration."""
    COUNT = "count"
    SUM = "sum"
    AVERAGE = "average"
    MIN = "min"
    MAX = "max"
    PERCENTAGE = "percentage"
    RATE = "rate"


# ==================== Communication Enumerations ====================

class CommunicationChannel(str, Enum):
    """Communication channel enumeration."""
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    PUSH_NOTIFICATION = "push_notification"
    IN_APP = "in_app"
    PHONE_CALL = "phone_call"


class MessageStatus(str, Enum):
    """Message status enumeration."""
    DRAFT = "draft"
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    BOUNCED = "bounced"


# ==================== Task Enumerations ====================

class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class TaskPriority(str, Enum):
    """Task priority enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ==================== Vendor Enumerations ====================

class VendorCategory(str, Enum):
    """Vendor category enumeration."""
    PLUMBING = "plumbing"
    ELECTRICAL = "electrical"
    FURNITURE = "furniture"
    CLEANING = "cleaning"
    PEST_CONTROL = "pest_control"
    CATERING = "catering"
    SECURITY = "security"
    INTERNET = "internet"
    LAUNDRY = "laundry"
    GENERAL = "general"


class VendorStatus(str, Enum):
    """Vendor status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLACKLISTED = "blacklisted"
    PENDING_VERIFICATION = "pending_verification"


# ==================== Referral Enumerations ====================

class ReferralStatus(str, Enum):
    """Referral status enumeration."""
    PENDING = "pending"
    REGISTERED = "registered"
    VERIFIED = "verified"
    COMPLETED = "completed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


# ==================== Occupancy Enumerations ====================

class OccupancyStatus(str, Enum):
    """Occupancy status enumeration."""
    VACANT = "vacant"
    OCCUPIED = "occupied"
    PARTIALLY_OCCUPIED = "partially_occupied"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"


# ==================== Environment Enumerations ====================

class Environment(str, Enum):
    """Environment enumeration."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"
    LOCAL = "local"