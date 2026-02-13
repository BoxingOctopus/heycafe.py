"""Feed endpoints: conversations, tags."""

from __future__ import annotations

from heycafe.resources.base import BaseResource


class FeedResource(BaseResource):
    """Feed endpoints. get_feed_conversations requires API key for personalized feed."""

    def conversations(
        self,
        start: int | None = None,
        count: int | None = None,
        rule: str | None = None,
        cafe: str | None = None,
        account: str | None = None,
    ) -> dict:
        """
        Get feed conversations. Requires API key for personalized feed.

        :param start: Offset to start at
        :param count: Number of items (default 20)
        :param rule: all, notme, others, account, cafe, tag, clean
        :param cafe: Limit to this café
        :param account: Limit to this account
        """
        params: dict = {}
        if start is not None:
            params["start"] = start
        if count is not None:
            params["count"] = count
        if rule:
            params["rule"] = rule
        if cafe:
            params["cafe"] = cafe
        if account:
            params["account"] = account
        return self._client.get("get_feed_conversations", params=params, use_api_key=True)

    def tags(self, **params: str) -> dict:
        """Get feed tags. Requires API key."""
        return self._client.get("get_feed_tags", params=params, use_api_key=True)
