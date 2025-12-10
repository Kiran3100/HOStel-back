"""
Application-wide constants.

This module contains all constant values used throughout the application.
Organized by category for easy reference and maintenance.
"""

from enum import Enum


# ==================== Application Constants ====================
APP_NAME = "Hostel Management System"
APP_VERSION = "1.0.0"
API_PREFIX = "/api/v1"
APP_DESCRIPTION = "Comprehensive hostel management platform"

# ==================== Date/Time Formats ====================
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATETIME_ISO_FORMAT = "%Y-%m-%dT%H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
MONTH_FORMAT = "%Y-%m"
YEAR_FORMAT = "%Y"

# Display formats
DISPLAY_DATE_FORMAT = "%d %b, %Y"  # 01 Jan, 2024
DISPLAY_DATETIME_FORMAT = "%d %b, %Y %I:%M %p"  # 01 Jan, 2024 02:30 PM
DISPLAY_TIME_FORMAT = "%I:%M %p"  # 02:30 PM

# ==================== Pagination Constants ====================
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
MIN_PAGE_SIZE = 1

# ==================== File Upload Constants ====================
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB

# File type categories
FILE_CATEGORY_IMAGE = "image"
FILE_CATEGORY_DOCUMENT = "document"
FILE_CATEGORY_VIDEO = "video"
FILE_CATEGORY_AUDIO = "audio"
FILE_CATEGORY_OTHER = "other"

# Image dimensions
THUMBNAIL_SIZE = (150, 150)
SMALL_SIZE = (300, 300)
MEDIUM_SIZE = (500, 500)
LARGE_SIZE = (1200, 1200)
MAX_IMAGE_DIMENSION = 4000

# Supported formats
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]
DOCUMENT_EXTENSIONS = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".txt"]
VIDEO_EXTENSIONS = [".mp4", ".avi", ".mov", ".wmv", ".flv"]
AUDIO_EXTENSIONS = [".mp3", ".wav", ".ogg", ".m4a"]

# MIME types
IMAGE_MIME_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"]
DOCUMENT_MIME_TYPES = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/csv",
    "text/plain"
]

# ==================== Cache TTL (in seconds) ====================
CACHE_TTL_SHORT = 300  # 5 minutes
CACHE_TTL_MEDIUM = 1800  # 30 minutes
CACHE_TTL_LONG = 3600  # 1 hour
CACHE_TTL_VERY_LONG = 86400  # 24 hours
CACHE_TTL_WEEK = 604800  # 7 days

# Cache keys
CACHE_KEY_USER = "user:{user_id}"
CACHE_KEY_HOSTEL = "hostel:{hostel_id}"
CACHE_KEY_BOOKING = "booking:{booking_id}"
CACHE_KEY_SEARCH = "search:{query}:{filters}"
CACHE_KEY_STATS = "stats:{entity}:{period}"

# ==================== Rate Limiting ====================
RATE_LIMIT_LOGIN = "5/minute"
RATE_LIMIT_REGISTER = "3/minute"
RATE_LIMIT_PASSWORD_RESET = "3/hour"
RATE_LIMIT_API = "60/minute"
RATE_LIMIT_UPLOAD = "10/minute"
RATE_LIMIT_EMAIL = "10/hour"
RATE_LIMIT_SMS = "5/hour"
RATE_LIMIT_SEARCH = "30/minute"

# ==================== Session Constants ====================
SESSION_COOKIE_NAME = "session_id"
SESSION_EXPIRE_SECONDS = 3600  # 1 hour
SESSION_ABSOLUTE_TIMEOUT = 86400  # 24 hours
SESSION_RENEWAL_THRESHOLD = 300  # 5 minutes

# ==================== OTP Constants ====================
OTP_LENGTH = 6
OTP_EXPIRE_MINUTES = 10
OTP_MAX_ATTEMPTS = 3
OTP_RESEND_DELAY_SECONDS = 60
OTP_NUMERIC_ONLY = True

# ==================== Password Constants ====================
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128
PASSWORD_RESET_TOKEN_EXPIRE_HOURS = 24
PASSWORD_RESET_TOKEN_LENGTH = 32

# ==================== Booking Constants ====================
BOOKING_ADVANCE_PERCENTAGE = 20.0
BOOKING_EXPIRY_HOURS = 24
MIN_BOOKING_DURATION_DAYS = 30
MAX_BOOKING_DURATION_DAYS = 365
BOOKING_CONFIRMATION_GRACE_PERIOD_HOURS = 2
BOOKING_CANCELLATION_DEADLINE_HOURS = 48
BOOKING_MODIFICATION_DEADLINE_HOURS = 24

