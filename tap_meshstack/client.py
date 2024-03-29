"""REST client handling, including MeshObjectStream base class."""

from typing import Any, Iterable, Optional, cast

import requests
import json
from pathlib import Path
from typing import Any, Optional, cast

from singer_sdk import typing as th  # JSON schema typing helpers
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BasicAuthenticator
from singer_sdk.plugin_base import PluginBase as TapBaseClass

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

MESHOBJECT_TAGS_SCHEMA = th.ArrayType(
    th.ObjectType(
        th.Property("key", th.StringType, required=True),
        th.Property(
            "values", 
            th.ArrayType(th.StringType),
            description="meshObject tag values are always arrays, even if they just contain a single element.",
            required=True
        )
    )
).to_dict()
 

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
        self.records_jsonpath = f"$._embedded.{self.name}[*]" 

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
    
    def apply_tag_schemas(self, schema):
        """applies tag schemas to a meshObject schema"""

        # by default most meshObjects have tags in spec.tags - override if this is not true
        schema["properties"]["spec"]["properties"]["tags"] = MESHOBJECT_TAGS_SCHEMA

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

        headers.update({
            "accept": self.meshobject_version
        })

        authenticator = self.authenticator
        if authenticator:
            headers.update(authenticator.auth_headers or {})
            params.update(authenticator.auth_params or {})

        # set session certificate
        custom_certificate=self.config.get("cert_path")
        if custom_certificate is not None:
            self.requests_session.verify=custom_certificate
        
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

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        extracted = super().parse_response(response)
        
        for obj in extracted:
            # remove _links field because its contents are not relevant for consumers (except the self-link maybe?)
            del obj["_links"]
            
            self.transform_record(obj)
            
            yield obj

    def transform_record(self, record: dict):
        """
        Transforms a record from the REST API representation to a more ELT friendly representation. 
        Most notably, transform tag properties to a predictable json schema.
        """
        record["spec"]["tags"] = self.transform_meshobject_tags(record["spec"]["tags"])
        
    def transform_meshobject_tags(self, tags: dict):
        return [{"key": k, "values": v} for k, v in tags.items()]

class FederationMeshObjectStream(MeshObjectStream):
    """meshStack meshObject stream class for federation."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config.get("federation").get("api_url")
    
    @property
    def authenticator(self) -> BasicAuthenticator:
        """Return a new authenticator object."""
        return BasicAuthenticator.create_for_stream(
            self,
            username=self.config.get("federation").get("auth").get("username"),
            password=self.config.get("federation").get("auth").get("password"),
        )

class KrakenMeshObjectStream(MeshObjectStream):
    """meshStack meshObject stream class for kraken."""

    @property
    def url_base(self) -> str:
        """Return the Kraken API URL root, configurable via tap settings."""
        return self.config.get("kraken").get("api_url")
    
    @property
    def authenticator(self) -> BasicAuthenticator:
        """Return a new authenticator object."""
        return BasicAuthenticator.create_for_stream(
            self,
            username=self.config.get("kraken").get("auth").get("username"),
            password=self.config.get("kraken").get("auth").get("password"),
        )
