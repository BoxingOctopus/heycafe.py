"""Chat endpoints: list, info, messages, create, message_create, etc."""

from __future__ import annotations

from heycafe.resources.base import BaseResource


class ChatResource(BaseResource):
    """Direct chat endpoints. Most require API key."""

    def account(self, **params: str) -> dict:
        """Get chat account info. Requires API key."""
        return self._client.get("get_chat_account", params=params, use_api_key=True)

    def info(self, query: str, **params: str) -> dict:
        """Get chat info. Requires API key."""
        return self._client.get(
            "get_chat_info", params={"query": query, **params}, use_api_key=True
        )

    def list(self, **params: str) -> dict:
        """List chats. Requires API key."""
        return self._client.get("get_chat_list", params=params, use_api_key=True)

    def messages(self, query: str, **params: str) -> dict:
        """Get chat messages. Requires API key."""
        return self._client.get(
            "get_chat_messages",
            params={"query": query, **params},
            use_api_key=True,
        )

    def accept(self, query: str) -> dict:
        """Accept a chat invite. Requires API key."""
        return self._client.post("post_chat_accept", data={"query": query}, use_api_key=True)

    def create(self, **data: str) -> dict:
        """Create a chat. Requires API key."""
        return self._client.post("post_chat_create", data=data, use_api_key=True)

    def invite(self, query: str, **data: str) -> dict:
        """Invite to chat. Requires API key."""
        return self._client.post(
            "post_chat_invite", data={"query": query, **data}, use_api_key=True
        )

    def leave(self, query: str) -> dict:
        """Leave a chat. Requires API key."""
        return self._client.post("post_chat_leave", data={"query": query}, use_api_key=True)

    def message_create(self, query: str, **data: str) -> dict:
        """Send a message in a chat. Requires API key."""
        return self._client.post(
            "post_chat_message_create",
            data={"query": query, **data},
            use_api_key=True,
        )

    def update_description(self, query: str, **data: str) -> dict:
        """Update chat description. Requires API key."""
        return self._client.post(
            "post_chat_update_description",
            data={"query": query, **data},
            use_api_key=True,
        )

    def update_emoji(self, query: str, **data: str) -> dict:
        """Update chat emoji. Requires API key."""
        return self._client.post(
            "post_chat_update_emoji",
            data={"query": query, **data},
            use_api_key=True,
        )

    def update_name(self, query: str, **data: str) -> dict:
        """Update chat name. Requires API key."""
        return self._client.post(
            "post_chat_update_name", data={"query": query, **data}, use_api_key=True
        )
