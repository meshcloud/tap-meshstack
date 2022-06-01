"""Stream type classes for tap-meshstack."""

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.plugin_base import PluginBase as TapBaseClass

from tap_meshstack.client import MeshObjectStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class MeshChargebackStatementsStream(MeshObjectStream):
    name = "meshChargebackStatements"
    name_singular = "meshChargebackStatement"
    
    def apply_tag_schemas(self, schema) -> dict:
        # chargeback statements have nested line items, that also have a tag schema
        schema["properties"]["spec"]["properties"]["tags"] = self.load_tag_schema(self.name_singular)
        schema["properties"]["status"]["properties"]["lineItems"]["items"]["properties"]["tags"] = self.load_tag_schema("meshTenantUsageReport")

        return schema

class MeshPaymentMethodsStream(MeshObjectStream):
    name = "meshPaymentMethods"
    name_singular = "meshPaymentMethod"

    def apply_tag_schemas(self, schema) -> dict:
        # chargeback statements have nested line items, that also have a tag schema
        schema["properties"]["spec"]["properties"]["tags"] = self.load_tag_schema(self.name_singular)

        return schema

class MeshCustomersStream(MeshObjectStream):
    name = "meshCustomers"
    name_singular = "meshCustomer"

    def apply_tag_schemas(self, schema) -> dict:
        # chargeback statements have nested line items, that also have a tag schema
        schema["properties"]["spec"]["properties"]["tags"] = self.load_tag_schema(self.name_singular)

        return schema

class MeshProjectsStream(MeshObjectStream):
    name = "meshProjects"
    name_singular = "meshProject"
   
    def apply_tag_schemas(self, schema) -> dict:
        # chargeback statements have nested line items, that also have a tag schema
        schema["properties"]["spec"]["properties"]["tags"] = self.load_tag_schema(self.name_singular)

        return schema

class MeshTenantsStream(MeshObjectStream):
    name = "meshTenants"
    name_singular = "meshTenant"
   
    def apply_tag_schemas(self, schema) -> dict:
        # chargeback statements have nested line items, that also have a tag schema
        schema["properties"]["spec"]["properties"]["tags"] = self.load_tag_schema(self.name_singular)

        return schema
