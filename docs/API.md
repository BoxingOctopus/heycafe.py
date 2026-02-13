# Hey.Café Python SDK – API reference

This document summarizes the SDK surface. For full endpoint details (parameters, response shapes, which require an API key), see the official docs: **[https://endpoint.hey.cafe](https://endpoint.hey.cafe)**.

## High-level client: `HeyCafe`

```python
from heycafe import HeyCafe

client = HeyCafe(api_key=None, session_token=None)
```

- **api_key** – For endpoints that accept an API key (Bearer or `query`).
- **session_token** – Optional. For endpoints that require a session (e.g. feed conversations, account notifications), pass a session token (e.g. from a browser login cookie). When set, it is sent as the `query` parameter on session-capable requests.

### Attributes (resource groups)

- **client** – Low-level `HeyCafeClient` for raw `get(endpoint, params)` / `post(endpoint, data)`
- **system** – System: `hello()`, `endpoints()`, `emoji_category()`, `emoji_search()`, `emoji_lookup()`, `reactions()`, `ip_details()`, `email_details()`
- **account** – Account: `info(query)`, `cafes()`, `conversations()`, `followers()`, `following()`, `friends()`, `key()`, `mutes()`, `notifications()`, `referrals()`, `reports()`, `rssimport_preview()`, and post actions: `follow()`, `unfollow()`, `subscribe()`, `unsubscribe()`, `update_ghost_*`, `update_public_*`, `notification_seen()`
- **cafe** – Café: `info(query)`, `conversations()`, `members()`, `create()`, `delete()`, `join()`, `favourite()`, `unfavourite()`, `update_notifications()`, `update_welcome()`, `update_rules()`, `update_website()`
- **conversation** – Conversation: `info(query)`, `comments()`, `create()`, `edit()`, `publish()`
- **comment** – Comment: `info(query)`
- **chat** – Chat: `account()`, `info()`, `list()`, `messages()`, `accept()`, `create()`, `invite()`, `leave()`, `message_create()`, `update_description()`, `update_emoji()`, `update_name()`
- **explore** – Explore: `accounts()`, `cafes()`, `conversations()`, `comments()`, `hot_conversations()`
- **feed** – Feed: `conversations()`, `tags()`
- **search** – Search: `accounts()`, `cafes()`, `conversations()`
- **stats** – Stats: `accounts()`, `accounts_pro()`, `conversations()`, `comments()`, and many other `get_stats_*` helpers
- **bot** – Bot: `giphy_search()`, `language_detect()`, `language_translate()`, `website_meta()`, `safespace_text()`
- **temp** – Temp: `file()`, `preview()`

Methods that require an API key or session will raise `AuthenticationError` if neither `api_key` nor `session_token` is set (for those endpoints that accept either).

## Low-level client: `HeyCafeClient`

```python
from heycafe import HeyCafeClient

client = HeyCafeClient(
    base_url="https://endpoint.hey.cafe",
    api_key=None,
    session_token=None,
    error_boolean=True,
    error_no_http=False,
    timeout=30.0,
)
```

- **session_token** – Optional. Sent as `query` on requests that use `use_session=True` (e.g. feed, notifications).
- **get(endpoint, params=None, use_api_key=False, use_session=False)** – GET request; returns `response_data` or full body.
- **post(endpoint, params=None, data=None, use_api_key=False)** – POST request; returns `response_data` or full body.
- **request(endpoint, method="GET", params=None, data=None, use_api_key=False, use_session=False)** – Generic request.

Endpoint names match the docs (e.g. `get_system_hello`, `get_account_info`, `post_conversation_create`).

## Helpers

- **encode_content(text: str) -> str** – Base64-encode text for endpoints that require encoded content.

## Exceptions

- **HeyCafeError** – Base for all SDK errors.
- **APIError** – API error; has `status_code`, `response_data`.
- **AuthenticationError** – API key required but not set.
- **ValidationError** – Invalid parameters.
- **RateLimitError** – Rate limited.

All defined in `heycafe.exceptions`.
