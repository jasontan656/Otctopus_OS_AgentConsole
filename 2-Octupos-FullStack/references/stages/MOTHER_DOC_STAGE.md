# Mother_Doc Stage

适用阶段：`mother_doc`

## Scope

- 强化当前用户意图。
- 先从 `mother_doc` 分支索引选择子链，再递归读取 `Mother_Doc` 当前索引树。
- 仅在 `Mother_Doc` 树内维护 `README.md`、`AGENTS.md`、`<folder_name>.md`、`common/` 与容器骨架。
- 给受影响的非 `AGENTS.md` 文档回填 `Document Status + Block Registry`，并通过本地 `git` 差异脚本标记为 `modified` / `null` / 保留 `developed`。
- 禁止写开发日志、部署日志与 Git / GitHub 留痕。

## Branch Entry

- 总入口：[00_MOTHER_DOC_BRANCH_INDEX.md](../mother_doc/00_MOTHER_DOC_BRANCH_INDEX.md)
- `direct_writeback`：把用户已明确的需求覆盖写回到 `overview / features / shared / common`。
- `question_backfill`：围绕未收口问题持续问答并回填。
- `agents_readme_manager`：统一管理 `Octopus_OS` 根层、各容器根层与 `Mother_Doc/docs` 文档树中的 `AGENTS.md + README.md` 模板、扫描、回收与反推。

## Required Workflow

1. 先用 `Meta-prompt-write` 强化用户意图。
2. 读取 [00_MOTHER_DOC_BRANCH_INDEX.md](../mother_doc/00_MOTHER_DOC_BRANCH_INDEX.md)，先判定当前任务属于 `direct_writeback`、`question_backfill` 还是 `agents_readme_manager`。
3. 若是普通需求覆盖写回，则进入 `direct_writeback`；若是追问未收口问题，则进入 `question_backfill`；若是 `AGENTS.md / README.md` 模板/索引管理，则进入 `agents_readme_manager`。
4. 进入 `Octopus_OS/Mother_Doc/docs/`，读取根层 `README.md`、`AGENTS.md`、`Mother_Doc.md`。
5. 每进入下一层目录，都先读 `README.md`、再读 `AGENTS.md`、再读同名 `<folder_name>.md`。
6. 递归选择直到完整影响面被覆盖。
7. 覆盖写回当前状态，并仅在 `Mother_Doc` 内刷新受影响目录的三类固定文件，以及 `overview / features / shared / common` 中实际命中的内容。
8. 若还有未收口点，则把问题写入受影响容器的 `features/open_questions.md` 或 `shared/open_questions.md`，供后续 `question_backfill` 使用。
9. 对受影响的非 `AGENTS.md` 文档同步写入 `Document Status + Block Registry`，然后运行基于本地 `git` 差异的状态脚本，统一把被改动文档标为 `modified`。
10. 结束时只保留覆盖后的当前状态，不写日志、不做版本留痕。

## Produces

- `Mother_Doc/docs` 当前状态目录树
- 容器级文档
- 结构级索引
- 文档级与区块级 `modified / developed / null` 状态信号
- `implementation` 阶段输入
