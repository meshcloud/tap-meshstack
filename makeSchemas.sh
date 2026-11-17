#!/usr/bin/env bash

set -o errexit   # exit on error
set -o errtrace  # enables ERR traps so we can run cleanup
set -o pipefail  # exit on error in a pipe, without this only the status of the last command in a pipe is considered

# this script extracts json schemas from an openapi3 specification of meshStack APIs
# the API spec is not official at this time, though we aim to make it available in the future
CLEAR='\033[0m'
RED='\033[0;31m'

main() {
  local apiSpecFile="${1:-}"
  local generatedApiSpecFile="${2:-}"
  if [[ -z $apiSpecFile ]]; then usage "openapi.yaml file argument for meshfed missing"; fi;
  if [[ -z $generatedApiSpecFile ]]; then usage "generated openapi.json file argument for meshfed missing"; fi;

  # meshfed-api, restdocs spec
  extractSchema "$apiSpecFile" "meshWorkspace" "meshWorkspace"
  extractSchema "$apiSpecFile" "meshProjectV2" "meshProject"
  extractSchema "$apiSpecFile" "meshPaymentMethodV2" "meshPaymentMethod"
  extractSchema "$apiSpecFile" "meshTenantV3" "meshTenant"

  # meshfed-api, generated spec (meshfed-release: meshfed/api/build/api-spec/openapi.json)
  extractDereferencedSchema "$generatedApiSpecFile" "MeshTenantUsageReportV3" "meshTenantUsageReport"
  patchAmounts "meshTenantUsageReport"
}

extractSchema() {
    local apiSpecFile="$1"
    local component="$2"
    local meshObject="$3"

    local schemaFile="tap_meshstack/schemas/$meshObject.json"

    echo "extracting $meshObject schema to $schemaFile"
    (jq ".components.schemas.$component | del(.properties._links)" < "$apiSpecFile") > "$schemaFile"
}

# the generated spec nests components via allOf/$ref and marks optional fields as "nullable" (openapi 3.0),
# singer needs a self-contained json schema with nullable types instead
extractDereferencedSchema() {
    local apiSpecFile="$1"
    local component="$2"
    local meshObject="$3"

    local schemaFile="tap_meshstack/schemas/$meshObject.json"

    echo "extracting $meshObject schema to $schemaFile"
    jq --arg component "$component" '
def deref($components):
  if type == "array" then map(deref($components))
  elif type != "object" then .
  elif has("$ref") then $components[.["$ref"] | ltrimstr("#/components/schemas/")] | deref($components)
  elif (.allOf | type) == "array" and (.allOf | length) == 1 then
    (.allOf[0] | deref($components)) + del(.allOf) | deref($components)
  else
    (if .nullable == true and (.type | type) == "string" then .type = [.type, "null"] else . end)
    | del(.nullable, .example, ."x-meshstack-versions")
    | map_values(deref($components))
  end;

.components.schemas as $components
| $components[$component]
| deref($components)
' < "$apiSpecFile" > "$schemaFile"
}

# ideally those would be published already correctly from meshcloud, but blocked on https://github.com/ePages-de/restdocs-api-spec/issues/264
patchAmounts() {
  local meshObject="$1"
  local schemaFile="tap_meshstack/schemas/$meshObject.json"

  # meshStack API does not cap scale at the moment, we have to compensate for this in the tap
  # 5 digits of precision, considering we also have individual line items of primitve billing units coming from cloud provider bills...
  # v3 also has an object "netAmount" and an integer payment method "amount", only patch numbers
  patched_json=$(jq '
def isNumber: (.type == "number") or ((.type | type) == "array" and (.type | index("number") != null));
walk(if type == "object" then
    with_entries(if (.key | test("amount$"; "i")) and (.value | type) == "object" and (.value | isNumber) then
        .value |= (. + {"multipleOf": 0.00001})
    else
        .
    end)
else
    .
end)
' "$schemaFile")

  echo "$patched_json" > "$schemaFile"

}

usage() {
  echo -e "${RED}👉 $1${CLEAR}\n";
  echo "Usage: $0 <openapiForMeshfed.yaml> <generatedOpenapiForMeshfed.json>"
  echo ""
  echo "Example: $0 openapiForMeshfed.yaml ../meshfed-release/meshfed/api/build/api-spec/openapi.json"
  exit 1
}

main "$@"

