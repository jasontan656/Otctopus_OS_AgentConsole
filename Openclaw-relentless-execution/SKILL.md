---
name: "Openclaw-relentless-execution"
description: "Toggle-on execution mode that mirrors OpenClaw's goal-completion behavior: objective contract, lifecycle hooks, tool-first execution, dependency self-healing, retry loops, and stop-only-on-done-or-hard-blocker."
---

# OpenClaw Relentless Execution

## Trigger
Use this skill when user explicitly asks for:
- OpenClaw-like unstoppable execution mode
- "不达目标不罢休" / "直到完成" / "排除万难"
- dependency self-healing + retry loop workflow

When this skill is not invoked, keep normal Codex round-based behavior.

## Full Migration Contract (MANDATORY)
When invoked, switch to `Goal-Completion Mode`:
1. Build objective contract with observable done criteria.
2. Run lifecycle hooks (`before-hook` -> attempts -> `after-hook` -> `flush-hook`).
3. Execute tool-first, not plan-only.
4. On failure: classify -> recover -> retry.
5. Enforce safety guardrails to prevent infinite loops.
6. Stop only when:
- done criteria are satisfied with evidence, or
- hard blocker needs user decision.

## Objective Contract
Create runtime state before substantial work:
- objective
- done_criteria (observable)
- constraints
- guardrails (max attempts/runtime/stagnation/repeat-failure)
- retry budgets per failure class

Use script:
```bash
python3 ~/.codex/skills/openclaw-relentless-execution/scripts/goal_state.py start \
  --id "<goal_id>" \
  --objective "<goal>" \
  --done "<done_criteria>" \
  --constraint "<safety_or_scope_constraint>" \
  --max-total-attempts 12 \
  --max-runtime-minutes 45 \
  --max-stagnation 4 \
  --repeat-failure-limit 3 \
  --budget-dependency-missing 3 \
  --budget-transient-runtime 4 \
  --budget-context-overflow 2 \
  --budget-logic-or-spec-gap 4 \
  --budget-hard-blocker 1
```

## Lifecycle Hooks (must run)
Use OpenClaw-style lifecycle sequence backed by local state, with optional external hook runtime only when explicitly configured:

```bash
python3 ~/.codex/skills/openclaw-relentless-execution/scripts/goal_state.py before-hook \
  --id "<goal_id>" \
  --prompt "<objective + working query>"

python3 ~/.codex/skills/openclaw-relentless-execution/scripts/goal_state.py after-hook \
  --id "<goal_id>" \
  --session-id 019be6dd-7220-7111-b4ea-b25fd1769866 \
  --user-text "<user_message>" \
  --assistant-text "<assistant_reply>"

python3 ~/.codex/skills/openclaw-relentless-execution/scripts/goal_state.py flush-hook \
  --id "<goal_id>" \
  --session-id 019be6dd-7220-7111-b4ea-b25fd1769866 \
  --content "<flush_summary>"
```

Hook runtime policy (Hard):
- No default persistent memory backend is assumed.
- Hook commands may use `--memory-runtime <path>` only when an external compatible runtime is explicitly provided.
- Without an external runtime, lifecycle hooks must degrade to local state logging instead of writing into any repo path.
- Repo path `OctuposOS_RunTime_Frontend/Rise/AI_WorkSpace/OctuposOS_Runtime_Backend/L13_DEV_SESSION_LOG/` remains forbidden for hook writes.

## Execution Loop
Repeat until done or hard blocker:
1. `Attempt`: perform next concrete operation.
2. `Verify`: run checks/tests/observable validation.
3. `Classify failure` (if failed):
- `dependency_missing`
- `transient_runtime`
- `context_overflow`
- `logic_or_spec_gap`
- `hard_blocker`
4. `Recover`:
- dependency missing: install, then retry.
- transient: bounded backoff retry.
- context overflow: shrink/segment work and retry.
- logic gap: minimal diagnostics + patch and retry.
- hard blocker: ask concise decision question.
5. Record step to state file.

Use script:
```bash
python3 ~/.codex/skills/openclaw-relentless-execution/scripts/goal_state.py attempt \
  --id "<goal_id>" \
  --command "<shell_command>" \
  --verify-command "<verification_command>" \
  --auto-heal
```

## Dependency Self-Healing (migrated)
Auto-heal classifier detects common missing dependency patterns:
- `command not found`
- `No module named ...`
- `Cannot find module ...`

Installer order (deterministic):
1. local/runtime toolchain (`uv`, repo package manager)
2. OS package manager (`brew`, `apt-get`)
3. language managers (`pip`, `npm`, `pnpm`)

After install, immediately rerun failed step and verify output.
Do not claim fixed without verification evidence.

## Infinite-Loop Safety (migrated)
Built-in guardrails block endless execution:
- max total attempts
- max runtime minutes
- max no-progress streak
- max repeated same-failure streak
- per-failure retry budgets

If any guardrail trips, run status and ask user for decision before continuing.

## Hard Blocker Definition
- Missing secret/credential/user-owned external permission
- Ambiguous product decision that changes architecture
- Explicit user pause/stop

## Reporting Format
For each completion update:
- `objective_status`: in_progress|done|blocked
- `latest_attempt`
- `evidence`
- `next_action`

## End/Close
Mark final state explicitly:
```bash
python3 ~/.codex/skills/openclaw-relentless-execution/scripts/goal_state.py complete \
  --id "<goal_id>" \
  --result done \
  --summary "<what was completed>" \
  --evidence "<test output / observable proof>"
```

Check state anytime:
```bash
python3 ~/.codex/skills/openclaw-relentless-execution/scripts/goal_state.py status --id "<goal_id>"
```

## References
- OpenClaw mechanism map: `references/openclaw-mechanism-map.md`
