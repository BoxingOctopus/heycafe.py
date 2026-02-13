"""Cafe endpoints: info, conversations, members, create, join, etc."""

from __future__ import annotations

from heycafe.resources.base import BaseResource


class CafeResource(BaseResource):
    """Café (community) endpoints."""

    def info(self, query: str) -> dict:
        """Get café info by alias or id. Public."""
        return self._client.get("get_cafe_info", params={"query": query})

    def conversations(self, query: str, **params: str) -> dict:
        """Get café conversations. query is café alias or id."""
        return self._client.get("get_cafe_conversations", params={"query": query, **params})

    def members(self, query: str, **params: str) -> dict:
        """Get café members. query is café alias or id."""
        return self._client.get("get_cafe_members", params={"query": query, **params})

    def create(self, **data: str) -> dict:
        """Create a café. Requires API key."""
        return self._client.post("post_cafe_create", data=data, use_api_key=True)

    def delete(self, query: str) -> dict:
        """Delete a café. Requires API key."""
        return self._client.post("post_cafe_delete", data={"query": query}, use_api_key=True)

    def join(self, query: str) -> dict:
        """Join a café. Requires API key."""
        return self._client.post("post_cafe_join", data={"query": query}, use_api_key=True)

    def favourite(self, query: str) -> dict:
        """Favourite a café. Requires API key."""
        return self._client.post("post_cafe_favourite", data={"query": query}, use_api_key=True)

    def unfavourite(self, query: str) -> dict:
        """Unfavourite a café. Requires API key."""
        return self._client.post("post_cafe_unfavourite", data={"query": query}, use_api_key=True)

    def update_notifications(self, **data: str) -> dict:
        """Update café notification settings. Requires API key."""
        return self._client.post("post_cafe_update_notifications", data=data, use_api_key=True)

    def update_welcome(self, **data: str) -> dict:
        """Update café welcome message. Requires API key."""
        return self._client.post("post_cafe_update_welcome", data=data, use_api_key=True)

    def update_rules(self, **data: str) -> dict:
        """Update café rules. Requires API key."""
        return self._client.post("post_cafe_update_rules", data=data, use_api_key=True)

    def update_website(self, **data: str) -> dict:
        """Update café website. Requires API key."""
        return self._client.post("post_cafe_update_website", data=data, use_api_key=True)
