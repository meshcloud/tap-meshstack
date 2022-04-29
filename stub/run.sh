#!/usr/bin/env bash
set -o errexit  # exit on error
set -o errtrace  # enables ERR traps so we can run cleanup
set -o pipefail  # exit on error in a pipe, without this only the status of the last command in a pipe is considered
set -o nounset  # exit on undefined variables

python3 -m http.server