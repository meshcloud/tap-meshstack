"""Stream type classes for tap-meshstack."""

from pathlib import Path

from tap_meshstack.client import MESHOBJECT_TAGS_SCHEMA, FederationMeshObjectStream
from tap_meshstack.client import KrakenMeshObjectStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class MeshChargebackStatementsStream(KrakenMeshObjectStream):
    name = "meshChargebacks"
    name_singular = "meshChargeback"
    meshobject_version = "application/vnd.meshcloud.api.meshchargeback.v2.hal+json"

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
    meshobject_version = "application/vnd.meshcloud.api.meshpaymentmethod.v2.hal+json"

class meshWorkspacesStream(FederationMeshObjectStream):
    name = "meshWorkspaces"
    name_singular = "meshWorkspace"
    meshobject_version = "application/vnd.meshcloud.api.meshworkspace.v1.hal+json"

class MeshProjectsStream(FederationMeshObjectStream):
    name = "meshProjects"
    name_singular = "meshProject"
    meshobject_version="application/vnd.meshcloud.api.meshproject.v2.hal+json"

class MeshTenantsStream(FederationMeshObjectStream):
    name = "meshTenants"
    name_singular = "meshTenant"
    meshobject_version="application/vnd.meshcloud.api.meshtenant.v3.hal+json"
   
    def apply_tag_schemas(self, schema) -> dict:
        schema["properties"]["metadata"]["properties"]["assignedTags"] = MESHOBJECT_TAGS_SCHEMA

    def transform_record(self, record: dict):
        record["metadata"]["assignedTags"] = self.transform_meshobject_tags(record["metadata"]["assignedTags"])

