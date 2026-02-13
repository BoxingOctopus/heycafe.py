"""Stats endpoints: accounts, cafes, conversations, comments, etc."""

from __future__ import annotations

from heycafe.resources.base import BaseResource


class StatsResource(BaseResource):
    """Platform statistics. All public."""

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        return self._client.get(endpoint, params=params or {})

    def accounts(self) -> dict:
        return self._get("get_stats_accounts")

    def accounts_pro(self) -> dict:
        return self._get("get_stats_accounts_pro")

    def accounts_verified(self) -> dict:
        return self._get("get_stats_accounts_verified")

    def accounts_today(self) -> dict:
        return self._get("get_stats_accounts_today")

    def accounts_week(self) -> dict:
        return self._get("get_stats_accounts_week")

    def accounts_month(self) -> dict:
        return self._get("get_stats_accounts_month")

    def accounts_type_person(self) -> dict:
        return self._get("get_stats_accounts_type_person")

    def accounts_type_business(self) -> dict:
        return self._get("get_stats_accounts_type_business")

    def accounts_type_robot(self) -> dict:
        return self._get("get_stats_accounts_type_robot")

    def accounts_type_creator(self) -> dict:
        return self._get("get_stats_accounts_type_creator")

    def accounts_type_news(self) -> dict:
        return self._get("get_stats_accounts_type_news")

    def accounts_status_active(self) -> dict:
        return self._get("get_stats_accounts_status_active")

    def accounts_status_banned(self) -> dict:
        return self._get("get_stats_accounts_status_banned")

    def accounts_status_deleted(self) -> dict:
        return self._get("get_stats_accounts_status_deleted")

    def accounts_follows(self) -> dict:
        return self._get("get_stats_accounts_follows")

    def accounts_notifications(self) -> dict:
        return self._get("get_stats_accounts_notifications")

    def accounts_subs(self) -> dict:
        return self._get("get_stats_accounts_subs")

    def accounts_online(self) -> dict:
        return self._get("get_stats_accounts_online")

    def accounts_online_today(self) -> dict:
        return self._get("get_stats_accounts_online_today")

    def accounts_online_week(self) -> dict:
        return self._get("get_stats_accounts_online_week")

    def accounts_online_month(self) -> dict:
        return self._get("get_stats_accounts_online_month")

    def accounts_tags(self) -> dict:
        return self._get("get_stats_accounts_tags")

    def chats(self) -> dict:
        return self._get("get_stats_chats")

    def chats_messages(self) -> dict:
        return self._get("get_stats_chats_messages")

    def chats_messages_today(self) -> dict:
        return self._get("get_stats_chats_messages_today")

    def chats_messages_week(self) -> dict:
        return self._get("get_stats_chats_messages_week")

    def chats_messages_month(self) -> dict:
        return self._get("get_stats_chats_messages_month")

    def cafes(self) -> dict:
        return self._get("get_stats_cafes")

    def cafes_members(self) -> dict:
        return self._get("get_stats_cafes_members")

    def cafes_tags(self) -> dict:
        return self._get("get_stats_cafes_tags")

    def cafes_conversations(self) -> dict:
        return self._get("get_stats_cafes_conversations")

    def conversations(self) -> dict:
        return self._get("get_stats_conversations")

    def conversations_tagged(self) -> dict:
        return self._get("get_stats_conversations_tagged")

    def conversations_reactions(self) -> dict:
        return self._get("get_stats_conversations_reactions")

    def conversations_today(self) -> dict:
        return self._get("get_stats_conversations_today")

    def conversations_week(self) -> dict:
        return self._get("get_stats_conversations_week")

    def conversations_month(self) -> dict:
        return self._get("get_stats_conversations_month")

    def comments(self) -> dict:
        return self._get("get_stats_comments")

    def comments_reactions(self) -> dict:
        return self._get("get_stats_comments_reactions")

    def comments_today(self) -> dict:
        return self._get("get_stats_comments_today")

    def comments_week(self) -> dict:
        return self._get("get_stats_comments_week")

    def comments_month(self) -> dict:
        return self._get("get_stats_comments_month")
