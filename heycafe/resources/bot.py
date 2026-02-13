"""Bot/utility endpoints: giphy_search, language_detect, language_translate, etc."""

from __future__ import annotations

from heycafe.resources.base import BaseResource


class BotResource(BaseResource):
    """Bot and utility endpoints. Public."""

    def giphy_search(self, query: str, **params: str) -> dict:
        """Search Giphy. query required."""
        return self._client.get("get_bot_giphy_search", params={"query": query, **params})

    def language_detect(self, **params: str) -> dict:
        """Detect language of text."""
        return self._client.get("get_bot_language_detect", params=params)

    def language_translate(self, **params: str) -> dict:
        """Translate text."""
        return self._client.get("get_bot_language_translate", params=params)

    def website_meta(self, **params: str) -> dict:
        """Get website metadata (e.g. Open Graph)."""
        return self._client.get("get_bot_website_meta", params=params)

    def safespace_text(self, **params: str) -> dict:
        """Safespace text check."""
        return self._client.get("get_bot_safespace_text", params=params)
