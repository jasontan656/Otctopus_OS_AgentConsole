#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"${script_dir}/agent-browser-runtime-guard.sh" >/dev/null

exec agent-browser "$@"
