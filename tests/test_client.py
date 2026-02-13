"""Tests for HeyCafeClient."""

import pytest
import responses

from heycafe import HeyCafeClient
from heycafe.exceptions import APIError, AuthenticationError


@responses.activate
def test_get_success(client, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_system_hello",
        json={
            "system_api_error": False,
            "response_data": "hello",
        },
        status=200,
    )
    result = client.get("get_system_hello")
    assert result == "hello"


@responses.activate
def test_get_returns_response_data(client, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_account_info",
        json={
            "system_api_error": False,
            "response_data": {"id": "abc", "alias": "hey"},
        },
        status=200,
    )
    result = client.get("get_account_info", params={"query": "hey"})
    assert result == {"id": "abc", "alias": "hey"}


@responses.activate
def test_get_passes_params(client, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_account_info",
        json={"system_api_error": False, "response_data": {}},
        status=200,
    )
    client.get("get_account_info", params={"query": "hey"})
    req = responses.calls[0].request
    assert "query=hey" in req.url


@responses.activate
def test_api_error_raises(client, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_system_hello",
        json={
            "system_api_error": True,
            "system_api_error_message": "Something went wrong",
        },
        status=200,
    )
    with pytest.raises(APIError) as exc_info:
        client.get("get_system_hello")
    assert "Something went wrong" in str(exc_info.value)
    assert exc_info.value.response_data.get("system_api_error") is True


@responses.activate
def test_use_api_key_without_key_raises(client):
    with pytest.raises(AuthenticationError) as exc_info:
        client.get("get_account_cafes", use_api_key=True)
    assert "API key" in str(exc_info.value)


@responses.activate
def test_use_api_key_sends_authorization(client_with_key, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_account_cafes",
        json={"system_api_error": False, "response_data": {}},
        status=200,
    )
    client_with_key.get("get_account_cafes", use_api_key=True)
    req = responses.calls[0].request
    assert req.headers.get("Authorization") == "Bearer test-api-key"


@responses.activate
def test_post_sends_data(client_with_key, base_url):
    responses.add(
        responses.POST,
        f"{base_url}/post_conversation_create",
        json={"system_api_error": False, "response_data": {"id": "conv123"}},
        status=200,
    )
    client_with_key.post(
        "post_conversation_create",
        data={"cafe": "cafe1", "content_raw": "Hello"},
        use_api_key=True,
    )
    req = responses.calls[0].request
    assert req.method == "POST"
    assert "cafe=cafe1" in req.body or "content_raw=Hello" in req.body


@responses.activate
def test_encode_content():
    from heycafe.client import encode_content

    assert encode_content("hello") == "aGVsbG8="
