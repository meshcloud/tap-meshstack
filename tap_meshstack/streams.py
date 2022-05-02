"""Stream type classes for tap-meshstack."""

from argparse import ArgumentError
from contextvars import Context
import json
from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_meshstack.client import MeshStackStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class MeshChargebackStatementsStream(MeshStackStream):
    """MeshChargebackStatementsStream meshObject stream"""
    name = "meshChargebackStatements"
    path = "/api/meshobjects/meshchargebackstatements"
    # primary_keys = ["id"]
    replication_key = None

    records_jsonpath = "$._embedded.meshChargebackStatements[*]"  # Or override `parse_response`.
    
    @property
    def schema(self) -> dict:
        """Get dynamic schema including the configured tag schema

        Returns:
            JSON Schema dictionary for this stream.
        """
    
        schema_filepath = SCHEMAS_DIR / "meshChargebackStatement.json"
        schema = json.loads(Path(schema_filepath).read_text())

        schema["properties"]["spec"]["properties"]["tags"] = self.config["tag_schemas"]["meshChargebackStatement"]
        schema["properties"]["status"]["properties"]["lineItems"]["items"]["properties"]["tags"]= self.config["tag_schemas"]["meshTenantUsageReport"]

        return schema

class MeshPaymentMethodsStream(MeshStackStream):
    """MeshPaymentMethods meshObject stream"""
    name = "meshPaymentMethods"
    path = "/api/meshobjects/meshpaymentmethods"
    
    # primary_keys = ["id"]
    replication_key = None

    records_jsonpath = "$._embedded.meshPaymentMethods[*]" 

    @property
    def schema(self) -> dict:
        schema_filepath = SCHEMAS_DIR / "meshPaymentMethod.json"
        schema = json.loads(Path(schema_filepath).read_text())

        tag_schema = self.config["tag_schemas"].get("meshPaymentMethod")
        if tag_schema is None: 
            raise ArgumentError("tap config did not specify mandatory tag_schemas.meshPaymentMethod key")

        schema["properties"]["spec"]["properties"]["tags"] = tag_schema

        return schema
