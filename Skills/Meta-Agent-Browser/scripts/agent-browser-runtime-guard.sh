#!/usr/bin/env bash
set -euo pipefail

# shellcheck source=./meta-agent-browser-env.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/meta-agent-browser-env.sh"
meta_agent_browser_prepare_dirs

runtime_dir="/run/user/$(id -u)/agent-browser"
chrome_headless_shell_path="${PLAYWRIGHT_BROWSERS_PATH:-$HOME/.cache/ms-playwright}"

if ! command -v agent-browser >/dev/null 2>&1; then
  echo "ERROR: external prerequisite missing: agent-browser is not installed or not in PATH" >&2
  echo "HINT: rerun the Octopus OS product installer so the target-local dependency manifest is applied, or install agent-browser manually outside Meta-Agent-Browser." >&2
  exit 1
fi

# Kill leftover npx daemons; they create unstable socket/session state in WSL.
pkill -f '/\.npm/_npx/.*/node_modules/agent-browser/.*/daemon\.js' >/dev/null 2>&1 || true

if [[ -d "$runtime_dir" ]]; then
  shopt -s nullglob
  for pid_file in "$runtime_dir"/*.pid; do
    pid="$(cat "$pid_file" 2>/dev/null || true)"
    base="${pid_file%.pid}"
    sock_file="${base}.sock"
    if [[ -z "$pid" ]] || ! kill -0 "$pid" >/dev/null 2>&1; then
      rm -f "$pid_file" "$sock_file"
    fi
  done
  shopt -u nullglob
fi

if ! find "$chrome_headless_shell_path" -path '*chrome-headless-shell-linux64/chrome-headless-shell' -type f | grep -q .; then
  echo "ERROR: external prerequisite missing: agent-browser browser assets are not installed" >&2
  echo "HINT: rerun the Octopus OS product installer so browser assets are installed into the target-local dependency root, or install them manually outside Meta-Agent-Browser." >&2
  exit 1
fi

agent-browser --version >/dev/null
echo "agent-browser runtime guard: ok"
