# app/utils/string_utils.py
from __future__ import annotations

import re
import secrets
import string
from typing import Iterable


_slug_pattern = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    """
    Simple slugify implementation:
    - Lowercase
    - Replace non-alphanumerics with '-'
    - Strip leading/trailing '-'
    """
    value = value.lower()
    value = _slug_pattern.sub("-", value)
    return value.strip("-")


def generate_token(length: int = 32) -> str:
    """Generate a random URL-safe token."""
    return secrets.token_urlsafe(length)


def random_string(
    length: int = 12,
    *,
    alphabet: str | None = None,
) -> str:
    """
    Generate a random string of given length from the specified alphabet.
    Default alphabet: ascii_letters + digits.
    """
    if alphabet is None:
        alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def normalize_whitespace(value: str) -> str:
    """Collapse multiple whitespace characters into single spaces and strip."""
    return " ".join(value.split())


def truncate(value: str, max_length: int, suffix: str = "…") -> str:
    """Truncate a string to max_length characters, including suffix."""
    if len(value) <= max_length:
        return value
    if max_length <= len(suffix):
        return suffix[:max_length]
    return value[: max_length - len(suffix)] + suffix