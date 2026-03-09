#!/usr/bin/env bash
set -euo pipefail

runtime_dir="/run/user/$(id -u)/agent-browser"

if ! command -v agent-browser >/dev/null 2>&1; then
  echo "ERROR: agent-browser is not installed globally or not in PATH" >&2
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

if ! find "${HOME}/.cache/ms-playwright" -path '*chrome-headless-shell-linux64/chrome-headless-shell' -type f | grep -q .; then
  agent-browser install
fi

agent-browser --version >/dev/null
echo "agent-browser runtime guard: ok"