# ==================== Payment Constants ====================
PAYMENT_REMINDER_DAYS_BEFORE = [7, 3, 1]  # Days before due date
PAYMENT_OVERDUE_GRACE_PERIOD_DAYS = 3
LATE_FEE_PERCENTAGE = 5.0
LATE_FEE_MAX_AMOUNT = 1000.0
REFUND_PROCESSING_DAYS = 7
REFUND_CANCELLATION_FEE_PERCENTAGE = 10.0

# Transaction limits
MIN_TRANSACTION_AMOUNT = 1.0
MAX_TRANSACTION_AMOUNT = 1000000.0

# ==================== Approval Thresholds ====================
SUPERVISOR_COMPLAINT_THRESHOLD = 5000.0
SUPERVISOR_MAINTENANCE_THRESHOLD = 10000.0
AUTO_APPROVE_THRESHOLD = 1000.0
ESCALATION_THRESHOLD = 50000.0

# ==================== Email Templates ====================
EMAIL_TEMPLATES_DIR = "app/templates/emails"

# Template names
EMAIL_TEMPLATE_VERIFICATION = "email_verification"
EMAIL_TEMPLATE_PASSWORD_RESET = "password_reset"
EMAIL_TEMPLATE_WELCOME = "welcome"
EMAIL_TEMPLATE_BOOKING_CONFIRMATION = "booking_confirmation"
EMAIL_TEMPLATE_BOOKING_CANCELLATION = "booking_cancellation"
EMAIL_TEMPLATE_PAYMENT_RECEIPT = "payment_receipt"
EMAIL_TEMPLATE_PAYMENT_REMINDER = "payment_reminder"
EMAIL_TEMPLATE_COMPLAINT_UPDATE = "complaint_update"
EMAIL_TEMPLATE_MAINTENANCE_UPDATE = "maintenance_update"
EMAIL_TEMPLATE_NOTICE = "notice"
EMAIL_TEMPLATE_INVOICE = "invoice"

# ==================== Notification Types ====================
NOTIFICATION_EMAIL = "email"
NOTIFICATION_SMS = "sms"
NOTIFICATION_PUSH = "push"
NOTIFICATION_IN_APP = "in_app"
NOTIFICATION_WEBHOOK = "webhook"

# Notification priorities
NOTIFICATION_PRIORITY_LOW = "low"
NOTIFICATION_PRIORITY_MEDIUM = "medium"
NOTIFICATION_PRIORITY_HIGH = "high"
NOTIFICATION_PRIORITY_URGENT = "urgent"

# ==================== Queue Names ====================
QUEUE_DEFAULT = "default"
QUEUE_EMAIL = "email"
QUEUE_SMS = "sms"
QUEUE_NOTIFICATION = "notification"
QUEUE_REPORT = "report"
QUEUE_EXPORT = "export"
QUEUE_IMPORT = "import"
QUEUE_ANALYTICS = "analytics"

# ==================== Task Priorities ====================
PRIORITY_CRITICAL = 0
PRIORITY_HIGH = 1
PRIORITY_MEDIUM = 5
PRIORITY_LOW = 10

# ==================== Search Constants ====================
SEARCH_MIN_QUERY_LENGTH = 2
SEARCH_MAX_QUERY_LENGTH = 100
SEARCH_MAX_RESULTS = 100
SEARCH_FUZZY_DISTANCE = 2
SEARCH_BOOST_EXACT_MATCH = 2.0
SEARCH_BOOST_PARTIAL_MATCH = 1.5

# ==================== Geocoding Constants ====================
DEFAULT_SEARCH_RADIUS_KM = 10
MAX_SEARCH_RADIUS_KM = 50
DEFAULT_LATITUDE = 0.0
DEFAULT_LONGITUDE = 0.0

# ==================== Review Constants ====================
MIN_REVIEW_LENGTH = 10
MAX_REVIEW_LENGTH = 1000
MIN_RATING = 1
MAX_RATING = 5
REVIEW_VERIFICATION_DAYS = 7  # Days after checkout to submit review

