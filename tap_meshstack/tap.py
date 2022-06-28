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
    # MeshChargebackStatementsStream,
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
            "tag_schemas",
            th.ObjectType(
                 th.Property(
                    "meshChargebackStatement",
                    th.ObjectType(),
                    required=False,
                    description="JSON schema for meshChargebackStatement tags"
                ),
                th.Property(
                    "meshTenantUsageReport",
                    th.ObjectType(
                    ),
                    required=False,
                    description="JSON schema for meshTenantUsageReport tags"
                ),
                th.Property(
                    "meshCustomer",
                    th.ObjectType(
                    ),
                    required=False,
                    description="JSON schema for meshCustomer tags"
                ),
                th.Property(
                    "meshProject",
                    th.ObjectType(
                    ),
                    required=False,
                    description="JSON schema for meshProject tags"
                ),
                th.Property(
                    "meshTenant",
                    th.ObjectType(
                    ),
                    required=False,
                    description="JSON schema for meshTenant tags"
                ),
            ),
            required=True,
            description="JSON Schema for meshObject tags. The tap needs schemas for every object that's part of a consumed stream.",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
