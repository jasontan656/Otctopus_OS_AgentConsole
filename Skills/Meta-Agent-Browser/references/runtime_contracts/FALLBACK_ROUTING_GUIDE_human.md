---
doc_id: meta_agent_browser.references_runtime_contracts_fallback_routing_guide
doc_type: routing_doc
topic: Fallback Routing Guide
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

<part_A>
# Fallback Routing Guide

- 正常路径仍然先走 `agent-browser`。
- 只有外部前置条件失败、daemon 不稳定，或必须做 GUI 验证时，才切到下一级 runtime。
- 浏览器 fallback 仍保留，但它们现在是 CLI 合同后的补充路径，不再是主入口。
</part_A>

<part_B>
{
  "directive_name": "meta_agent_browser_fallback_routing_guide",
  "directive_version": "1.0.0",
  "doc_kind": "guide",
  "topic": "fallback-routing",
  "purpose": "Define the runtime escalation order for browser tasks handled by Meta-Agent-Browser.",
  "instruction": [
    "Default order remains agent-browser -> WSL headless fallback -> Windows headed bridge.",
    "Read references/browser-total-entry.md only as a human supplement after the CLI payload has established that fallback routing is relevant.",
    "Use references/windows-headed-bridge.md only when headed verification is truly required."
  ],
  "workflow": [
    "Start from the runtime-entry instruction and the skill-local stable wrapper path.",
    "If the external agent-browser prerequisite fails or the daemon remains unstable, switch to the documented headless fallback rather than improvising a new browser stack inside this skill.",
    "Escalate to the Windows headed bridge only when GUI evidence or Windows-specific behavior is required."
  ],
  "rules": [
    "Do not skip directly to headed mode without a runtime reason.",
    "Do not treat fallback markdown docs as the primary entry path for normal browser work.",
    "When a task belongs to another browser workflow family, hand off to that skill rather than absorbing its domain policy into Meta-Agent-Browser."
  ]
}
</part_B>
