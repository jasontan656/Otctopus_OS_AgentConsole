#!/usr/bin/env bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_root="$(cd "$script_dir/.." && pwd)"
product_root="$(cd "$skill_root/../.." && pwd)"
workspace_root="$(cd "$product_root/.." && pwd)"
skill_name="$(basename "$skill_root")"
dependency_root_default="$workspace_root/.product_runtime/external_runtime_dependencies/agent-browser"
agent_browser_bin_default="$dependency_root_default/npm/bin/agent-browser"
agent_browser_bin_dir_default="$dependency_root_default/npm/bin"
playwright_browsers_path_default="$dependency_root_default/ms-playwright"

export META_AGENT_BROWSER_SKILL_ROOT="${META_AGENT_BROWSER_SKILL_ROOT:-$skill_root}"
export META_AGENT_BROWSER_PRODUCT_ROOT="${META_AGENT_BROWSER_PRODUCT_ROOT:-$product_root}"
export META_AGENT_BROWSER_WORKSPACE_ROOT="${META_AGENT_BROWSER_WORKSPACE_ROOT:-$workspace_root}"
export META_AGENT_BROWSER_RUNTIME_DIR="${META_AGENT_BROWSER_RUNTIME_DIR:-$workspace_root/Codex_Skill_Runtime/$skill_name}"
export META_AGENT_BROWSER_RESULT_DIR="${META_AGENT_BROWSER_RESULT_DIR:-$workspace_root/Codex_Skills_Result/$skill_name}"
export META_AGENT_BROWSER_DEPENDENCY_ROOT="${META_AGENT_BROWSER_DEPENDENCY_ROOT:-$dependency_root_default}"
export META_AGENT_BROWSER_AGENT_BROWSER_BIN="${META_AGENT_BROWSER_AGENT_BROWSER_BIN:-$agent_browser_bin_default}"
export META_AGENT_BROWSER_PLAYWRIGHT_BROWSERS_PATH="${META_AGENT_BROWSER_PLAYWRIGHT_BROWSERS_PATH:-$playwright_browsers_path_default}"

agent_browser_bin_dir="$(dirname "$META_AGENT_BROWSER_AGENT_BROWSER_BIN")"
if [[ -d "$agent_browser_bin_dir" ]]; then
  export PATH="$agent_browser_bin_dir${PATH:+:$PATH}"
fi
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$META_AGENT_BROWSER_PLAYWRIGHT_BROWSERS_PATH}"

meta_agent_browser_prepare_dirs() {
  mkdir -p \
    "$META_AGENT_BROWSER_RUNTIME_DIR" \
    "$META_AGENT_BROWSER_RESULT_DIR" \
    "$META_AGENT_BROWSER_DEPENDENCY_ROOT"
}
