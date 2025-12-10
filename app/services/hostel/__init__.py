# app/services/hostel/__init__.py
"""
Hostel-related services.

- HostelService: core Hostel CRUD, visibility and status updates.
- (Admin views, comparison, analytics can be added in separate modules.)
"""

from .hostel_service import HostelService

__all__ = [
    "HostelService",
]