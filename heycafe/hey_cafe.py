"""
High-level Hey.Café API client.

Use this as the main entry point: instantiate HeyCafe with optional api_key,
then use .system, .account, .cafe, etc. for typed access to endpoints.
"""

from __future__ import annotations

from heycafe.client import HeyCafeClient
from heycafe.resources import (
    AccountResource,
    BotResource,
    CafeResource,
    ChatResource,
    CommentResource,
    ConversationResource,
    ExploreResource,
    FeedResource,
    SearchResource,
    StatsResource,
    SystemResource,
    TempResource,
)


class HeyCafe:
    """
    High-level client for the Hey.Café API.

    Example:
        client = HeyCafe(api_key="your-key")
        info = client.account.info("hey")
        client.system.hello()
        client.cafe.info("python")
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        session_token: str | None = None,
        **client_kwargs,
    ):
        """
        :param api_key: Account API key for authenticated endpoints
        :param base_url: Override API base URL (default: https://endpoint.hey.cafe)
        :param session_token: Optional session token (e.g. from browser login) for
            endpoints that require a session (feed, notifications)
        :param client_kwargs: Additional arguments for HeyCafeClient (timeout, session, etc.)
        """
        client_kwargs["api_key"] = api_key
        client_kwargs["session_token"] = session_token
        if base_url is not None:
            client_kwargs["base_url"] = base_url
        self._client = HeyCafeClient(**client_kwargs)

    @property
    def client(self) -> HeyCafeClient:
        """Low-level client for raw request/get/post calls."""
        return self._client

    @property
    def system(self) -> SystemResource:
        """System: hello, endpoints, emoji, reactions."""
        return SystemResource(self._client)

    @property
    def account(self) -> AccountResource:
        """Account: info, cafes, followers, follow, etc."""
        return AccountResource(self._client)

    @property
    def cafe(self) -> CafeResource:
        """Café: info, conversations, members, join, etc."""
        return CafeResource(self._client)

    @property
    def conversation(self) -> ConversationResource:
        """Conversation: info, comments, create, edit, publish."""
        return ConversationResource(self._client)

    @property
    def comment(self) -> CommentResource:
        """Comment: info."""
        return CommentResource(self._client)

    @property
    def chat(self) -> ChatResource:
        """Chat: list, info, messages, create, message_create, etc."""
        return ChatResource(self._client)

    @property
    def explore(self) -> ExploreResource:
        """Explore: accounts, cafes, conversations, hot_conversations."""
        return ExploreResource(self._client)

    @property
    def feed(self) -> FeedResource:
        """Feed: conversations, tags."""
        return FeedResource(self._client)

    @property
    def search(self) -> SearchResource:
        """Search: accounts, cafes, conversations."""
        return SearchResource(self._client)

    @property
    def stats(self) -> StatsResource:
        """Stats: platform statistics."""
        return StatsResource(self._client)

    @property
    def bot(self) -> BotResource:
        """Bot: giphy_search, language_detect, website_meta, etc."""
        return BotResource(self._client)

    @property
    def temp(self) -> TempResource:
        """Temp: file upload, preview."""
        return TempResource(self._client)
