<part_A>
# Meta-Agent-Browser Runtime Contract

- 本文件是给人看的镜像；模型运行时主入口仍然是 `./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py contract --json`。
- 本技能只治理 `Meta-Agent-Browser` 自己的包装层，不接管外部 `agent-browser` 安装与上游实现。
- 需要输出路径时，再调用 `./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py paths --json` 获取当前仓内解析结果。
</part_A>

<part_B>
{
  "contract_name": "meta_agent_browser_runtime_contract",
  "contract_version": "1.0.0",
  "skill_name": "__SKILL_NAME__",
  "runtime_source_policy": {
    "primary_runtime_source": "CLI_JSON",
    "human_markdown_role": "part_a_narrative_for_humans",
    "payload_role": "part_b_json_for_models",
    "markdown_is_not_primary_instruction_source": true
  },
  "tool_entry": {
    "script": "scripts/Cli_Toolbox.py",
    "commands": {
      "contract": "./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py contract --json",
      "directive": "./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py directive --topic <topic> --json",
      "paths": "./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py paths --json"
    }
  },
  "must_use_sequence": [
    "Call contract before consuming runtime guidance for this skill.",
    "Choose the directive topic by actual task intent.",
    "When output files, state files, traces, screenshots, or downloads are involved, also call paths --json before writing artifacts.",
    "Open human mirrors or legacy reference docs only when the direct JSON payload still leaves a real gap."
  ],
  "directive_topics": [
    {
      "topic": "runtime-entry",
      "doc_kind": "instruction",
      "use_when": "The task needs the normal agent-browser execution path, wrapper scripts, or external prerequisite boundary."
    },
    {
      "topic": "fallback-routing",
      "doc_kind": "guide",
      "use_when": "The task is browser-related but runtime selection, fallback order, or headed escalation is still unclear."
    },
    {
      "topic": "output-governance",
      "doc_kind": "guide",
      "use_when": "The task needs screenshots, PDFs, traces, auth state, downloads, or any other skill-generated artifacts."
    }
  ],
  "external_dependency_boundary": [
    "agent-browser is an external prerequisite tool.",
    "This skill may validate and wrap agent-browser usage but must not install, patch, or manage the upstream package inside the skill workflow."
  ],
  "path_policy": {
    "runtime_dir_rule": "Derive runtime logs and audit artifacts from product_root.parent / Codex_Skill_Runtime / __SKILL_NAME__.",
    "result_dir_rule": "Derive default screenshots, PDFs, state files, downloaded files, traces, and generic outputs from product_root.parent / Codex_Skills_Result / __SKILL_NAME__.",
    "resolved_paths_command": "./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py paths --json"
  },
  "hard_constraints": [
    "Do not treat SKILL.md or browser-total-entry.md as the primary runtime instruction source.",
    "Do not let skill-local wrappers mutate the external agent-browser installation.",
    "Do not default new artifacts to the current working directory or /tmp when the skill can resolve its governed output roots."
  ]
}
</part_B>
