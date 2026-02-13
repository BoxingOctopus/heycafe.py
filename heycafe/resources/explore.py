"""Explore endpoints: accounts, cafes, conversations, comments, hot_conversations."""

from __future__ import annotations

from heycafe.resources.base import BaseResource


class ExploreResource(BaseResource):
    """Explore/discovery endpoints. Public."""

    def accounts(self, **params: str) -> dict:
        """Explore accounts."""
        return self._client.get("get_explore_accounts", params=params)

    def cafes(self, **params: str) -> dict:
        """Explore cafés."""
        return self._client.get("get_explore_cafes", params=params)

    def conversations(self, **params: str) -> dict:
        """Explore conversations."""
        return self._client.get("get_explore_conversations", params=params)

    def comments(self, **params: str) -> dict:
        """Explore comments."""
        return self._client.get("get_explore_comments", params=params)

    def hot_conversations(self, **params: str) -> dict:
        """Get hot/trending conversations."""
        return self._client.get("get_explore_hot_conversations", params=params)
