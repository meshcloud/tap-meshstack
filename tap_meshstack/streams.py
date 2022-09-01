"""Stream type classes for tap-meshstack."""

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.plugin_base import PluginBase as TapBaseClass

from tap_meshstack.client import MESHOBJECT_TAGS_SCHEMA, FederationMeshObjectStream
from tap_meshstack.client import KrakenMeshObjectStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class MeshChargebackStatementsStream(KrakenMeshObjectStream):
    name = "meshChargebacks"
    name_singular = "meshChargeback"

    def transform_record(self, record: dict):
        super().transform_record(record)

        # fix precision of netAmounts so data warehouses pipelines can work with decimal data types instead of FLOATs
        for li in record["status"]["lineItems"]:
            li["netAmount"] = round(li["netAmount"], 2)

        for na in record["status"]["netAmounts"]:
            na["amount"] = round(na["amount"], 2)

class MeshPaymentMethodsStream(FederationMeshObjectStream):
    name = "meshPaymentMethods"
    name_singular = "meshPaymentMethod"

class MeshCustomersStream(FederationMeshObjectStream):
    name = "meshCustomers"
    name_singular = "meshCustomer"

class MeshProjectsStream(FederationMeshObjectStream):
    name = "meshProjects"
    name_singular = "meshProject"

class MeshTenantsStream(FederationMeshObjectStream):
    name = "meshTenants"
    name_singular = "meshTenant"
   
    def apply_tag_schemas(self, schema) -> dict:
        schema["properties"]["metadata"]["properties"]["assignedTags"] = MESHOBJECT_TAGS_SCHEMA

    def transform_record(self, record: dict):
        record["metadata"]["assignedTags"] = self.transform_meshobject_tags(record["metadata"]["assignedTags"])

