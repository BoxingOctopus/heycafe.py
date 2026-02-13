#!/usr/bin/env python3
"""
Live test suite for the Hey.Café SDK.

Calls the real API to verify the SDK. Uses HEYCAFE_API_KEY for authenticated
tests and optionally HEYCAFE_BASE_URL. Set HEYCAFE_LIVE_TEST_WRITE=1 to run
write tests (e.g. create draft) with a test account only.
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


def main():
    base_url = env("HEYCAFE_BASE_URL") or "https://endpoint.hey.cafe"
    api_key = env("HEYCAFE_API_KEY")
    allow_write = env("HEYCAFE_LIVE_TEST_WRITE") == "1"

    client = HeyCafe(base_url=base_url, api_key=api_key or None)

    print("Live tests (base URL: %s)" % base_url)
    print("API key: %s" % ("set" if api_key else "not set (auth tests skipped)"))
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

    # --- Authenticated endpoints (key required) ---
    if api_key:
        print("\n[Authenticated endpoints (read-only)]")

        ok, _ = run("account.key()", client.account.key)
        if ok:
            passed += 1
        else:
            failed += 1

        ok, _ = run("account.cafes()", client.account.cafes)
        if ok:
            passed += 1
        else:
            failed += 1

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
        print("\n[Authenticated endpoints] skipped (no HEYCAFE_API_KEY)")

    # --- Optional write test (draft only) ---
    if api_key and allow_write:
        print("\n[Write test (draft)]")
        # Find a café the account is in and create a draft conversation
        ok, cafes_data = run("account.cafes()", client.account.cafes)
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
    elif api_key:
        print("\n[Write test] skipped (set HEYCAFE_LIVE_TEST_WRITE=1 to enable)")

    # --- Summary ---
    print()
    print("Summary: %d passed, %d failed" % (passed, failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
