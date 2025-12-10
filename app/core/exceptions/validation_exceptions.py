# --- File: app/core/exceptions/validation_exceptions.py ---
"""
Validation and input error exceptions.

This module contains all exceptions related to input validation,
data integrity, and format validation errors.
"""

from typing import Optional, Dict, Any, List, Union
from fastapi import status
from app.core.exceptions.base import BaseValidationException
from app.core.constants import (
    ERROR_VALIDATION_FAILED,
    ERROR_INVALID_INPUT,
    ERROR_DUPLICATE_ENTRY,
    ERROR_INVALID_DATE_RANGE,
    ERROR_REQUIRED_FIELD,
    ERROR_INVALID_FORMAT
)


class ValidationException(BaseValidationException):
    """
    General validation exception.
    
    Raised when input validation fails for any reason.
    """
    
    def __init__(
        self,
        message: str = "Validation failed",
        field: Optional[str] = None,
        value: Optional[Any] = None,
        error_code: str = ERROR_VALIDATION_FAILED,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            field=field,
            value=value,
            error_code=error_code,
            details=details
        )


class InvalidInputException(ValidationException):
    """
    Exception raised when input data is invalid.
    
    This includes wrong data types, invalid formats, or malformed data.
    """
    
    def __init__(
        self,
        message: str = "Invalid input data",
        field: Optional[str] = None,
        value: Optional[Any] = None,
        expected_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        input_details = details or {}
        if expected_type:
            input_details["expected_type"] = expected_type
        
        super().__init__(
            message=message,
            field=field,
            value=value,
            error_code=ERROR_INVALID_INPUT,
            details=input_details
        )


class DataIntegrityException(ValidationException):
    """
    Exception raised when data integrity constraints are violated.
    
    This includes foreign key violations, unique constraints, etc.
    """
    
    def __init__(
        self,
        message: str = "Data integrity violation",
        constraint: Optional[str] = None,
        table: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        integrity_details = details or {}
        if constraint:
            integrity_details["constraint"] = constraint
        if table:
            integrity_details["table"] = table
        
        super().__init__(
            message=message,
            error_code="VAL_007",
            details=integrity_details
        )


class DuplicateEntryException(ValidationException):
    """
    Exception raised when trying to create duplicate entries.
    
    This occurs when unique constraints are violated.
    """
    
    def __init__(
        self,
        message: str = "Duplicate entry",
        field: Optional[str] = None,
        value: Optional[Any] = None,
        existing_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        duplicate_details = details or {}
        if existing_id:
            duplicate_details["existing_id"] = existing_id
        
        super().__init__(
            message=message,
            field=field,
            value=value,
            error_code=ERROR_DUPLICATE_ENTRY,
            details=duplicate_details
        )


class InvalidDateRangeException(ValidationException):
    """
    Exception raised when date ranges are invalid.
    
    This includes end dates before start dates, invalid date formats, etc.
    """
    
    def __init__(
        self,
        message: str = "Invalid date range",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        date_details = details or {}
        if start_date:
            date_details["start_date"] = start_date
        if end_date:
            date_details["end_date"] = end_date
        
        super().__init__(
            message=message,
            error_code=ERROR_INVALID_DATE_RANGE,
            details=date_details
        )


class RequiredFieldException(ValidationException):
    """
    Exception raised when required fields are missing.
    
    This occurs when mandatory fields are not provided in requests.
    """
    
    def __init__(
        self,
        message: str = "Required field missing",
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            field=field,
            error_code=ERROR_REQUIRED_FIELD,
            details=details
        )


class InvalidFormatException(ValidationException):
    """
    Exception raised when data format is invalid.
    
    This includes invalid email formats, phone numbers, URLs, etc.
    """
    
    def __init__(
        self,
        message: str = "Invalid format",
        field: Optional[str] = None,
        value: Optional[Any] = None,
        expected_format: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        format_details = details or {}
        if expected_format:
            format_details["expected_format"] = expected_format
        
        super().__init__(
            message=message,
            field=field,
            value=value,
            error_code=ERROR_INVALID_FORMAT,
            details=format_details
        )


class FileSizeException(ValidationException):
    """
    Exception raised when file size exceeds limits.
    
    This occurs during file upload validation.
    """
    
    def __init__(
        self,
        message: str = "File size exceeds limit",
        file_size: Optional[int] = None,
        max_size: Optional[int] = None,
        filename: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        file_details = details or {}
        if file_size is not None:
            file_details["file_size"] = file_size
        if max_size is not None:
            file_details["max_size"] = max_size
        if filename:
            file_details["filename"] = filename
        
        super().__init__(
            message=message,
            error_code="VAL_008",
            details=file_details
        )


class FileTypeException(ValidationException):
    """
    Exception raised when file type is not allowed.
    
    This occurs when uploaded files have unsupported extensions or MIME types.
    """
    
    def __init__(
        self,
        message: str = "File type not allowed",
        file_type: Optional[str] = None,
        allowed_types: Optional[List[str]] = None,
        filename: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        file_details = details or {}
        if file_type:
            file_details["file_type"] = file_type
        if allowed_types:
            file_details["allowed_types"] = allowed_types
        if filename:
            file_details["filename"] = filename
        
        super().__init__(
            message=message,
            error_code="VAL_009",
            details=file_details
        )


class RangeValidationException(ValidationException):
    """
    Exception raised when numeric values are outside allowed ranges.
    
    This includes age limits, price ranges, quantity limits, etc.
    """
    
    def __init__(
        self,
        message: str = "Value outside allowed range",
        field: Optional[str] = None,
        value: Optional[Union[int, float]] = None,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        range_details = details or {}
        if min_value is not None:
            range_details["min_value"] = min_value
        if max_value is not None:
            range_details["max_value"] = max_value
        
        super().__init__(
            message=message,
            field=field,
            value=value,
            error_code="VAL_010",
            details=range_details
        )


class EmailValidationException(InvalidFormatException):
    """
    Exception raised when email format is invalid.
    
    Specific validation for email addresses.
    """
    
    def __init__(
        self,
        message: str = "Invalid email format",
        email: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            field="email",
            value=email,
            expected_format="valid email address",
            details=details
        )


class PhoneValidationException(InvalidFormatException):
    """
    Exception raised when phone number format is invalid.
    
    Specific validation for phone numbers.
    """
    
    def __init__(
        self,
        message: str = "Invalid phone number format",
        phone: Optional[str] = None,
        country_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        phone_details = details or {}
        if country_code:
            phone_details["country_code"] = country_code
        
        super().__init__(
            message=message