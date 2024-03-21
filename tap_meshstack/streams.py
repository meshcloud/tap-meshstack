"""Stream type classes for tap-meshstack."""

from pathlib import Path

from tap_meshstack.client import MESHOBJECT_TAGS_SCHEMA, FederationMeshObjectStream
from tap_meshstack.client import KrakenMeshObjectStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

# the meshStack API does currently not apply rounding consistently in all endpoints, especially when line items from
# cloud providers are involved. We have to compensate for this here. This should be solved by meshStack in the future.
CURRENCY_AMOUNT_SCALE = 5
class MeshChargebackStatementsStream(KrakenMeshObjectStream):
    name = "meshChargebacks"
    name_singular = "meshChargeback"
    meshobject_version = "application/vnd.meshcloud.api.meshchargeback.v3.hal+json"

    def transform_record(self, record: dict):
        super().transform_record(record)

        for li in record["status"]["lineItems"]:
            li["netAmount"] = round(li["netAmount"], CURRENCY_AMOUNT_SCALE)
            
            # baseNetAmount is optional, this is not clear in the API docs
            if "baseNetAmount" in li:
                li["baseNetAmount"] = round(li["baseNetAmount"], CURRENCY_AMOUNT_SCALE)

        for na in record["status"]["netAmounts"]:
            na["amount"] = round(na["amount"], CURRENCY_AMOUNT_SCALE)

            # baseNetAmount is optional, this is not clear in the API docs
            if "baseNetAmount" in na:
                na["baseNetAmount"] = round(na["baseNetAmount"], CURRENCY_AMOUNT_SCALE)


class MeshTenantUsageReportsStream(KrakenMeshObjectStream):
    name = "meshTenantUsageReports"
    name_singular = "meshTenantUsageReport"
    meshobject_version = "application/vnd.meshcloud.api.meshtenantusagereport.v2.hal+json"


    def transform_record(self, record: dict):
        # TenantUsageReports don't have a spec.tags field, so we don't call super

        for na in record["status"]["netAmounts"]:
            na["amount"] = round(na["amount"], CURRENCY_AMOUNT_SCALE)
            
            # baseAmount is optional, this is not clear in the API docs
            if "baseAmount" in na:
                na["baseAmount"] = round(na["baseAmount"], CURRENCY_AMOUNT_SCALE)

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

