import os
import json

from singer_sdk import Tap, Stream
from typing import List

from tap_meshstack.streams import MeshCustomersStream
from tap_meshstack.tap import TapMeshStack

this_dir = os.path.dirname(os.path.realpath(__file__))
stub_dir = this_dir + "/../../stub/meshobjects"
    
class StubTap(Tap):
    """meshStack tap stub class."""
    name = "tap-meshstack"

    def discover_streams(self) -> List[Stream]:
        return []

def test_tag_transform():
    stream = MeshCustomersStream(StubTap())

    with open(f"{stub_dir}/meshcustomers.json") as f:
        record = json.load(f)["_embedded"]["meshCustomers"][0]
        stream.transform_record(record)
    
        assert record["spec"]["tags"] == [{"key": "environment", "values": ["dev", "prod"]}]




