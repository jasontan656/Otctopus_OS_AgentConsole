<part_A>
# Runtime Entry Instruction

- 先走 `contract --json`，再按需读取 `runtime-entry`。
- `agent-browser-runtime-guard.sh` 只做验证与清理，不负责安装外部工具。
- `agent-browser-stable.sh` 是 skill 自己的稳定包装入口，不是上游工具替代品。
</part_A>

<part_B>
{
  "directive_name": "meta_agent_browser_runtime_entry_instruction",
  "directive_version": "1.0.0",
  "doc_kind": "instruction",
  "topic": "runtime-entry",
  "purpose": "Enter Meta-Agent-Browser through CLI JSON, then use the skill-local wrappers around the external agent-browser tool.",
  "instruction": [
    "Treat `python3 scripts/Cli_Toolbox.py contract --json` as the first runtime entry for this skill.",
    "Use `scripts/agent-browser-runtime-guard.sh` only to validate the external prerequisite and clean skill-local stale runtime state.",
    "Use `scripts/agent-browser-stable.sh` for stable multi-step sessions after the runtime guard succeeds."
  ],
  "workflow": [
    "Call contract --json.",
    "Call `python3 scripts/Cli_Toolbox.py directive --topic runtime-entry --json` for the local execution path.",
    "If artifact paths matter, call `python3 scripts/Cli_Toolbox.py paths --json` before choosing screenshot, PDF, download, trace, or auth-state destinations.",
    "Only if the JSON payload is still insufficient, open supplementary human docs such as references/browser-total-entry.md or references/windows-headed-bridge.md."
  ],
  "rules": [
    "Do not run install or patch flows for the external agent-browser binary from inside this skill.",
    "Do not treat deep-dive markdown references as the primary runtime contract.",
    "Do not mix multiple browser runtimes in one branch unless the fallback guide explicitly justifies the switch."
  ]
}
</part_B>
