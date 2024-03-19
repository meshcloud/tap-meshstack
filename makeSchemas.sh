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
  local krakenApiSpecFile="${2:-}"
  if [[ -z $apiSpecFile ]]; then usage "openapi.yaml file argument for meshfed missing"; fi;
  if [[ -z $krakenApiSpecFile ]]; then usage "openapi.yaml file argument for kraken missing"; fi;

  # meshfed-api
  extractSchema "$apiSpecFile" "meshWorkspace" "meshWorkspace"
  extractSchema "$apiSpecFile" "meshProjectV2" "meshProject"
  extractSchema "$apiSpecFile" "meshPaymentMethodV2" "meshPaymentMethod"
  extractSchema "$apiSpecFile" "meshTenantV3" "meshTenant"

  # kraken-api
  extractSchema "$krakenApiSpecFile" "meshChargeback" "meshChargeback"
  extractSchema "$krakenApiSpecFile" "meshTenantUsageReport" "meshTenantUsageReport"
}

extractSchema() {
    local apiSpecFile="$1"
    local component="$2"
    local meshObject="$3"

    local schemaFile="tap_meshstack/schemas/$meshObject.json"

    echo "extracting $meshObject schema to $schemaFile"
    (jq ".components.schemas.$component | del(.properties._links)" < "$apiSpecFile") > "$schemaFile"
}

usage() {
  echo -e "${RED}👉 $1${CLEAR}\n";
  echo "Usage: $0 <openapiForMeshfed.yaml>  <openapiForKraken.yaml>"
  echo ""
  echo "Example: $0 openapiForMeshfed.yaml openapiForKraken.yaml"
  exit 1
}

main "$@"