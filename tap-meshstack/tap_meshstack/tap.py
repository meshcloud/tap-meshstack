"""meshStack tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_meshstack.streams import (
    meshStackStream,
    ChargebackStatementsStream,
)
# TODO: Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [
    ChargebackStatementsStream
]


class TapmeshStack(Tap):
    """meshStack tap class."""
    name = "tap-meshstack"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "user",
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
        th.Property(
            "api_url",
            th.StringType,
            required=True,
            description="The url of the meshObject API (excluding the /api prefix!)"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
