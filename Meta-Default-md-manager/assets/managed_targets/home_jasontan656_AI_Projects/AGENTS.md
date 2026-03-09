[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract. This file is a hard runtime contract for the agent in this workspace.

[TURN START - MANDATORY]

1. Load Contract
- Must read this file before drafting any response.
- Validation command:
- `test -f /home/jasontan656/AI_Projects/AGENTS.md`

2. Stage Guardrails Hook (Do/Don't print, non-memory Meta only)
- Script path:
- `/home/jasontan656/.codex/skills/Meta-mindchain/scripts/meta_stage_guardrails.sh`
- This script is mandatory and command-based.
- At each stage, print guardrails before doing stage actions.

3. TURN_START print command (required)
- `/home/jasontan656/.codex/skills/Meta-mindchain/scripts/meta_stage_guardrails.sh TURN_START`

4. Intent Structuring Hook (command-based)
- Must classify user intent and print a "Skill Read Directive" block before task execution.
- Command template:
- `python3 /home/jasontan656/.codex/skills/Meta-prompt-write/scripts/filter_active_invoke_output.py --mode skill_directive --input-text "<USER_INTENT_TEXT>"`

5. Branch Routing Hook
- Read-only: objective is only read/retrieve/analyze/audit/explain; no disk writes (no create/modify/delete/move/rename).
- Non-read-only: any actual/potential write intent (create/modify/delete/move/rename) is Non-read-only.
- `Meta-browser-operation` load gate:
  - Only read/load `Meta-browser-operation` when the task explicitly involves browser work or explicit frontend/browser operation, or when the user explicitly invokes that skill.
  - For non-browser tasks, and for tasks that do not explicitly involve frontend/browser operation, skip reading `Meta-browser-operation` entirely.
- ROUTE print command (required):
- `/home/jasontan656/.codex/skills/Meta-mindchain/scripts/meta_stage_guardrails.sh ROUTE`

[EXECUTION - MANDATORY]

6. Read-only Workflow
- READ_EXEC print command (required):
- `/home/jasontan656/.codex/skills/Meta-mindchain/scripts/meta_stage_guardrails.sh READ_EXEC`
- Execute only read/retrieve/analyze/report actions.
- Lint/audit is allowed only if no write-back is triggered.

7. Non-read-only Workflow
- WRITE_EXEC print command (required):
- `/home/jasontan656/.codex/skills/Meta-mindchain/scripts/meta_stage_guardrails.sh WRITE_EXEC`
- Apply replacement-first editing flow:
- First run keyword/semantic replacement search (example: `rg -n "<keyword>" <target>`).
- If replacement is insufficient, then apply minimal additive edits.
- If refactor/migration is involved, define observable-effect equivalence (consumer/observables/invariants/witness) before editing.

7.1 Architectural Stability Refusal Rule (Hard)
- If a user request conflicts with `Meta-mindchain` architect-first principles and would harm architecture stability, boundary clarity, abstraction quality, reuse, or long-term cleanliness, the agent must explicitly refuse that path.
- Do not comply just because the user requested it; the user may not be able to judge the architectural impact.
- Refusal must be direct and explicit:
- state what the conflict is,
- state why it harms the architecture,
- propose a cleaner replacement path.
- Do not soften this into a weak reminder and then proceed anyway.

8. GitHub Hook (hard, write turns only)
- 仅当本回合是 Non-read-only 且实际写入发生在以下仓库之一时，才启用自动推送留痕：
  - `/home/jasontan656/AI_Projects/Octopus_OS`
  - `/home/jasontan656/AI_Projects/Codex_Skills_Mirror`
- Read-only 回合不启用。
- 对其他仓库或 `~/AI_Projects` 根目录本身不启用。
- 对命中的每个仓库，必须在同一回合结束前完成一次独立留痕；不得把本回合写入延后到后续回合再补。
- 若同一回合同时写入两个仓库，必须分别各跑一次对应命令。
- 使用以下映射命令：
  - `python3 /home/jasontan656/.codex/skills/Meta-github-operation/scripts/Cli_Toolbox.py commit-and-push --repo Octopus_OS --message "<commit message>" --use-latest-claims --auto-scope --allow-empty`
  - `python3 /home/jasontan656/.codex/skills/Meta-github-operation/scripts/Cli_Toolbox.py commit-and-push --repo Codex_Skills_Mirror --message "<commit message>" --use-latest-claims --auto-scope --allow-empty`
- 若命令失败、被跳过、或与实际写入仓库不匹配，属于 `violation`，必须先修复后才能结束回合。

9. Tool Failure Immediate-Repair Rules
- If any tool fails: analyze the cause, apply fix immediately.
9.1 Deletion Safety Rules (Hard)
- The model is forbidden to use `rm -rf` under any circumstance.
- For bulk deletions, use a `python3` command/script with explicit target paths.
- For small deletions, use `apply_patch` deletion hunks.
- Do not use shell-force recursive deletion as a shortcut.

10. Workspace Rules (always enforced)
- Language policy: Chinese primary, English anchors auxiliary.
- Output policy: extremely concise, core information only, no long-form reports.
- Workspace boundary: `~/AI_Projects` is a multi-repo container root and is intentionally **not** a Git repo. Therefore `git -C /home/jasontan656/AI_Projects ...` failing at root is expected; always run Git commands inside a concrete child repository.
- Repository independence: each project keeps independent Git boundaries (`.git`, `origin`, branches, history).
- If a task already has explicit concrete source paths or concrete target repositories, discovery scope must stay inside those paths/repos; do not scan unrelated sibling repositories under `~/AI_Projects` just to gather more context.
- [Repos] Active repository roots in this contract:
  - `/home/jasontan656/AI_Projects/Octopus_OS`
  - `/home/jasontan656/AI_Projects/Codex_Skills_Mirror`
- [Repos] 其余 sibling 目录当前默认视为退役或非主动路由对象；除非用户显式点名，否则不要把它们当作 active repo 扩展扫描。
- [OctopusOS] Unified workspace root: `/home/jasontan656/AI_Projects/Octopus_OS`.
- [OctopusOS] Unified Mother_Doc root: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc`.
- [Skills] Primary skills directory: `/home/jasontan656/.codex/skills`.
- [Skills] Runtime temp artifacts directory: `Codex_Skill_Runtime`.
- [Skills] Final non-log results directory: `Codex_Skills_Result`.
- [Skills] Mirror directory: `/home/jasontan656/AI_Projects/Codex_Skills_Mirror`.
- [Skills] Skill create/modify location must be `Codex_Skills_Mirror`.

11. Governance/Constitution Violation Handling
- If governance/constitution non-compliance is found, explicitly declare `violation`.
- Fix the `violation` before continuing the original task.

[TURN END - MANDATORY]

12. TURN_END print command (required)
- `/home/jasontan656/.codex/skills/Meta-mindchain/scripts/meta_stage_guardrails.sh TURN_END`

13. Constitution Lint Gate (required)
- Before final result, run Constitution-knowledge-base static lint:
- `python3 /home/jasontan656/.codex/skills/Constitution-knowledge-base/scripts/run_constitution_lints.py --target <CONCRETE_TARGET_ROOT>`
- `<CONCRETE_TARGET_ROOT>` must be the concrete child repository or concrete skill repository actually affected by the task.
- If multiple repositories were affected, run the lint once per repository.
- `/home/jasontan656/AI_Projects` itself is not a valid default target; always pick the real affected repository root.
- Any non-zero exit, or any lint result containing `status=fail`, is a `violation`.
- If a `violation` is found, fix it, rerun the lint, and do not close the task until it passes.

14. Closure
- Ensure branch obligations are complete:
  - read-only: no writes, no commit/push
  - non-read-only touching `Octopus_OS` and/or `Codex_Skills_Mirror`: include commit/push traceability for each affected repo
  - non-read-only not touching those two repos: no GitHub hook obligation from this file
- Then output final result.
