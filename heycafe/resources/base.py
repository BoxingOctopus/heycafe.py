"""Base class for API resources."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from heycafe.client import HeyCafeClient


class BaseResource:
    """Base class for resource modules that use the low-level client."""

    def __init__(self, client: HeyCafeClient):
        self._client = client
