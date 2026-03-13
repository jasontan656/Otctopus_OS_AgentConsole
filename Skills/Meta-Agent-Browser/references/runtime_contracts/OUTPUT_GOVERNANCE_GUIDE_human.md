---
doc_id: meta_agent_browser.references_runtime_contracts_output_governance_guide
doc_type: topic_atom
topic: Output Governance Guide
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

<part_A>
# Output Governance Guide

- 本技能自己的默认产物要回收到受管根，而不是继续散落到 cwd 或 `/tmp`。
- skill 只能治理自己的 wrapper、template 与文档默认值，不能接管上游 `~/.agent-browser` 目录。
- 用户显式给了输出路径时，仍然按用户路径执行。
</part_A>

<part_B>
{
  "directive_name": "meta_agent_browser_output_governance_guide",
  "directive_version": "1.0.0",
  "doc_kind": "guide",
  "topic": "output-governance",
  "purpose": "Keep Meta-Agent-Browser artifacts inside governed runtime and result roots without mutating the external agent-browser installation.",
  "instruction": [
    "Resolve governed paths through `./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py paths --json` before choosing default artifact destinations.",
    "Use __RUNTIME_DIR__ for skill-local runtime logs and guardrail traces.",
    "Use __RESULT_DIR__ for screenshots, PDFs, auth state, downloads, traces, extracted text, and other generic result artifacts."
  ],
  "workflow": [
    "If the user did not provide an explicit output path, fall back to the governed result root for the relevant template or script.",
    "If the user provides an explicit path, honor it without rewriting the external tool itself.",
    "Treat legacy examples using the current working directory or /tmp as deprecated and migrate them to the governed roots or explicit user-provided paths."
  ],
  "rules": [
    "Do not introduce new default artifacts under the current working directory or /tmp.",
    "Do not claim ownership over upstream agent-browser state directories such as ~/.agent-browser; only govern the skill's own wrappers and templates.",
    "Keep document examples aligned with the same default output rules used by the skill-local scripts."
  ]
}
</part_B>
