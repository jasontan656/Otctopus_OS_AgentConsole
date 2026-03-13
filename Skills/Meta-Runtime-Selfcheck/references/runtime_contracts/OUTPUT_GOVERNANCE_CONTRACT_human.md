---
doc_id: "meta_runtime_selfcheck.output_governance_contract"
doc_type: "topic_atom"
topic: "Output governance for runtime logs and repair/result artifacts"
node_role: "topic_atom"
domain_type: "runtime_contract"
anchors:
  - target: "SKILL_RUNTIME_CONTRACT_human.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Output governance is one governed branch under the runtime contract."
  - target: "DIAGNOSE_WORKFLOW_human.md"
    relation: "supports"
    direction: "cross"
    reason: "Turn-end selfcheck output still needs governed runtime logging."
---

# OUTPUT_GOVERNANCE_CONTRACT

<part_A>
- 本文件约束 runtime log、repair evidence 与未来结果产物的默认落点。
- 当前技能主要把 observability log 写入 runtime root；若未来新增导出型建议报告或修复证据，也必须遵守同一套 result root 规则。
- 所有落点都应从 product root 推导，而不是硬编码当前工作目录。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_runtime_selfcheck_output_governance_contract",
  "directive_version": "2.0.0",
  "doc_kind": "contract",
  "topic": "output-governance",
  "purpose": "Govern runtime logs, report outputs, default result roots, and same-turn repair artifacts for Meta-Runtime-Selfcheck.",
  "instruction": [
    "Write runtime logs under __RUNTIME_ROOT__/logs/runtime_pain_batch/<run_id>.",
    "Treat __RESULT_ROOT__ as the default governed result root for any future exported report artifact or repair evidence artifact.",
    "Document any legacy runtime artifact still outside governed roots and give it an explicit migration or retention rule."
  ],
  "workflow": [
    "Resolve the current product-root derived paths through scripts/Cli_Toolbox.py paths --json.",
    "Keep machine logs and human-readable logs under the namespaced runtime root instead of the current working directory.",
    "If a future directed output path is added, require an explicit path or fall back to the governed result root."
  ],
  "rules": [
    "Do not treat grep or constant strings alone as proof of governed output behavior.",
    "Do not silently preserve scattered legacy runtime artifacts without a documented disposition.",
    "Do not default future report files, repair evidence files, or runtime notes to /tmp or skill-local source folders."
  ]
}
```
</part_B>
