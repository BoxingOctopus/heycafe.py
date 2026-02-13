"""Pytest fixtures for heycafe tests."""

import pytest

from heycafe import HeyCafe, HeyCafeClient


@pytest.fixture
def base_url():
    """Base URL for the API (used with responses library)."""
    return "https://endpoint.hey.cafe"


@pytest.fixture
def client(base_url):
    """HeyCafeClient with no API key and test base URL."""
    return HeyCafeClient(base_url=base_url, api_key=None)


@pytest.fixture
def client_with_key(base_url):
    """HeyCafeClient with API key."""
    return HeyCafeClient(base_url=base_url, api_key="test-api-key")


@pytest.fixture
def heycafe(base_url):
    """HeyCafe high-level client with no API key."""
    return HeyCafe(base_url=base_url)


@pytest.fixture
def heycafe_with_key(base_url):
    """HeyCafe high-level client with API key."""
    return HeyCafe(base_url=base_url, api_key="test-api-key")