# ==================== Complaint Constants ====================
COMPLAINT_AUTO_ESCALATE_DAYS = 3
COMPLAINT_AUTO_CLOSE_DAYS = 30
COMPLAINT_RESOLUTION_TARGET_DAYS = 7
MAX_COMPLAINT_ATTACHMENTS = 5

# ==================== Maintenance Constants ====================
PREVENTIVE_MAINTENANCE_ADVANCE_DAYS = 7
MAINTENANCE_WARRANTY_PERIOD_DAYS = 90
MAX_MAINTENANCE_COST = 100000.0

# ==================== Attendance Constants ====================
LATE_ARRIVAL_THRESHOLD_MINUTES = 30
ABSENCE_NOTIFICATION_DELAY_HOURS = 2
MIN_ATTENDANCE_PERCENTAGE = 75.0
ATTENDANCE_MARKING_WINDOW_HOURS = 24

# ==================== Leave Constants ====================
MAX_LEAVE_DAYS_PER_REQUEST = 30
LEAVE_APPLICATION_ADVANCE_DAYS = 2
ANNUAL_LEAVE_QUOTA_DAYS = 15

# ==================== Report Retention ====================
REPORT_RETENTION_DAYS = 90
AUDIT_LOG_RETENTION_DAYS = 365
SESSION_CLEANUP_DAYS = 30
NOTIFICATION_RETENTION_DAYS = 90
TEMP_FILE_RETENTION_HOURS = 24

# ==================== HTTP Status Codes ====================
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_202_ACCEPTED = 202
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_409_CONFLICT = 409
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_429_TOO_MANY_REQUESTS = 429
HTTP_500_INTERNAL_SERVER_ERROR = 500
HTTP_502_BAD_GATEWAY = 502
HTTP_503_SERVICE_UNAVAILABLE = 503

# ==================== Error Codes ====================
# Authentication errors
ERROR_AUTHENTICATION_FAILED = "AUTH_001"
ERROR_INVALID_TOKEN = "AUTH_002"
ERROR_TOKEN_EXPIRED = "AUTH_003"
ERROR_PERMISSION_DENIED = "AUTH_004"
ERROR_INVALID_CREDENTIALS = "AUTH_005"
ERROR_EMAIL_NOT_VERIFIED = "AUTH_006"
ERROR_ACCOUNT_INACTIVE = "AUTH_007"
ERROR_ACCOUNT_SUSPENDED = "AUTH_008"

# Validation errors
ERROR_VALIDATION_FAILED = "VAL_001"
ERROR_INVALID_INPUT = "VAL_002"
ERROR_DUPLICATE_ENTRY = "VAL_003"
ERROR_INVALID_DATE_RANGE = "VAL_004"
ERROR_REQUIRED_FIELD = "VAL_005"
ERROR_INVALID_FORMAT = "VAL_006"

# Resource errors
ERROR_RESOURCE_NOT_FOUND = "RES_001"
ERROR_HOSTEL_NOT_FOUND = "RES_002"
ERROR_BOOKING_NOT_FOUND = "RES_003"
ERROR_STUDENT_NOT_FOUND = "RES_004"
ERROR_PAYMENT_NOT_FOUND = "RES_005"

# Business logic errors
ERROR_BOOKING_UNAVAILABLE = "BIZ_001"
ERROR_PAYMENT_FAILED = "BIZ_002"
ERROR_INSUFFICIENT_BALANCE = "BIZ_003"
ERROR_BOOKING_EXPIRED = "BIZ_004"
ERROR_ALREADY_BOOKED = "BIZ_005"
ERROR_CAPACITY_EXCEEDED = "BIZ_006"

# ==================== Success Messages ====================
MSG_SUCCESS = "Operation completed successfully"
MSG_CREATED = "Resource created successfully"
MSG_UPDATED = "Resource updated successfully"
MSG_DELETED = "Resource deleted successfully"
MSG_UPLOADED = "File uploaded successfully"

# User messages
MSG_LOGIN_SUCCESS = "Login successful"
MSG_LOGOUT_SUCCESS = "Logout successful"
MSG_REGISTRATION_SUCCESS = "Registration successful. Please verify your email."
MSG_PASSWORD_RESET = "Password reset link sent to your email"
MSG_PASSWORD_CHANGED = "Password changed successfully"
MSG_EMAIL_VERIFIED = "Email verified successfully"
MSG_PROFILE_UPDATED = "Profile updated successfully"

