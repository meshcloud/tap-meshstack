"""meshStack tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_meshstack.streams import (
    MeshChargebackStatementsStream,
    MeshCustomersStream,
    MeshPaymentMethodsStream,
    MeshProjectsStream,
    MeshTenantsStream,
)

STREAM_TYPES = [
    MeshChargebackStatementsStream,
    MeshPaymentMethodsStream,
    MeshCustomersStream,
    MeshProjectsStream,
    MeshTenantsStream,
]

class TapMeshStack(Tap):
    """meshStack tap class."""
    name = "tap-meshstack"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "federation",
            th.ObjectType(
                th.Property(
                    "auth",
                    th.ObjectType(
                        th.Property(
                            "username",
                            th.StringType,
                            required=True,
                            description="The HTTP basic auth user to authenticate against the meshObject API for federation"
                        ),
                        th.Property(
                            "password",
                            th.StringType,
                            required=True,
                            description="The HTTP basic auth password to authenticate against the meshObject API for federation"
                        ),
                    ),
                    required=True,
                    description="API authentication configuration",
                ),
                th.Property(
                    "api_url",
                    th.StringType,
                    required=True,
                    description="The url of the meshObject API (excluding the /api prefix!)"
                ),
            ),
            required=True,
            description="Configuration for Federation",
        ),
        th.Property(
            "kraken",
            th.ObjectType(
                th.Property(
                    "auth",
                    th.ObjectType(
                        th.Property(
                            "username",
                            th.StringType,
                            required=True,
                            description="The HTTP basic auth user to authenticate against the meshObject API for kraken"
                        ),
                        th.Property(
                            "password",
                            th.StringType,
                            required=True,
                            description="The HTTP basic auth password to authenticate against the meshObject API for kraken"
                        ),
                    ),
                    required=True,
                    description="API authentication configuration",
                ),
                th.Property(
                    "api_url",
                    th.StringType,
                    required=True,
                    description="The url of the meshObject API (excluding the /api prefix!)"
                ),
            ),
            required=True,
            description="Configuration for Kraken",
        ),
        th.Property(
            "cert_path",
            th.StringType
            required=False,
            description="Path to self-signed SSL certificate",
        )
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
