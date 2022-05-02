"""meshStack tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_meshstack.streams import (
    MeshChargebackStatementsStream,
    MeshPaymentMethodsStream,
)

STREAM_TYPES = [
    # MeshChargebackStatementsStream,
    MeshPaymentMethodsStream
]


class TapMeshStack(Tap):
    """meshStack tap class."""
    name = "tap-meshstack"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth",
            th.ObjectType(
                th.Property(
                    "username",
                    th.StringType,
                    required=True,
                      description="The HTTP basic auth user to authenticate against the meshObject API"
                ),
                th.Property(
                    "password",
                    th.StringType,
                    required=True,
                    description="The HTTP basic auth password to authenticate against the meshObject API"
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
        th.Property(
            "tag_schemas",
            th.ObjectType(
                 th.Property(
                    "ChargebackStatement",
                    th.ObjectType(),
                    required=False,
                    description="JSON schema for ChargebackStatement tags"
                ),
                th.Property(
                    "TenantUsageReport",
                    th.ObjectType(
                    ),
                    required=False,
                    description="JSON schema for TenantUsageReport tags"
                )
            ),
            required=True,
            description="Expected JSON Schema for meshObject tags",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
