# Live testing scripts

These scripts call the real Hey.Café API to verify the SDK works against the live service. Use a **test account** so no real user data is affected.

## Running with Docker (recommended)

No local Python or dependency setup needed. From the **project root**:

```bash
# Build the image (once)
docker build -t heycafe .

# Run live tests (pass API key via env)
docker run --rm -e HEYCAFE_API_KEY="your-test-account-key" heycafe

# With session token (for feed/notifications)
docker run --rm -e HEYCAFE_SESSION_TOKEN="your-session-cookie-value" heycafe

# Optional: override base URL or enable write test
docker run --rm \
  -e HEYCAFE_API_KEY="your-key" \
  -e HEYCAFE_BASE_URL="https://endpoint.hey.cafe" \
  -e HEYCAFE_LIVE_TEST_WRITE=1 \
  heycafe
```

Run unit tests (no integration) in the same image:

```bash
docker run --rm heycafe pytest tests/ -m "not integration" -v
```

Run integration tests (public API, no key):

```bash
docker run --rm heycafe pytest tests/ -m integration -v
```

## Running with Podman

[Podman](https://podman.io/) is a Docker-compatible container engine (daemonless, rootless-friendly). Use the same image build and run workflow as Docker; only the command name changes.

**Build the image** (from project root). Use either the Dockerfile or the Containerfile:

```bash
# Using the Dockerfile (same as Docker)
podman build -t heycafe -f Dockerfile .

# Or, if you have a Containerfile (alias for Dockerfile)
podman build -t heycafe .
```

**Run the same commands as above**, with `podman` instead of `docker`:

```bash
# Live tests
podman run --rm -e HEYCAFE_API_KEY="your-test-account-key" heycafe

# Unit tests
podman run --rm heycafe pytest tests/ -m "not integration" -v

# Integration tests
podman run --rm heycafe pytest tests/ -m integration -v
```

All environment variables (`HEYCAFE_API_KEY`, `HEYCAFE_BASE_URL`, `HEYCAFE_LIVE_TEST_WRITE`) work the same way. No Docker daemon is required.

## Setup (without Docker)

1. **Create a test account** on [Hey.Café](https://hey.cafe) (or use an existing test account).
2. **Get an API key** for that account (account settings → API key). See [Hey.Café’s guide](https://heycafe.invfy.com/support/articles/BP1Z7F1UB2).
3. **Set environment variables** (do not commit these):

   ```bash
   export HEYCAFE_API_KEY="your-test-account-api-key"
   # optional (for feed/notifications when API key returns "needs_session"):
   export HEYCAFE_SESSION_TOKEN="session-cookie-value-from-browser"
   export HEYCAFE_BASE_URL="https://endpoint.hey.cafe"
   ```

## Running the live test suite (without Docker)

From the project root (with the package installed):

```bash
pip install -e .
python scripts/live_test.py
```

Or with env vars inline:

```bash
HEYCAFE_API_KEY="your-key" python scripts/live_test.py
```

## What gets tested

- **Without API key:** Public endpoints only (system hello, endpoints, account info for "hey", café info, explore, search, stats).
- **With API key:** Same as above, plus authenticated read-only calls (account info for self, account cafes). Feed and notifications may return “needs_session” with only an API key; use a session token to test those (see below).
- **With session token:** Same as API key for `account.key()` and `account.cafes()`, and **feed** and **notifications** are tested as real calls (no skip). Optionally, a **draft** conversation can be created (set `HEYCAFE_LIVE_TEST_WRITE=1`).

### Getting a session token (for feed / notifications)

Some endpoints (e.g. feed conversations, account notifications) require a **session** rather than only an API key. To test them:

1. Log in to [Hey.Café](https://hey.cafe) in a browser.
2. Open DevTools → Application (or Storage) → Cookies → `https://hey.cafe` (or the domain the app uses).
3. Copy the value of the session cookie (often named `session` or similar).
4. Run the live test with that value:
   ```bash
   export HEYCAFE_SESSION_TOKEN="paste-cookie-value-here"
   python scripts/live_test.py
   ```
   You can set both `HEYCAFE_API_KEY` and `HEYCAFE_SESSION_TOKEN`; the script uses the key for key/cafes and the session for feed/notifications.

Session tokens are tied to your browser login and may expire; treat them as sensitive and do not commit them.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `HEYCAFE_API_KEY` | For auth tests | Test account API key |
| `HEYCAFE_SESSION_TOKEN` | No | Session token (e.g. browser cookie) for feed/notifications when API key returns “needs_session” |
| `HEYCAFE_BASE_URL` | No | API base URL (default: https://endpoint.hey.cafe) |
| `HEYCAFE_LIVE_TEST_WRITE` | No | Set to `1` to run write tests (e.g. create draft). Use only with a test account. |

## CI

These scripts are not run in CI by default (they need a real API key and hit the live API). You can run them locally or in a scheduled workflow with `HEYCAFE_API_KEY` stored as a repository secret.
