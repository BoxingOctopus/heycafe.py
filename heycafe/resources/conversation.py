"""Conversation endpoints: info, comments, create, edit, publish."""

from __future__ import annotations

from typing import Optional

from heycafe.client import encode_content
from heycafe.resources.base import BaseResource


class ConversationResource(BaseResource):
    """Conversation (post) endpoints."""

    def info(self, query: str) -> dict:
        """Get conversation info by id. Public."""
        return self._client.get("get_conversation_info", params={"query": query})

    def comments(self, query: str, **params: str) -> dict:
        """Get conversation comments. query is conversation id."""
        return self._client.get("get_conversation_comments", params={"query": query, **params})

    def create(
        self,
        cafe: str,
        content: Optional[str] = None,
        content_raw: Optional[str] = None,
        file: Optional[str] = None,
        image_url: Optional[str] = None,
        alt: Optional[str] = None,
        draft: bool = False,
    ) -> dict:
        """
        Create a new conversation in a café.

        Requires API key. Provide either content (base64), content_raw (plain text), or both.
        Optional: file (from post_temp_file), image_url, alt (alt text, base64 or plain), draft.
        """
        data: dict = {"cafe": cafe}
        if content_raw is not None:
            data["content_raw"] = content_raw
        if content is not None:
            data["content"] = content
        elif content_raw is not None:
            data["content"] = encode_content(content_raw)
        if file:
            data["file"] = file
        if image_url:
            data["image_url"] = image_url
        if alt is not None:
            data["alt"] = alt
        if draft:
            data["draft"] = "true"
        return self._client.post("post_conversation_create", data=data, use_api_key=True)

    def edit(self, query: str, **data: str) -> dict:
        """Edit a conversation. Requires API key."""
        return self._client.post("post_conversation_edit", data={"query": query, **data}, use_api_key=True)

    def publish(self, query: str) -> dict:
        """Publish a draft conversation. Requires API key."""
        return self._client.post("post_conversation_publish", data={"query": query}, use_api_key=True)
