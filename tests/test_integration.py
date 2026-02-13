"""Integration tests that call the real Hey.Café API.

Run with: pytest tests/ -m integration -v
Skip in CI when network is unavailable or to avoid external calls:
  pytest tests/ -m "not integration"
"""

import os

import pytest

from heycafe import HeyCafe
from heycafe.exceptions import APIError


# Base URL can be overridden for testing (e.g. staging)
HEYCAFE_BASE_URL = os.environ.get("HEYCAFE_BASE_URL", "https://endpoint.hey.cafe")


@pytest.fixture(scope="module")
def live_client():
    """Client pointing at real API (no key for public endpoints)."""
    return HeyCafe(base_url=HEYCAFE_BASE_URL)


@pytest.mark.integration
def test_system_hello(live_client):
    """Public endpoint: get_system_hello returns 'hello'."""
    result = live_client.system.hello()
    assert result == "hello"


@pytest.mark.integration
def test_system_endpoints(live_client):
    """Public endpoint: get_system_endpoints returns recommended and list."""
    result = live_client.system.endpoints()
    assert "recommended" in result
    assert "endpoints" in result
    assert isinstance(result["endpoints"], list)
    assert len(result["endpoints"]) >= 1


@pytest.mark.integration
def test_account_info_public(live_client):
    """Public endpoint: get_account_info for known account 'hey'."""
    info = live_client.account.info("hey")
    assert "id" in info
    assert info.get("alias") == "hey"
    assert "name" in info


@pytest.mark.integration
def test_cafe_info_public(live_client):
    """Public endpoint: get_cafe_info for a known café."""
    # Use a café that likely exists (e.g. 'python' or 'general')
    result = live_client.cafe.info("python")
    assert isinstance(result, dict)
    assert "id" in result or "alias" in result


@pytest.mark.integration
def test_explore_hot_conversations(live_client):
    """Public endpoint: get_explore_hot_conversations."""
    result = live_client.explore.hot_conversations()
    assert isinstance(result, dict)


@pytest.mark.integration
def test_search_accounts(live_client):
    """Public endpoint: get_search_accounts."""
    result = live_client.search.accounts("hey")
    assert isinstance(result, dict)


@pytest.mark.integration
def test_stats_accounts(live_client):
    """Public endpoint: get_stats_accounts."""
    result = live_client.stats.accounts()
    # Returns a number or dict depending on API
    assert result is not None
