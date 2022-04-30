"""Stream type classes for tap-meshstack."""

from contextvars import Context
import json
from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_meshstack.client import MeshStackStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class ChargebackStatementsStream(MeshStackStream):
    """ChagebackStatements meshObject stream"""
    name = "chargebackStatements"
    path = "/api/meshobjects/meshchargebackstatements"
    # primary_keys = ["id"]
    replication_key = None
    
    

    @property
    def schema(self) -> dict:
        """Get dynamic schema including the configured tag schema

        Returns:
            JSON Schema dictionary for this stream.
        """
    
        schema_filepath = SCHEMAS_DIR / "meshChargebackStatement.json"
        schema = json.loads(Path(schema_filepath).read_text())

        schema["properties"]["spec"]["properties"]["tags"] = self.config["tag_schemas"]["ChargebackStatement"]
        schema["properties"]["status"]["properties"]["lineItems"]["items"]["properties"]["tags"]= self.config["tag_schemas"]["TenantUsageReport"]

        return schema
