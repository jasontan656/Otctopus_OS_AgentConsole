# AGENTS.md Rules For Mother_Doc

适用技能：`2-Octupos-FullStack`

## Fixed Role

- `AGENTS.md` 只允许存在于 `Octopus_OS/Mother_Doc/docs/**`。
- `Octopus_OS/<Container_Name>/` 这类实际工作目录容器不得创建 `AGENTS.md`。
- `AGENTS.md` 是当前 `Mother_Doc` 目录的固定索引入口。
- `AGENTS.md` 管理是 `mother_doc` 阶段下的独立子分支，必须通过 `scan / collect / push` 明确分离。

## Fixed Shape

每个 `AGENTS.md` 必须固定包含：

1. `目标`
2. `同层入口`
3. `下一层入口`
4. `选择规则`
5. `更新边界`
6. `索引契约`
7. `递归动作`

## Managed Branch

- 总入口：[agents_branch/00_BRANCH_INDEX.md](agents_branch/00_BRANCH_INDEX.md)
- `scan`：扫描当前文档树中的 `AGENTS.md` 现状，不回写正文。
- `collect`：把产品侧 `AGENTS.md` 反向采集回技能内 `assets/mother_doc_agents/`。
- `push`：把技能侧当前模板反推回 `Octopus_OS/Mother_Doc/docs/**/AGENTS.md`，随后自动重扫并回收。
