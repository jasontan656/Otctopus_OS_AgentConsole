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
- `可优化点` 不是泛泛而谈的“也许能更好”，而是必须满足等效边界后才能成立的正式对象。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_runtime_selfcheck_execution_taxonomy_governance",
  "directive_version": "2.0.0",
  "doc_kind": "contract",
  "topic": "execution-taxonomy-governance",
  "purpose": "Define the runtime boundary between problems, expected failures, and optimization points so Meta-Runtime-Selfcheck can route each signal through the correct closure path.",
  "instruction": [
    "Classify every observed runtime signal into exactly one primary lane: problem, expected failure, or optimization point.",
    "Use the problem lane for concrete runtime pain, failing behavior, unsafe drift, or local defects that should be repaired or strengthened immediately.",
    "Use the expected-failure lane only for stage-scoped, explicitly whitelisted failing signals that are intentionally exposing a defect and must be recorded without auto-killing the run.",
    "Use the optimization-point lane only when the current path already preserves substantially the same output, side-effect boundary, risk boundary, and observable closure signal, yet remains visibly inferior to a better known pattern."
  ],
  "workflow": [
    "First ask whether the signal created a concrete failure, blocker, or immediate runtime risk; if yes, route it as a problem.",
    "If not a problem, ask whether the signal is an intentionally allowed failing validation pattern covered by the active whitelist; if yes, route it as an expected failure.",
    "If the run remained acceptable and the same target result would still hold under a better pattern, compare the observed path against that better pattern using explicit evidence rather than vague style preference.",
    "Only after the equivalence check passes may the path, quality, cost, stability, complexity, maintainability, or known better practice signal be routed as an optimization point.",
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
      "The run did not fail on this path and the same intended output, side-effect scope, risk boundary, and observable result would remain materially intact under the better alternative.",
      "The observed path is still non-canonical, over-costly, more complex than necessary, less stable than the known better pattern, or harder to maintain.",
      "The point is grounded in concrete run evidence plus an explicit knowledge-based comparison against a better implementation, method, skill shape, or task path already known to the model.",
      "The point should be presented as a governed recommendation, not silently ignored and not force-repaired in the same lane as runtime pain."
    ]
  },
  "optimization_point_required_gates": [
    "equivalent_target_output",
    "equivalent_side_effect_boundary",
    "equivalent_risk_boundary",
    "equivalent_observable_closure",
    "better_pattern_is_concrete",
    "evidence_from_current_run_exists"
  ],
  "optimization_point_exclusions": [
    "The alternative changes what the user would receive or observe in a material way.",
    "The alternative broadens side effects, weakens verification, or introduces new unresolved risk.",
    "The observed signal is already a runtime problem, an error, or a whitelisted expected failure.",
    "The recommendation cannot be justified beyond vague taste, token-count vanity, or generic 'could be optimized' language."
  ],
  "optimization_audit_levels": [
    {
      "level": "code",
      "meaning": "Implementation or command-surface shape could be cleaner while preserving the same governed effect."
    },
    {
      "level": "method",
      "meaning": "The operational method or tactical sequence could be improved without changing the target result."
    },
    {
      "level": "skill",
      "meaning": "The skill facade, contract, runtime carrier, or guidance surface caused avoidable friction despite eventual success."
    },
    {
      "level": "task",
      "meaning": "The overall task path was valid but not close to the best route under the current constraints."
    }
  ],
  "rules": [
    "Do not classify everything as a problem just because a better path exists.",
    "Do not hide expected failures inside the optimization lane.",
    "Do not suppress optimization points merely because the run technically succeeded.",
    "Every optimization point must include the better alternative, expected benefit, risk, and whether execution is recommended.",
    "Every optimization point must explain why the point is not a problem, why it is not an expected failure, and why the model believes a better pattern exists from its own governed knowledge rather than from empty stylistic preference."
  ]
}
```
</part_B>
