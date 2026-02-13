# heycafe.py

[![PyPI version](https://img.shields.io/pypi/v/heycafe.svg)](https://pypi.org/project/heycafe/)
[![Tests and security](https://github.com/BoxingOctopus/heycafe.py/actions/workflows/tests.yml/badge.svg)](https://github.com/BoxingOctopus/heycafe.py/actions/workflows/tests.yml)
[![CodeQL](https://github.com/BoxingOctopus/heycafe.py/actions/workflows/codeql.yml/badge.svg)](https://github.com/BoxingOctopus/heycafe.py/actions/workflows/codeql.yml)
[![Integration tests](https://github.com/BoxingOctopus/heycafe.py/actions/workflows/integration.yml/badge.svg)](https://github.com/BoxingOctopus/heycafe.py/actions/workflows/integration.yml)

Python SDK for the [Hey.Café](https://hey.cafe) social media platform REST API. The API is open and does not require a developer account for public endpoints; some endpoints require an account API key.

**API documentation:** [https://endpoint.hey.cafe](https://endpoint.hey.cafe)

**Badges:** PyPI shows the current stable release. Each CI badge links to its workflow; if a badge is failing, open it to see which job failed (unit tests, code quality, SAST, SCA, or integration).

## Installation

```bash
pip install -e .
# or from PyPI (when published)
# pip install heycafe
```

Requirements: Python 3.8+, [requests](https://pypi.org/project/requests/).

## Quick start

```python
from heycafe import HeyCafe

# No API key needed for public endpoints
client = HeyCafe()

# Ping the API
client.system.hello()  # returns "hello"

# Get public account info
info = client.account.info("hey")

# Get café info
cafe = client.cafe.info("python")

# Search
results = client.search.accounts("coffee")
conversations = client.explore.hot_conversations()
```

### With API key (authenticated endpoints)

Endpoints that act on behalf of an account (feed, post, follow, etc.) require an API key. You can obtain one from your account settings; see [Hey.Café’s guide](https://heycafe.invfy.com/support/articles/BP1Z7F1UB2).

```python
from heycafe import HeyCafe

client = HeyCafe(api_key="your-api-key")

# Your feed
feed = client.feed.conversations(count=20)

# Create a conversation (post)
client.conversation.create(cafe="your-cafe-id", content_raw="Hello from the SDK!")

# Follow an account
client.account.follow("someuser")
```

## Client options

```python
HeyCafe(
    api_key=None,           # Account API key for authenticated endpoints
    base_url=None,          # Override API base URL (default: https://endpoint.hey.cafe)
    timeout=30.0,           # Request timeout in seconds (via client)
)
```

For more control, use the low-level client:

```python
from heycafe import HeyCafeClient

client = HeyCafeClient(
    base_url="https://endpoint.hey.cafe",
    api_key="your-key",
    error_boolean=True,     # Prefer boolean error field
    error_no_http=False,    # Keep HTTP 200 on API errors
    timeout=30.0,
)

# Raw GET/POST
data = client.get("get_account_info", params={"query": "hey"})
data = client.post("post_conversation_create", data={"cafe": "x", "content_raw": "Hi"}, use_api_key=True)
```

## Resource overview

| Resource       | Examples |
|----------------|----------|
| **system**     | `hello()`, `endpoints()`, `emoji_search()`, `reactions()` |
| **account**    | `info(query)`, `follow(query)`, `conversations()`, `notifications()` |
| **cafe**       | `info(query)`, `conversations()`, `members()`, `join()`, `create()` |
| **conversation** | `info()`, `comments()`, `create()`, `edit()`, `publish()` |
| **comment**    | `info(query)` |
| **chat**       | `list()`, `info()`, `messages()`, `message_create()`, `create()` |
| **explore**    | `accounts()`, `cafes()`, `conversations()`, `hot_conversations()` |
| **feed**       | `conversations()`, `tags()` (require API key) |
| **search**     | `accounts()`, `cafes()`, `conversations()` |
| **stats**      | `accounts()`, `conversations()`, `comments()`, … (many stat endpoints) |
| **bot**        | `giphy_search()`, `language_detect()`, `website_meta()`, `safespace_text()` |
| **temp**       | `file()`, `preview()` (uploads; require API key) |

## Errors

The SDK raises:

- **`heycafe.APIError`** – API returned an error (with optional `status_code`, `response_data`)
- **`heycafe.AuthenticationError`** – Endpoint requires an API key but none was provided
- **`heycafe.ValidationError`** – Invalid request parameters
- **`heycafe.RateLimitError`** – Rate limited

```python
from heycafe import HeyCafe
from heycafe.exceptions import APIError, AuthenticationError

client = HeyCafe()
try:
    client.account.follow("user")  # needs API key
except AuthenticationError as e:
    print("Set api_key when creating the client")
except APIError as e:
    print(str(e), e.status_code, e.response_data)
```

## Tests

From the project root:

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

Optional: `pytest-cov` for coverage. Unit tests use the `responses` library to mock HTTP. Integration tests (real API) run with `pytest tests/ -m integration`.

**Code quality** (same as CI): `pip install -e ".[dev,quality]"` then `ruff check heycafe tests`, `ruff format --check heycafe tests`, and `mypy heycafe`.

## CI / GitHub Actions

| Workflow | Description |
|----------|-------------|
| **Tests and security** (`.github/workflows/tests.yml`) | Unit tests (Python 3.8–3.12), **code quality** (Ruff lint + format, mypy), **SAST** (Bandit), **SCA** (pip-audit). |
| **CodeQL** (`.github/workflows/codeql.yml`) | **SAST** via GitHub CodeQL (security-extended queries). |
| **Integration tests** (`.github/workflows/integration.yml`) | Calls the live Hey.Café API (public endpoints). Runs on push/PR, daily schedule, and `workflow_dispatch`. |

Optional: set `HEYCAFE_BASE_URL` in integration workflow or repo secrets to override the API base URL.

## Publishing to PyPI

The project is set up for PyPI. To publish:

1. **Check the name**: Ensure the name `heycafe` is available on [PyPI](https://pypi.org/project/heycafe/) (or use a different name in `pyproject.toml`).
2. **Install build tools**: `pip install -e ".[publish]"` (adds `build` and `twine`).
3. **Build**: `python -m build`
4. **Upload**: `python -m twine upload dist/*` (PyPI token or credentials required).

Use a test index first: `twine upload --repository testpypi dist/*`.

## License

Apache License 2.0. Hey.Café is a product of LAMM Creative Solutions.
