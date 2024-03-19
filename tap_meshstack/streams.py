"""Stream type classes for tap-meshstack."""

from pathlib import Path

from tap_meshstack.client import MESHOBJECT_TAGS_SCHEMA, FederationMeshObjectStream
from tap_meshstack.client import KrakenMeshObjectStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class MeshChargebackStatementsStream(KrakenMeshObjectStream):
    name = "meshChargebacks"
    name_singular = "meshChargeback"
    meshobject_version = "application/vnd.meshcloud.api.meshchargeback.v2.hal+json"

class MeshTenantUsageReportsStream(KrakenMeshObjectStream):
    name = "meshTenantUsageReports"
    name_singular = "meshTenantUsageReport"
    meshobject_version = "application/vnd.meshcloud.api.meshtenantusagereport.v2.hal+json"

    # TenantUsageReports don't have a spec.tags field
    def transform_record(self, record: dict):
        return

class MeshPaymentMethodsStream(FederationMeshObjectStream):
    name = "meshPaymentMethods"
    name_singular = "meshPaymentMethod"
    meshobject_version = "application/vnd.meshcloud.api.meshpaymentmethod.v2.hal+json"

class MeshWorkspacesStream(FederationMeshObjectStream):
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

