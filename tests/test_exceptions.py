"""Tests for SDK exceptions."""

from heycafe.exceptions import (
    APIError,
    AuthenticationError,
    HeyCafeError,
    RateLimitError,
    ValidationError,
)


def test_hey_cafe_error_base():
    err = HeyCafeError("test")
    assert str(err) == "test"


def test_api_error_attributes():
    err = APIError("failed", status_code=400, response_data={"code": "bad"})
    assert err.status_code == 400
    assert err.response_data == {"code": "bad"}
    assert "failed" in str(err)


def test_authentication_error_inherits_api_error():
    err = AuthenticationError("no key")
    assert isinstance(err, APIError)
    assert isinstance(err, HeyCafeError)


def test_validation_error_inherits():
    err = ValidationError("invalid param")
    assert isinstance(err, APIError)


def test_rate_limit_error_inherits():
    err = RateLimitError("too many requests", status_code=429)
    assert isinstance(err, APIError)
    assert err.status_code == 429
