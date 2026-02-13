"""Search endpoints: accounts, cafes, conversations."""

from __future__ import annotations

from heycafe.resources.base import BaseResource


class SearchResource(BaseResource):
    """Search endpoints. Public."""

    def accounts(self, query: str, **params: str) -> dict:
        """Search accounts."""
        return self._client.get("get_search_accounts", params={"query": query, **params})

    def cafes(self, query: str, **params: str) -> dict:
        """Search cafés."""
        return self._client.get("get_search_cafes", params={"query": query, **params})

    def conversations(self, query: str, **params: str) -> dict:
        """Search conversations."""
        return self._client.get("get_search_conversations", params={"query": query, **params})
