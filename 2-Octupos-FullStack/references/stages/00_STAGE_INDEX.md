# Stage Index

适用技能：`2-Octupos-FullStack`

## Top-Level Rules

- 顶层常驻文档固定为：
  - `rules/FULLSTACK_SKILL_HARD_RULES.md`
  - `references/runtime/SKILL_RUNTIME_CONTRACT.md`
  - `references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md`
  - `/home/jasontan656/AI_Projects/AGENTS.md`

## Stage Order

1. `mother_doc`
2. `implementation`
3. `evidence`

## Carry-Forward Rules

- `implementation` 必须显式引用 `mother_doc` 当前状态产物。
- `evidence` 必须显式引用 `mother_doc` 与 `implementation` 当前状态产物。
- 阶段切换时，上一阶段的阶段文档与临时 focus 必须丢弃。
