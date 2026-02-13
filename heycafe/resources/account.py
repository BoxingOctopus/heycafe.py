"""Account endpoints: info, cafes, followers, notifications, follow, etc."""

from __future__ import annotations

from heycafe.resources.base import BaseResource


class AccountResource(BaseResource):
    """
    Account-related endpoints.

    Endpoints that perform actions on behalf of an account (e.g. follow, feed)
    require an API key. Read-only public endpoints (e.g. get_account_info by alias)
    do not.
    """

    def info(self, query: str) -> dict:
        """Get account info by alias or id. Public."""
        return self._client.get("get_account_info", params={"query": query})

    def cafes(self, **params: str) -> dict:
        """Get cafes for the account. Requires API key."""
        return self._client.get("get_account_cafes", params=params, use_api_key=True)

    def conversations(self, **params: str) -> dict:
        """Get account conversations. Requires API key if filtering by account."""
        return self._client.get("get_account_conversations", params=params, use_api_key=True)

    def followers(self, **params: str) -> dict:
        """Get account followers. Requires API key for authenticated account."""
        return self._client.get("get_account_followers", params=params, use_api_key=True)

    def following(self, **params: str) -> dict:
        """Get accounts that the account follows. Requires API key."""
        return self._client.get("get_account_following", params=params, use_api_key=True)

    def friends(self, **params: str) -> dict:
        """Get account friends. Requires API key."""
        return self._client.get("get_account_friends", params=params, use_api_key=True)

    def key(self, **params: str) -> dict:
        """Get account API key info. Requires API key."""
        return self._client.get("get_account_key", params=params, use_api_key=True)

    def mutes(self, **params: str) -> dict:
        """Get account mutes. Requires API key."""
        return self._client.get("get_account_mutes", params=params, use_api_key=True)

    def notifications(self, **params: str) -> dict:
        """Get account notifications. Requires API key."""
        return self._client.get("get_account_notifications", params=params, use_api_key=True)

    def referrals(self, **params: str) -> dict:
        """Get account referrals. Requires API key."""
        return self._client.get("get_account_referrals", params=params, use_api_key=True)

    def reports(self, **params: str) -> dict:
        """Get account reports. Requires API key."""
        return self._client.get("get_account_reports", params=params, use_api_key=True)

    def rssimport_preview(self, **params: str) -> dict:
        """Preview RSS import. Requires API key."""
        return self._client.get("get_account_rssimport_preview", params=params, use_api_key=True)

    # Post Account
    def follow(self, query: str) -> dict:
        """Follow an account. Requires API key."""
        return self._client.post("post_account_follow", data={"query": query}, use_api_key=True)

    def unfollow(self, query: str) -> dict:
        """Unfollow an account. Requires API key."""
        return self._client.post("post_account_unfollow", data={"query": query}, use_api_key=True)

    def subscribe(self, query: str) -> dict:
        """Subscribe to an account. Requires API key."""
        return self._client.post("post_account_subscribe", data={"query": query}, use_api_key=True)

    def unsubscribe(self, query: str) -> dict:
        """Unsubscribe from an account. Requires API key."""
        return self._client.post(
            "post_account_unsubscribe", data={"query": query}, use_api_key=True
        )

    def update_ghost_cafes(self, **data: str) -> dict:
        """Update ghost cafes preference. Requires API key."""
        return self._client.post("post_account_update_ghost_cafes", data=data, use_api_key=True)

    def update_ghost_explore(self, **data: str) -> dict:
        """Update ghost explore preference. Requires API key."""
        return self._client.post("post_account_update_ghost_explore", data=data, use_api_key=True)

    def update_ghost_followers(self, **data: str) -> dict:
        """Update ghost followers preference. Requires API key."""
        return self._client.post("post_account_update_ghost_followers", data=data, use_api_key=True)

    def update_ghost_following(self, **data: str) -> dict:
        """Update ghost following preference. Requires API key."""
        return self._client.post("post_account_update_ghost_following", data=data, use_api_key=True)

    def update_ghost_online(self, **data: str) -> dict:
        """Update ghost online preference. Requires API key."""
        return self._client.post("post_account_update_ghost_online", data=data, use_api_key=True)

    def update_public_view(self, **data: str) -> dict:
        """Update public view preference. Requires API key."""
        return self._client.post("post_account_update_public_view", data=data, use_api_key=True)

    def update_public_react(self, **data: str) -> dict:
        """Update public react preference. Requires API key."""
        return self._client.post("post_account_update_public_react", data=data, use_api_key=True)

    def update_public_comment(self, **data: str) -> dict:
        """Update public comment preference. Requires API key."""
        return self._client.post("post_account_update_public_comment", data=data, use_api_key=True)

    def notification_seen(self, **data: str) -> dict:
        """Mark notification(s) as seen. Requires API key."""
        return self._client.post("post_account_notification_seen", data=data, use_api_key=True)
