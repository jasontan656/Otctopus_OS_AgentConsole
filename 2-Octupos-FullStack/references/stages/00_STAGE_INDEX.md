# Stage Index

适用技能：`2-Octupos-FullStack`

## Top-Level Rules

- 任意阶段开始前，必须先加载：
  - `rules/FULLSTACK_SKILL_HARD_RULES.md`
  - `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- 顶层规则属于 always-load 规则，不因阶段切换而丢弃。

## Stage Order

1. `mother_doc`
2. `implementation`
3. `evidence`

## Carry-Forward Rules

- `mother_doc`：
  - 先强化用户意图，再递归读取 `Mother_Doc` 当前索引树。
- `implementation`：
  - 必须显式引用 `mother_doc` 当前状态产物。
- `evidence`：
  - 必须显式引用 `mother_doc` 与 `implementation` 当前状态产物。
- 任一后续阶段如果缺失前序阶段输入，必须停止并回到前序阶段补齐。

## Stage Documents

- `MOTHER_DOC_STAGE.md`
- `IMPLEMENTATION_STAGE.md`
- `EVIDENCE_STAGE.md`
