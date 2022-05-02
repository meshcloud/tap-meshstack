"""REST client handling, including MeshStackStream base class."""

import requests
from pathlib import Path
from typing import Any, Optional, cast

from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BasicAuthenticator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class MeshStackStream(RESTStream):
    """meshStack stream class."""
    
    # todo: these ones would be actually correct for productive meshStack,
    # but we're protoyping with a mock API that uses different conventions
    next_page_token_jsonpath = "$._links.next.href"

    # records_jsonpath = "$.content[*]"  # Or override `parse_response`.
    # next_page_token_jsonpath = "$.links[?(@.rel=='next')].href"


    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]
    
    @property
    def authenticator(self) -> BasicAuthenticator:
        """Return a new authenticator object."""
        return BasicAuthenticator.create_for_stream(
            self,
            username=self.config.get("auth").get("username"),
            password=self.config.get("auth").get("password"),
        )
 
 
    def prepare_request(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> requests.PreparedRequest:
        """Prepare a request object.

        If partitioning is supported, the `context` object will contain the partition
        definitions. Pagination information can be parsed from `next_page_token` if
        `next_page_token` is not None.

        Args:
            context: Stream partition or context dictionary.
            next_page_token: Token, page number or any request argument to request the
                next page of data.

        Returns:
            Build a request with the stream's URL, path, query parameters,
            HTTP headers and authenticator.
        """
        http_method = self.rest_method
        
        # the next_page_token is be the next page link, if set use it to overwrite the URL
        url: str = next_page_token if next_page_token is not None else self.get_url(context)
        
        params: dict = self.get_url_params(context, next_page_token)
        request_data = self.prepare_request_payload(context, next_page_token)
        headers = self.http_headers

        authenticator = self.authenticator
        if authenticator:
            headers.update(authenticator.auth_headers or {})
            params.update(authenticator.auth_params or {})

        request = cast(
            requests.PreparedRequest,
            self.requests_session.prepare_request(
                requests.Request(
                    method=http_method,
                    url=url,
                    params=params,
                    headers=headers,
                    json=request_data,
                ),
            ),
        )
        return request
