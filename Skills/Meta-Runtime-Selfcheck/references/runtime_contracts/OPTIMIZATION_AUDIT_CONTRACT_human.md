---
doc_id: "meta_runtime_selfcheck.optimization_audit_governance_contract"
doc_type: "topic_atom"
topic: "Turn-end optimization audit governance for Meta-Runtime-Selfcheck"
node_role: "topic_atom"
domain_type: "runtime_contract"
anchors:
  - target: "SKILL_RUNTIME_CONTRACT_human.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Optimization audit is a governed branch under the main runtime contract."
  - target: "FINAL_REPLY_MERGE_CONTRACT_human.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Optimization recommendations may need concise user-facing closeout."
---

# OPTIMIZATION_AUDIT_CONTRACT

<part_A>
- 本文件治理 turn-end / runtime-end 的“优化审计轨”。
- 它不替代运行中问题修复，而是在运行结束后补一轮“虽然没错，但是否已经足够优”的正式审计。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_runtime_selfcheck_optimization_audit_governance",
  "directive_version": "1.0.0",
  "doc_kind": "contract",
  "topic": "optimization-audit-governance",
  "purpose": "Govern the turn-end optimization audit track so Meta-Runtime-Selfcheck can report non-blocking but worthwhile improvement opportunities after the runtime path completes.",
  "instruction": [
    "Run this audit after runtime end or turn end once the full execution path is visible.",
    "Compare the observed path against the target intent, execution cost, stability, complexity, maintainability, result quality, and clearly better known patterns available to the model.",
    "Emit optimization points as governed recommendations grouped by whether they mainly improve the current run flow, the skill itself, or future discretionary tuning."
  ],
  "workflow": [
    "Review the completed turn evidence, including successful commands, repeated help discovery, canonical-surface drift, issue recovery cost, and final closure shape.",
    "Create optimization points only when the run was acceptable enough to avoid the problem lane but still not optimal enough to ignore.",
    "For each optimization point, record the evidence, better alternative, recommendation class, expected benefit, risk, and whether execution is recommended.",
    "Merge optimization audit output into turn audit and final closeout without overshadowing the main task answer."
  ],
  "recommendation_classes": [
    {
      "class": "suggestion_only",
      "use_when": "The improvement is discretionary and should stay as a recommendation unless the user asks to pursue it."
    },
    {
      "class": "optimize_runflow",
      "use_when": "The current execution sequence should be tightened on future runs, but the skill surface itself is mostly fine."
    },
    {
      "class": "upgrade_skill",
      "use_when": "The evidence suggests the skill, contract, facade, or runtime carrier should be improved so future turns become cleaner by default."
    }
  ],
  "rules": [
    "Do not output optimization audit items when the turn is still active; defer until turn end unless the caller explicitly requests a partial audit.",
    "Do not dump raw internals; optimization output must be a curated recommendation set.",
    "Do not treat optimization points as auto-authorized skill rewrites.",
    "If an optimization point implies destructive rewrite/delete work, route that future writeback through keyword-first-edit governance and user confirmation."
  ]
}
```
</part_B>
