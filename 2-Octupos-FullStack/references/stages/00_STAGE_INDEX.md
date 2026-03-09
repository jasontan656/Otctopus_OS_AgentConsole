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

- `mother_doc` 内部先读 `00_MOTHER_DOC_BRANCH_INDEX.md`，再选择 `direct_writeback`、`question_backfill` 或 `AGENTS manager` 子链。
- `implementation` 必须显式引用 `mother_doc` 当前状态产物。
- `implementation` 必须承接 `mother_doc` 产出的 `pending_implementation` 状态信号。
- `evidence` 必须显式引用 `mother_doc` 与 `implementation` 当前状态产物。
- `evidence` 必须承接 implementation 产出的对齐状态、差异范围与 witness 输入，并统一完成日志与 Git / GitHub 留痕。
- 阶段切换时，上一阶段的阶段文档与临时 focus 必须丢弃。
