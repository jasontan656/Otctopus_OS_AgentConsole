# Evidence Stage

适用阶段：`evidence`

## Scope

- 从 implementation 产物中提取执行证据、验收 witness 与回写记录，并绑定回 `Mother_Doc`。

## Must Load

- `rules/FULLSTACK_SKILL_HARD_RULES.md`
- `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- `references/stages/MOTHER_DOC_STAGE.md`
- `references/stages/IMPLEMENTATION_STAGE.md`

## Required Inputs

- `mother_doc` 阶段产物
- `implementation` 阶段产物

## Produces

- execution evidence
- acceptance witnesses
- writeback records

## CLI Scope

- `scripts/Cli_Toolbox.py evidence-stage`
