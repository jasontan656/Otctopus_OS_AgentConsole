# Mother_Doc Stage

适用阶段：`mother_doc`

## Scope

- 强化当前用户意图。
- 维护 `Mother_Doc` 当前状态目录树。
- 仅在需要时进入 AGENTS manager，统一治理唯一外部目标 `Octopus_OS/AGENTS.md`。
- 给受影响的非 AGENTS 文档回填 `Document Status + Block Registry`，并通过本地 `git` 差异脚本标记为 `modified` / `null` / 保留 `developed`。
- 禁止写开发日志、部署日志与 Git / GitHub 留痕。

## Branch Entry

- 总入口：[00_MOTHER_DOC_BRANCH_INDEX.md](../mother_doc/00_MOTHER_DOC_BRANCH_INDEX.md)
- `direct_writeback`：把用户已明确的需求覆盖写回到 `overview / features / shared / common`。
- `question_backfill`：围绕未收口问题持续问答并回填。
- `agents_manager`：只负责 `Octopus_OS/AGENTS.md` 的 scan / collect / push，不再管理 container roots 或 `Mother_Doc/docs` 树中的递归 AGENTS。

## Required Workflow

1. 先用 `Meta-prompt-write` 强化用户意图。
2. 读取 [00_MOTHER_DOC_BRANCH_INDEX.md](../mother_doc/00_MOTHER_DOC_BRANCH_INDEX.md)，先判定当前任务属于 `direct_writeback`、`question_backfill` 还是 `agents_manager`。
3. 读取 [项目统一目标基线](../skill_native/10_PROJECT_BASELINE_INDEX.md)，再选择本轮实际影响的容器与共享域。
4. 若是普通需求覆盖写回，则进入 `direct_writeback`；若是追问未收口问题，则进入 `question_backfill`；若是根 `AGENTS.md` 治理，则进入 `agents_manager`。
5. 进入 `Octopus_OS/Mother_Doc/docs/` 后，只读取和维护 `README.md` 与同名 scope 文档；递归 `AGENTS.md` 已废弃。
6. 先按“默认全相关”列出当前需求可能覆盖的容器与共享域，再按最高概率不相关域做减法排除。
7. 覆盖写回当前状态，并仅刷新受影响目录的 README、scope 文档与实际命中的 `overview / features / shared / common` 内容。
8. 若还有未收口点，则把问题写入受影响容器的 `features/open_questions.md`、`shared/open_questions.md`，或项目级 `project_baseline/current_project_development_baseline.md`。
9. 对受影响的非 AGENTS 文档同步写入 `Document Status + Block Registry`，然后运行基于本地 `git` 差异的状态脚本，统一把被改动文档标为 `modified`。
10. 结束时只保留覆盖后的当前状态，不写日志、不做版本留痕。

## Produces

- `Mother_Doc/docs` 当前状态目录树
- 容器级文档
- README 与 scope 文档
- 文档级与区块级 `modified / developed / null` 状态信号
- `implementation` 阶段输入
