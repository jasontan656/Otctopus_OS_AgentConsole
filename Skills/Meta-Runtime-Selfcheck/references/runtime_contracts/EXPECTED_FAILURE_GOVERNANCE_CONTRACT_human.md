---
doc_id: "meta_runtime_selfcheck.expected_failure_governance_contract"
doc_type: "topic_atom"
topic: "Expected failure governance for Meta-Runtime-Selfcheck"
node_role: "topic_atom"
domain_type: "runtime_contract"
anchors:
  - target: "SKILL_RUNTIME_CONTRACT_human.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Expected failure governance is one governed branch under the runtime contract."
  - target: "DIAGNOSE_WORKFLOW_human.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The turn hook workflow needs this contract to distinguish allowed signals from runtime pain."
---

# EXPECTED_FAILURE_GOVERNANCE_CONTRACT

<part_A>
- 本文件治理“预期失败白名单”。
- 它的作用不是忽略失败，而是把某些阶段内本就应暴露缺陷的信号安全放行并记账。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_runtime_selfcheck_expected_failure_governance_contract",
  "directive_version": "3.0.0",
  "doc_kind": "contract",
  "topic": "expected-failure-governance",
  "purpose": "Define how Meta-Runtime-Selfcheck records and allows intentionally failing validation signals without mistaking them for execution pain that should be auto-killed.",
  "instruction": [
    "Use this contract when the active stage intentionally allows failing tests, lint, or contract validation to expose a defect.",
    "Pass the whitelist JSON into pre-exec-check or run-turn-hook through --expected-failure-file so the hook can distinguish allowed signals from runtime pain.",
    "Record expected failures in turn audit buckets instead of silently ignoring them."
  ],
  "workflow": [
    "Create a whitelist file with rules keyed by stage, command_contains, and optional output_contains or reason_codes.",
    "When a command matches the whitelist, classify it as allow_expected_failure.",
    "Do not auto-repair over the expected failure; preserve the signal and carry it into later validation or strengthening artifacts.",
    "If the observed failure shape drifts beyond the whitelist, fall back to normal runtime selfcheck adjudication."
  ],
  "rules": [
    "Whitelist rules are opt-in and stage-scoped; they must not become broad global ignores.",
    "Expected failures must still be visible in turn audit and final closure.",
    "A whitelist entry may allow and record a failure, but it must not mark an unrelated execution pain as healthy."
  ],
  "payload_shape": {
    "rules": [
      {
        "rule_id": "validation_pytest_red_phase",
        "stages": [
          "validation"
        ],
        "command_contains": [
          "pytest"
        ],
        "output_contains": [
          "failed"
        ],
        "action": "allow_expected_failure",
        "reason": "validation stage may intentionally expose failing tests before the implementation loop closes"
      }
    ]
  }
}
```
</part_B>
