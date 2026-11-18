"""meshStack API key authentication."""

import time
from typing import Optional

import requests
from singer_sdk.authenticators import APIAuthenticatorBase
from singer_sdk.streams import RESTStream

# renew the token a bit early so that it does not expire while a page is in flight
TOKEN_RENEWAL_MARGIN_SECONDS = 60


class ApiKeyAuthenticator(APIAuthenticatorBase):
    """Exchanges a meshStack API key for a short-lived bearer token at /api/login."""

    def __init__(self, stream: RESTStream, api_url: str, client_id: str, client_secret: str) -> None:
        super().__init__(stream=stream)
        self._login_url = f"{api_url}/api/login"
        self._client_id = client_id
        self._client_secret = client_secret
        self._verify = stream.config.get("cert_path") or True
        self._access_token: Optional[str] = None
        self._renew_at = 0.0

    @property
    def auth_headers(self) -> dict:
        if self._access_token is None or time.time() >= self._renew_at:
            self._login()

        return {"Authorization": f"Bearer {self._access_token}"}

    def _login(self) -> None:
        response = requests.post(
            self._login_url,
            json={"clientId": self._client_id, "clientSecret": self._client_secret},
            verify=self._verify,
        )
        response.raise_for_status()
        token = response.json()

        self._access_token = token["access_token"]
        self._renew_at = time.time() + token["expires_in"] - TOKEN_RENEWAL_MARGIN_SECONDS