# Booking messages
MSG_BOOKING_CREATED = "Booking created successfully"
MSG_BOOKING_CONFIRMED = "Booking confirmed successfully"
MSG_BOOKING_CANCELLED = "Booking cancelled successfully"
MSG_BOOKING_CHECKED_IN = "Check-in completed successfully"
MSG_BOOKING_CHECKED_OUT = "Check-out completed successfully"

# Payment messages
MSG_PAYMENT_SUCCESS = "Payment completed successfully"
MSG_PAYMENT_INITIATED = "Payment initiated"
MSG_PAYMENT_FAILED = "Payment failed. Please try again."
MSG_REFUND_INITIATED = "Refund request initiated"
MSG_REFUND_COMPLETED = "Refund completed successfully"

# Complaint messages
MSG_COMPLAINT_FILED = "Complaint filed successfully"
MSG_COMPLAINT_UPDATED = "Complaint status updated"
MSG_COMPLAINT_RESOLVED = "Complaint resolved"

# Maintenance messages
MSG_MAINTENANCE_REQUESTED = "Maintenance request created"
MSG_MAINTENANCE_ASSIGNED = "Maintenance request assigned"
MSG_MAINTENANCE_COMPLETED = "Maintenance completed"

# ==================== Regex Patterns ====================
REGEX_EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
REGEX_PHONE = r"^\+?[1-9]\d{1,14}$"
REGEX_PHONE_INDIA = r"^[6-9]\d{9}$"
REGEX_UUID = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
REGEX_ALPHANUMERIC = r"^[a-zA-Z0-9]+$"
REGEX_SLUG = r"^[a-z0-9-]+$"
REGEX_URL = r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"
REGEX_IPV4 = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
REGEX_PINCODE_INDIA = r"^[1-9][0-9]{5}$"

# ==================== Currency Formats ====================
CURRENCY_SYMBOLS = {
    "INR": "₹",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
}

CURRENCY_NAMES = {
    "INR": "Indian Rupee",
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
}

# ==================== Time Zones ====================
DEFAULT_TIMEZONE = "Asia/Kolkata"
SUPPORTED_TIMEZONES = [
    "Asia/Kolkata",
    "UTC",
    "America/New_York",
    "Europe/London",
]

# ==================== Export Formats ====================
EXPORT_FORMAT_CSV = "csv"
EXPORT_FORMAT_EXCEL = "excel"
EXPORT_FORMAT_PDF = "pdf"
EXPORT_FORMAT_JSON = "json"

# ==================== Hostel Amenities ====================
AMENITIES_BASIC = [
    "wifi",
    "hot_water",
    "laundry",
    "power_backup",
]

AMENITIES_PREMIUM = [
    "ac",
    "tv",
    "refrigerator",
    "microwave",
    "gym",
    "swimming_pool",
]

AMENITIES_SECURITY = [
    "cctv",
    "security_guard",
    "biometric",
    "fire_safety",
]

# ==================== Room Amenities ====================
ROOM_AMENITIES_BASIC = [
    "bed",
    "mattress",
    "wardrobe",
    "study_table",
    "chair",
]

ROOM_AMENITIES_ADDITIONAL = [
    "ac",
    "fan",
    "window",
    "attached_bathroom",
    "balcony",
]

# ==================== Default Values ====================
DEFAULT_PAGE_SIZE = 20
DEFAULT_LANGUAGE = "en"
DEFAULT_COUNTRY_CODE = "+91"
DEFAULT_CURRENCY = "INR"

# ==================== Limits ====================
MAX_PROFILE_PICTURE_SIZE = 2 * 1024 * 1024  # 2MB
MAX_HOSTEL_PHOTOS = 20
MAX_COMPLAINT_PHOTOS = 5
MAX_REVIEW_PHOTOS = 10
MAX_CONCURRENT_BOOKINGS_PER_USER = 5
MAX_COMPLAINTS_PER_DAY = 10

# ==================== Scoring ====================
HOSTEL_RANKING_WEIGHTS = {
    "rating": 0.4,
    "occupancy": 0.2,
    "reviews_count": 0.2,
    "price": 0.1,
    "location": 0.1,
}

# ==================== Feature Flags ====================
FEATURE_ONLINE_PAYMENT = True
FEATURE_SMS_NOTIFICATIONS = False
FEATURE_PUSH_NOTIFICATIONS = False
FEATURE_ANALYTICS_DASHBOARD = True
FEATURE_MULTI_LANGUAGE = False
FEATURE_DARK_MODE = True