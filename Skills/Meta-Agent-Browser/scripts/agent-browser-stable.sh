#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./meta-agent-browser-env.sh
source "${script_dir}/meta-agent-browser-env.sh"
meta_agent_browser_prepare_dirs
"${script_dir}/agent-browser-runtime-guard.sh" >/dev/null

exec agent-browser "$@"
