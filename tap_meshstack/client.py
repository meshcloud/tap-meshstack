"""REST client handling, including MeshObjectStream base class."""

from argparse import ArgumentError

import requests
import json
from pathlib import Path
from typing import Any, Optional, cast

from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BasicAuthenticator
from singer_sdk.plugin_base import PluginBase as TapBaseClass

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class MeshObjectStream(RESTStream):
    """meshStack meshObject stream class."""
 
    def __init__(
        self,
        tap: TapBaseClass,
    ) -> None:
        super().__init__(tap=tap)

        self.next_page_token_jsonpath = "$._links.next.href"
        self.path = f"/api/meshobjects/{self.name.lower()}"
        self.replication_key = None
        self.records_jsonpath = f"$._embedded.${self.name}[*]" 

    @property
    def schema(self) -> dict:
        """Get dynamic schema including the configured tag schema

        Returns:
            JSON Schema dictionary for this stream.
        """
    
        schema_filepath = SCHEMAS_DIR / f"{self.name_singular}.json"
        schema = json.loads(Path(schema_filepath).read_text())

        self.apply_tag_schemas(schema)
        
        return schema
    
    def apply_tag_schemas(self, schema) -> dict:
        """applies tag schemas to a meshObject schema"""
        return schema

    def load_tag_schema(self, name: str) -> dict:
        """loads a valid tag schema from the tap config"""
        tag_schema = self.config and self.config["tag_schemas"].get(name)
        if tag_schema is None: 
            self.logger.warning(f"tap config did not specify the key tag_schemas.${name}. Assuming an empty tag schema instead")
            tag_schema = {
                'type': 'object',
                'required': [],
                'properties': {}
            }

        return tag_schema

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
