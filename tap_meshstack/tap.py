"""meshStack tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_meshstack.streams import (
    MeshTenantUsageReportsStream,
    MeshWorkspacesStream,
    MeshPaymentMethodsStream,
    MeshProjectsStream,
    MeshTenantsStream,
)

STREAM_TYPES = [
    MeshTenantUsageReportsStream,
    MeshPaymentMethodsStream,
    MeshWorkspacesStream,
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
                            "client_id",
                            th.StringType,
                            required=True,
                            description="The client id (key id) of the meshStack API key"
                        ),
                        th.Property(
                            "client_secret",
                            th.StringType,
                            required=True,
                            description="The client secret (key secret) of the meshStack API key"
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
            "cert_path",
            th.StringType,
            required=False,
            description="path to a public SSL certificate used to verify connection to meshStack",
        )
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
