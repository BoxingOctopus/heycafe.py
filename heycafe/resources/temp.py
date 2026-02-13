"""Temp endpoints: file upload, preview."""

from __future__ import annotations

from heycafe.resources.base import BaseResource


class TempResource(BaseResource):
    """Temporary file and preview. post_temp_file typically requires API key."""

    def file(self, **data: str) -> dict:
        """Upload a temp file. Returns file id for post_conversation_create. Requires API key."""
        return self._client.post("post_temp_file", data=data, use_api_key=True)

    def preview(self, **data: str) -> dict:
        """Create a preview. Requires API key."""
        return self._client.post("post_temp_preview", data=data, use_api_key=True)
