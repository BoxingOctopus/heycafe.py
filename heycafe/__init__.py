"""
Hey.Café Python SDK

A Python client for the Hey.Café social media platform REST API.
Documentation: https://endpoint.hey.cafe
"""

from heycafe.client import HeyCafeClient, encode_content
from heycafe.exceptions import (
    APIError,
    AuthenticationError,
    HeyCafeError,
    RateLimitError,
    ValidationError,
)
from heycafe.hey_cafe import HeyCafe
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

__version__ = "0.1.0"

__all__ = [
    "HeyCafe",
    "HeyCafeClient",
    "encode_content",
    "HeyCafeError",
    "APIError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
    "SystemResource",
    "AccountResource",
    "CafeResource",
    "ConversationResource",
    "ChatResource",
    "CommentResource",
    "ExploreResource",
    "FeedResource",
    "SearchResource",
    "StatsResource",
    "BotResource",
    "TempResource",
]
