#!/usr/bin/env bash

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_root="$(cd "$script_dir/.." && pwd)"
product_root="$(cd "$skill_root/../.." && pwd)"
workspace_root="$(cd "$product_root/.." && pwd)"
skill_name="$(basename "$skill_root")"

export META_AGENT_BROWSER_SKILL_ROOT="${META_AGENT_BROWSER_SKILL_ROOT:-$skill_root}"
export META_AGENT_BROWSER_PRODUCT_ROOT="${META_AGENT_BROWSER_PRODUCT_ROOT:-$product_root}"
export META_AGENT_BROWSER_WORKSPACE_ROOT="${META_AGENT_BROWSER_WORKSPACE_ROOT:-$workspace_root}"
export META_AGENT_BROWSER_RUNTIME_DIR="${META_AGENT_BROWSER_RUNTIME_DIR:-$workspace_root/Codex_Skill_Runtime/$skill_name}"
export META_AGENT_BROWSER_RESULT_DIR="${META_AGENT_BROWSER_RESULT_DIR:-$workspace_root/Codex_Skills_Result/$skill_name}"

meta_agent_browser_prepare_dirs() {
  mkdir -p "$META_AGENT_BROWSER_RUNTIME_DIR" "$META_AGENT_BROWSER_RESULT_DIR"
}
