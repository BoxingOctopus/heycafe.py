"""Comment endpoints."""

from __future__ import annotations

from heycafe.resources.base import BaseResource


class CommentResource(BaseResource):
    """Comment endpoints."""

    def info(self, query: str) -> dict:
        """Get comment info by id. Public."""
        return self._client.get("get_comment_info", params={"query": query})
