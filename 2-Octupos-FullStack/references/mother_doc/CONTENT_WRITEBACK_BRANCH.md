# Content Writeback Branch

适用阶段：`mother_doc`

## Entry

- [入口规则](MOTHER_DOC_ENTRY_RULES.md)
- [回填规则](MOTHER_DOC_WRITEBACK_RULES.md)
- [状态规则](DOC_STATUS_RULES.md)
- [README 规则](README_MD_RULES.md)
- [Scope Entity 规则](SCOPE_ENTITY_MD_RULES.md)
- [命名参考](PHASE1_CONTAINER_NAMING_REFERENCE.md)

## Use

- 进入这里时，只处理普通 Mother_Doc 文档的覆盖写回与状态同步。
- `AGENTS.md` 的扫描、反收集与模板反推不在这里处理，转去 `agents_manager`。

## Example

- 用户要求新增或调整某个容器目录、common 文档、实体文档、README 或状态块。
- 用户要求根据强化意图覆盖写回当前状态，但不涉及 Git 留痕与日志。
