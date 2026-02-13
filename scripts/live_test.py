#!/usr/bin/env python3
"""
Live test suite for the Hey.Café SDK.

Calls the real API to verify the SDK. Uses HEYCAFE_API_KEY for authenticated
tests and optionally HEYCAFE_SESSION_TOKEN for session-only endpoints (feed,
notifications). Set HEYCAFE_BASE_URL to override the API URL and
HEYCAFE_LIVE_TEST_WRITE=1 to run write tests (e.g. create draft) with a test account.
"""

import os
import sys

# Ensure the package is importable when run from project root or scripts/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from heycafe import HeyCafe
from heycafe.exceptions import APIError, AuthenticationError


def env(key: str, default: str = "") -> str:
    return os.environ.get(key, default).strip()


def run(name: str, fn, *args, **kwargs):
    """Run a test; print pass/fail."""
    try:
        result = fn(*args, **kwargs)
        print(f"  OK   {name}")
        return True, result
    except Exception as e:
        print(f"  FAIL {name}: {e}")
        return False, None


def run_skip_on(name: str, fn, *args, skip_messages=(), **kwargs):
    """Run a test; pass, fail, or skip when the error message contains one of skip_messages."""
    try:
        result = fn(*args, **kwargs)
        print(f"  OK   {name}")
        return True, result
    except APIError as e:
        msg = str(e).lower()
        if any(skip in msg for skip in skip_messages):
            print(f"  SKIP {name}: {e} (endpoint may require session auth)")
            return True, None  # don't count as failed
        print(f"  FAIL {name}: {e}")
        return False, None
    except Exception as e:
        print(f"  FAIL {name}: {e}")
        return False, None


def main():
    base_url = env("HEYCAFE_BASE_URL") or "https://endpoint.hey.cafe"
    api_key = env("HEYCAFE_API_KEY")
    session_token = env("HEYCAFE_SESSION_TOKEN")
    allow_write = env("HEYCAFE_LIVE_TEST_WRITE") == "1"

    client = HeyCafe(
        base_url=base_url,
        api_key=api_key or None,
        session_token=session_token or None,
    )

    print("Live tests (base URL: %s)" % base_url)
    print("API key: %s" % ("set" if api_key else "not set"))
    print("Session token: %s" % ("set" if session_token else "not set"))
    if not api_key and not session_token:
        print("(auth tests skipped without HEYCAFE_API_KEY or HEYCAFE_SESSION_TOKEN)")
    print()

    passed = 0
    failed = 0

    # --- Public endpoints (no key) ---
    print("[Public endpoints]")

    ok, _ = run("system.hello()", client.system.hello)
    if ok:
        passed += 1
    else:
        failed += 1

    ok, _ = run("system.endpoints()", client.system.endpoints)
    if ok:
        passed += 1
    else:
        failed += 1

    ok, _ = run("account.info('hey')", client.account.info, "hey")
    if ok:
        passed += 1
    else:
        failed += 1

    ok, _ = run("cafe.info('python')", client.cafe.info, "python")
    if ok:
        passed += 1
    else:
        failed += 1

    ok, _ = run("explore.hot_conversations()", client.explore.hot_conversations)
    if ok:
        passed += 1
    else:
        failed += 1

    ok, _ = run("search.accounts('hey')", client.search.accounts, "hey")
    if ok:
        passed += 1
    else:
        failed += 1

    ok, _ = run("stats.accounts()", client.stats.accounts)
    if ok:
        passed += 1
    else:
        failed += 1

    # --- Authenticated endpoints (API key or session token) ---
    has_auth = api_key or session_token
    if has_auth:
        print("\n[Authenticated endpoints (read-only)]")

        ok, key_data = run("account.key()", client.account.key)
        if ok:
            passed += 1
        else:
            failed += 1

        # get_account_cafes expects query=account alias; use alias from key() if available
        alias = None
        if key_data:
            alias = key_data.get("alias")
            if not alias and isinstance(key_data.get("account"), dict):
                alias = key_data["account"].get("alias")
        if alias:
            ok, _ = run("account.cafes(query=%r)" % alias, lambda: client.account.cafes(query=alias))
        else:
            ok, _ = run("account.cafes()", client.account.cafes)
        if ok:
            passed += 1
        else:
            failed += 1

        # feed/notifications require session when using only API key; with session_token they pass
        if session_token:
            ok, _ = run("feed.conversations(count=5)", lambda: client.feed.conversations(count=5))
            if ok:
                passed += 1
            else:
                failed += 1
            ok, _ = run("account.notifications()", client.account.notifications)
            if ok:
                passed += 1
            else:
                failed += 1
        else:
            ok, _ = run_skip_on(
                "feed.conversations(count=5)",
                lambda: client.feed.conversations(count=5),
                skip_messages=("needs_session",),
            )
            if ok:
                passed += 1
            else:
                failed += 1
            ok, _ = run_skip_on(
                "account.notifications()",
                client.account.notifications,
                skip_messages=("needs_session",),
            )
            if ok:
                passed += 1
            else:
                failed += 1
    else:
        print("\n[Authenticated endpoints] skipped (no HEYCAFE_API_KEY or HEYCAFE_SESSION_TOKEN)")

    # --- Optional write test (draft only) ---
    if has_auth and allow_write:
        print("\n[Write test (draft)]")
        # Find a café the account is in and create a draft conversation
        get_cafes = (lambda: client.account.cafes(query=alias)) if alias else client.account.cafes
        ok, cafes_data = run(
            "account.cafes()" + (" (query=%r)" % alias if alias else ""),
            get_cafes,
        )
        if ok and cafes_data:
            cafes = cafes_data.get("cafes") or cafes_data.get("cafe_list") or (
                cafes_data if isinstance(cafes_data, list) else []
            )
            if isinstance(cafes, dict):
                cafes = list(cafes.values()) if cafes else []
            cafe_id = None
            if cafes:
                first = cafes[0]
                if isinstance(first, dict):
                    cafe_id = first.get("id") or first.get("alias")
                else:
                    cafe_id = str(first)
            if cafe_id:
                ok, _ = run(
                    "conversation.create(draft=True)",
                    client.conversation.create,
                    cafe=cafe_id,
                    content_raw="[live test draft]",
                    draft=True,
                )
                if ok:
                    passed += 1
                else:
                    failed += 1
            else:
                print("  SKIP conversation.create (no cafe id found)")
        else:
            print("  SKIP conversation.create (no cafes for account)")
    elif has_auth:
        print("\n[Write test] skipped (set HEYCAFE_LIVE_TEST_WRITE=1 to enable)")

    # --- Summary ---
    print()
    print("Summary: %d passed, %d failed" % (passed, failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
