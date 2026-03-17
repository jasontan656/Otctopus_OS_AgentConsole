---
doc_id: "meta_runtime_selfcheck.execution_taxonomy_governance_contract"
doc_type: "topic_atom"
topic: "Execution taxonomy governance for Meta-Runtime-Selfcheck"
node_role: "topic_atom"
domain_type: "runtime_contract"
anchors:
  - target: "SKILL_RUNTIME_CONTRACT_human.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Signal taxonomy is a top-level runtime rule under the main selfcheck contract."
  - target: "DIAGNOSE_WORKFLOW_human.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Problem signals continue into the immediate repair workflow."
  - target: "OPTIMIZATION_AUDIT_CONTRACT_human.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Optimization points continue into the turn-end audit lane."
---

# EXECUTION_TAXONOMY_CONTRACT

<part_A>
- 本文件显式定义 `问题`、`预期失败`、`可优化点` 的边界。
- 目的不是多造概念，而是避免把所有运行信号都混成同一种 issue。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_runtime_selfcheck_execution_taxonomy_governance",
  "directive_version": "1.0.0",
  "doc_kind": "contract",
  "topic": "execution-taxonomy-governance",
  "purpose": "Define the runtime boundary between problems, expected failures, and optimization points so Meta-Runtime-Selfcheck can route each signal through the correct closure path.",
  "instruction": [
    "Classify every observed runtime signal into exactly one primary lane: problem, expected failure, or optimization point.",
    "Use the problem lane for concrete runtime pain, failing behavior, unsafe drift, or local defects that should be repaired or strengthened immediately.",
    "Use the expected-failure lane only for stage-scoped, explicitly whitelisted failing signals that are intentionally exposing a defect and must be recorded without auto-killing the run.",
    "Use the optimization-point lane for successful or acceptable behavior that is still demonstrably non-optimal compared with the current governed target shape or a clearly better known pattern."
  ],
  "workflow": [
    "First ask whether the signal created a concrete failure, blocker, or immediate runtime risk; if yes, route it as a problem.",
    "If not a problem, ask whether the signal is an intentionally allowed failing validation pattern covered by the active whitelist; if yes, route it as an expected failure.",
    "If the run remained acceptable but the path, quality, cost, stability, complexity, maintainability, or known better practice indicates a better implementation or decision exists, route it as an optimization point.",
    "Problems stay on the runtime repair track, expected failures stay on the governed record-and-allow track, and optimization points flow into the turn-end optimization audit."
  ],
  "classification_criteria": {
    "problem": [
      "Command failed, blocked, or produced an unsafe local state.",
      "The model entered repeated trial-and-error, hesitation, path misuse, or contract mismatch that should be corrected now.",
      "A local fix or bounded strengthening is available inside the active turn."
    ],
    "expected_failure": [
      "The active stage explicitly allows this failing signal through a whitelist rule.",
      "The failure is valuable evidence for red-phase validation and should not be auto-repaired over.",
      "The signal must still be surfaced in audit and closeout."
    ],
    "optimization_point": [
      "The run did not fail on this path, but the execution is visibly non-canonical, over-costly, more complex than necessary, less stable than the known better pattern, or harder to maintain.",
      "The point can be explained with concrete evidence from the completed run and a credible better alternative.",
      "The point should be presented as a governed recommendation, not silently ignored and not force-repaired in the same lane as runtime pain."
    ]
  },
  "rules": [
    "Do not classify everything as a problem just because a better path exists.",
    "Do not hide expected failures inside the optimization lane.",
    "Do not suppress optimization points merely because the run technically succeeded.",
    "Every optimization point must include the better alternative, expected benefit, risk, and whether execution is recommended."
  ]
}
```
</part_B>
