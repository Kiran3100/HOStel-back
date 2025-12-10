# app/services/common/__init__.py
"""
Shared service-layer infrastructure.

- UnitOfWork: transaction boundary & repository factory
- security: password hashing and JWT helpers
- permissions: generic RBAC helpers
- mapping: model <-> schema utilities
- pagination: helpers to build PaginatedResponse objects
"""

from .unit_of_work import UnitOfWork
from . import security
from . import permissions
from . import mapping
from . import pagination

__all__ = [
    "UnitOfWork",
    "security",
    "permissions",
    "mapping",
    "pagination",
]