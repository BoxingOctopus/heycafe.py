"""Exceptions raised by the Hey.Café SDK."""

from __future__ import annotations

from typing import Any, Dict, Optional


class HeyCafeError(Exception):
    """Base exception for all Hey.Café SDK errors."""

    pass


class APIError(HeyCafeError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class AuthenticationError(APIError):
    """Raised when API key is missing or invalid for an endpoint that requires it."""

    pass


class ValidationError(APIError):
    """Raised when request parameters are invalid."""

    pass


class RateLimitError(APIError):
    """Raised when rate limited by the API."""

    pass
