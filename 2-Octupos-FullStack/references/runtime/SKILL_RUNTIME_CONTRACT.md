# 2-Octupos-FullStack Runtime Contract

> Audit copy for `references/runtime/SKILL_RUNTIME_CONTRACT.json`.

- `skill_name`: `2-Octupos-FullStack`
- `role_definition`: 未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护底层文档、开发代码并回填 evidence。
- `execution_model`: 文档直达实现；新文档架构直接匹配代码结构，因此不保留独立的中间 `plan` / `construction_plan` 环节。

## Governance Rules
- 文档、代码与 evidence 都是项目本体的一部分。
- 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。
- `SKILL.md` 门面只描述如何使用本技能，以及文档撰写、代码落盘、evidence 回填规范。
- UI 设计、event 设计、后端支持与其他实现细节，必须落入本技能产出的开发运维文档中。
- 技能写文档与按照文档开发出来的内容是两回事。
