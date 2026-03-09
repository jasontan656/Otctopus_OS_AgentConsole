# Mother_Doc Stage

适用阶段：`mother_doc`

## Scope

- 强化当前用户意图。
- 递归读取 `Mother_Doc` 索引树，选择并覆盖完整影响面。
- 维护 `Mother_Doc` 结构、容器扩容、命名规则、抽象层骨架与容器文档内容。

## Must Load

- `rules/FULLSTACK_SKILL_HARD_RULES.md`
- `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- `references/mother_doc/MOTHER_DOC_ENTRY_RULES.md`
- `references/mother_doc/AGENTS_MD_RULES.md`
- `references/mother_doc/README_MD_RULES.md`
- `references/mother_doc/MOTHER_DOC_WRITEBACK_RULES.md`
- `references/mother_doc/PHASE1_CONTAINER_NAMING_REFERENCE.md`

## Required Workflow

1. 先结合当前上下文使用 `Meta-prompt-write` 强化用户意图。
2. 先读取 `Octopus_OS/Mother_Doc/README.md` 与 `Octopus_OS/Mother_Doc/agents.md`。
3. 选择下一层覆盖面后，进入该层目录。
4. 在每一层都先读取当前层 `README.md`，再读取当前层 `agents.md`。
5. 按索引继续选择下一层，直到完整影响面被覆盖。
6. 若缺少容器目录、抽象层骨架或递归索引，则先补齐。
7. 以覆盖写入方式回填当前状态，不保留项目内部文档版本。

## Produces

- `Mother_Doc` 当前状态目录树
- 递归 `agents.md` 索引树
- 容器级文档
- `implementation` 阶段输入

## CLI Scope

- `scripts/Cli_Toolbox.py mother-doc-stage`
- `scripts/Cli_Toolbox.py materialize-container-layout`
- `scripts/Cli_Toolbox.py sync-mother-doc-navigation`
