"""Stream type classes for tap-meshstack."""

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.plugin_base import PluginBase as TapBaseClass

from tap_meshstack.client import FederationMeshObjectStream
from tap_meshstack.client import KrakenMeshObjectStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class MeshChargebackStatementsStream(KrakenMeshObjectStream):
    # to refactor
    name = "meshChargeback" #->meshChargebacks
    name_singular = "meshChargebackStatement" #->meshChargeback

    def apply_tag_schemas(self, schema) -> dict:
        tags=self.load_tag_schema(self.name_singular)
        # check if tag is an empty array
        # true: remove tags from schema
        # false: load tags schema from configuration
        if tags["properties"] == {}:
            # tags must be removed from schema as empty RECORDS cannot be handled by meltano loader like big-query
            del schema["properties"]["spec"]["properties"]["tags"]
            return schema
        
        schema["properties"]["spec"]["properties"]["tags"] = self.load_tag_schema(self.name_singular)
        return schema
    
    
    # unfortunately needs an override, because the name + name_singular pattern
    # is not applicable here. (for tag_schema loading it is fitting.)
    def __init__(
        self,
        tap: TapBaseClass,
    ) -> None:
        super().__init__(tap=tap)

        self.next_page_token_jsonpath = "$._links.next.href"
        self.path = f"/api/meshobjects/meshchargeback"
        self.replication_key = None
        self.records_jsonpath = f"$._embedded.meshChargebacks[*]"

class MeshPaymentMethodsStream(FederationMeshObjectStream):
    name = "meshPaymentMethods"
    name_singular = "meshPaymentMethod"

    def apply_tag_schemas(self, schema) -> dict:
        schema["properties"]["spec"]["properties"]["tags"] = self.load_tag_schema(self.name_singular)

        return schema

class MeshCustomersStream(FederationMeshObjectStream):
    name = "meshCustomers"
    name_singular = "meshCustomer"

    def apply_tag_schemas(self, schema) -> dict:
        schema["properties"]["spec"]["properties"]["tags"] = self.load_tag_schema(self.name_singular)

        return schema

class MeshProjectsStream(FederationMeshObjectStream):
    name = "meshProjects"
    name_singular = "meshProject"
   
    def apply_tag_schemas(self, schema) -> dict:
        schema["properties"]["spec"]["properties"]["tags"] = self.load_tag_schema(self.name_singular)

        return schema

class MeshTenantsStream(FederationMeshObjectStream):
    name = "meshTenants"
    name_singular = "meshTenant"
   
    def apply_tag_schemas(self, schema) -> dict:
        schema["properties"]["metadata"]["properties"]["assignedTags"] = self.load_tag_schema(self.name_singular)
    
        return schema
