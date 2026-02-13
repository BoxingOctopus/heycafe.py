# Hey.Café Python SDK – API reference

This document summarizes the SDK surface. For full endpoint details (parameters, response shapes, which require an API key), see the official docs: **[https://endpoint.hey.cafe](https://endpoint.hey.cafe)**.

## High-level client: `HeyCafe`

```python
from heycafe import HeyCafe

client = HeyCafe(api_key=None)
```

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

Methods that require an API key will raise `AuthenticationError` if the client was created without one.

## Low-level client: `HeyCafeClient`

```python
from heycafe import HeyCafeClient

client = HeyCafeClient(
    base_url="https://endpoint.hey.cafe",
    api_key=None,
    error_boolean=True,
    error_no_http=False,
    timeout=30.0,
)
```

- **get(endpoint, params=None, use_api_key=False)** – GET request; returns `response_data` or full body.
- **post(endpoint, params=None, data=None, use_api_key=False)** – POST request; returns `response_data` or full body.
- **request(endpoint, method="GET", params=None, data=None, use_api_key=False)** – Generic request.

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
