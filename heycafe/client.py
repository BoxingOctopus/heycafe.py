"""HTTP client for the Hey.Café API."""
# fmt: off
from __future__ import annotations

import base64
from typing import Any

import requests

from heycafe.exceptions import APIError, AuthenticationError

DEFAULT_BASE_URL = "https://endpoint.hey.cafe"


class HeyCafeClient:
    """
    Low-level client for the Hey.Café REST API.

    Handles HTTP requests, response parsing, and error handling.
    See https://endpoint.hey.cafe for API documentation.
    """

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        api_key: str | None = None,
        error_boolean: bool = True,
        error_no_http: bool = False,
        timeout: float = 30.0,
        session: requests.Session | None = None,
    ):
        """
        Initialize the client.

        :param base_url: API base URL (default: https://endpoint.hey.cafe)
        :param api_key: Account API key for endpoints that require authentication
        :param error_boolean: If True, request error_boolean=true so errors are booleans
        :param error_no_http: If True, API keeps HTTP 200 on errors
        :param timeout: Request timeout in seconds
        :param session: Optional requests.Session for connection pooling
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.error_boolean = error_boolean
        self.error_no_http = error_no_http
        self.timeout = timeout
        self._session = session or requests.Session()

    def _default_params(self) -> dict[str, str]:
        params: dict[str, str] = {}
        if self.error_boolean:
            params["error_boolean"] = "true"
        if self.error_no_http:
            params["error_no_http"] = "true"
        return params

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def request(
        self,
        endpoint: str,
        method: str = "GET",
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        use_api_key: bool = False,
    ) -> dict[str, Any]:
        """
        Perform an API request and return the parsed response.

        :param endpoint: Endpoint name (e.g. get_system_hello, get_account_info)
        :param method: HTTP method (GET or POST)
        :param params: Query parameters (for GET) or form data (for POST)
        :param data: Optional POST body (merged with params for POST)
        :param use_api_key: If True, require api_key to be set
        :return: response_data from the API (or full response if no response_data)
        :raises AuthenticationError: When use_api_key=True but no key is set
        :raises APIError: When the API returns an error
        """
        if use_api_key and not self.api_key:
            raise AuthenticationError(
                "This endpoint requires an API key. Set api_key when creating the "
                "client or pass it to the method."
            )

        url = f"{self.base_url}/{endpoint}"
        req_params = {**self._default_params()}
        req_data: dict[str, Any] = {}

        if method.upper() == "GET":
            if params:
                req_params.update(_serialize_params(params))
            resp = self._session.get(
                url,
                params=req_params,
                headers=self._headers(),
                timeout=self.timeout,
            )
        else:
            if params:
                req_params.update(_serialize_params(params))
            if data:
                req_data = _serialize_params(data)
            # POST: some endpoints expect form data
            resp = self._session.post(
                url,
                params=req_params,
                data=req_data if req_data else None,
                headers=self._headers(),
                timeout=self.timeout,
            )

        return self._parse_response(resp, endpoint)

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        use_api_key: bool = False,
    ) -> dict[str, Any]:
        """GET request to the given endpoint."""
        return self.request(
            endpoint, method="GET", params=params, use_api_key=use_api_key
        )

    def post(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        use_api_key: bool = False,
    ) -> dict[str, Any]:
        """POST request to the given endpoint."""
        return self.request(
            endpoint,
            method="POST",
            params=params,
            data=data,
            use_api_key=use_api_key,
        )

    def _parse_response(self, response: requests.Response, endpoint: str) -> dict[str, Any]:
        try:
            body = response.json()
        except ValueError:
            raise APIError(
                f"Invalid JSON response from {endpoint}",
                status_code=response.status_code,
            )

        error = body.get("system_api_error")
        if error is True or (isinstance(error, str) and error.lower() in ("true", "1", "yes")):
            msg = body.get("system_api_error_message") or str(error) or "API returned an error"
            raise APIError(msg, status_code=response.status_code, response_data=body)

        if response.status_code >= 400 and not self.error_no_http:
            raise APIError(
                body.get("system_api_error_message") or f"HTTP {response.status_code}",
                status_code=response.status_code,
                response_data=body,
            )

        if "response_data" in body:
            return body["response_data"]
        return body


def _serialize_params(params: dict[str, Any]) -> dict[str, str]:
    """Convert params to string values for query/body."""
    out: dict[str, str] = {}
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, bool):
            out[k] = "true" if v else "false"
        elif isinstance(v, (list, tuple)):
            out[k] = ",".join(str(x) for x in v)
        else:
            out[k] = str(v)
    return out


def encode_content(text: str) -> str:
    """Base64-encode content for endpoints that require it (e.g. conversation content)."""
    return base64.b64encode(text.encode("utf-8")).decode("ascii")
# fmt: on
