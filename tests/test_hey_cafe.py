"""Tests for high-level HeyCafe client and resources."""

import pytest
import responses

from heycafe import HeyCafe


@responses.activate
def test_hey_cafe_system_hello(heycafe, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_system_hello",
        json={"system_api_error": False, "response_data": "hello"},
        status=200,
    )
    assert heycafe.system.hello() == "hello"


@responses.activate
def test_hey_cafe_account_info(heycafe, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_account_info",
        json={
            "system_api_error": False,
            "response_data": {"id": "x", "alias": "hey", "name": "Hey.Café"},
        },
        status=200,
    )
    info = heycafe.account.info("hey")
    assert info["alias"] == "hey"
    assert info["name"] == "Hey.Café"


@responses.activate
def test_hey_cafe_cafe_info(heycafe, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_cafe_info",
        json={
            "system_api_error": False,
            "response_data": {"id": "c1", "alias": "python", "name": "Python Café"},
        },
        status=200,
    )
    info = heycafe.cafe.info("python")
    assert info["alias"] == "python"


@responses.activate
def test_hey_cafe_conversation_info(heycafe, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_conversation_info",
        json={
            "system_api_error": False,
            "response_data": {"id": "conv1", "content": "Hello world"},
        },
        status=200,
    )
    info = heycafe.conversation.info("conv1")
    assert info["id"] == "conv1"


@responses.activate
def test_hey_cafe_search_accounts(heycafe, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_search_accounts",
        json={
            "system_api_error": False,
            "response_data": {"accounts": [{"alias": "hey"}]},
        },
        status=200,
    )
    result = heycafe.search.accounts("hey")
    assert "accounts" in result


@responses.activate
def test_hey_cafe_explore_hot(heycafe, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_explore_hot_conversations",
        json={"system_api_error": False, "response_data": {"conversations": []}},
        status=200,
    )
    result = heycafe.explore.hot_conversations()
    assert "conversations" in result


@responses.activate
def test_hey_cafe_stats_accounts(heycafe, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_stats_accounts",
        json={"system_api_error": False, "response_data": "12345"},
        status=200,
    )
    result = heycafe.stats.accounts()
    assert result == "12345"


@responses.activate
def test_hey_cafe_bot_giphy(heycafe, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_bot_giphy_search",
        json={"system_api_error": False, "response_data": {"gifs": []}},
        status=200,
    )
    result = heycafe.bot.giphy_search("coffee")
    assert "gifs" in result


@responses.activate
def test_hey_cafe_conversation_create_uses_content_raw(heycafe_with_key, base_url):
    responses.add(
        responses.POST,
        f"{base_url}/post_conversation_create",
        json={"system_api_error": False, "response_data": {"id": "new1"}},
        status=200,
    )
    result = heycafe_with_key.conversation.create(
        cafe="cafe-id",
        content_raw="Hello from SDK",
    )
    assert result["id"] == "new1"
    req = responses.calls[0].request
    body = req.body if isinstance(req.body, str) else req.body.decode()
    assert "content_raw" in body


@responses.activate
def test_hey_cafe_client_low_level_access(heycafe, base_url):
    responses.add(
        responses.GET,
        f"{base_url}/get_system_endpoints",
        json={
            "system_api_error": False,
            "response_data": {"recommended": "endpoint-001.hey.cafe", "endpoints": []},
        },
        status=200,
    )
    result = heycafe.client.get("get_system_endpoints")
    assert "recommended" in result
