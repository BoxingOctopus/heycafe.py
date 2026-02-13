"""System endpoints: hello, endpoints, emoji, reactions, etc."""

from __future__ import annotations

from heycafe.resources.base import BaseResource


class SystemResource(BaseResource):
    """System and utility endpoints. No API key required."""

    def hello(self) -> str:
        """Ping the API. Returns 'hello'."""
        return self._client.get("get_system_hello")

    def endpoints(self) -> dict:
        """Get recommended endpoint and list of all endpoints for this session."""
        return self._client.get("get_system_endpoints")

    def emoji_category(self, params: dict | None = None) -> dict:
        """Get emoji categories. Pass optional query params."""
        return self._client.get("get_system_emoji_category", params=params or {})

    def emoji_search(self, query: str, **kwargs: str) -> dict:
        """Search emoji. Requires query."""
        return self._client.get("get_system_emoji_search", params={"query": query, **kwargs})

    def emoji_lookup(self, params: dict | None = None) -> dict:
        """Look up emoji by shortcode or other params."""
        return self._client.get("get_system_emoji_lookup", params=params or {})

    def reactions(self) -> dict:
        """Get available reactions."""
        return self._client.get("get_system_reactions")

    def ip_details(self, params: dict | None = None) -> dict:
        """Get IP details. Pass optional params."""
        return self._client.get("get_system_ip_details", params=params or {})

    def email_details(self, params: dict | None = None) -> dict:
        """Get email details. Pass optional params."""
        return self._client.get("get_system_email_details", params=params or {})
