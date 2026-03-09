# Mother_Doc Branch Index

适用阶段：`mother_doc`

## Purpose

- `mother_doc` 阶段先读本索引，再进入具体子分支。
- 当前阶段固定分三条链：
  - `direct_writeback`
  - `question_backfill`
  - `agents_readme_manager`
- 先选链，再读该链下的规则、workflow、示例与工具入口。

## Branch Entry

- `direct_writeback`
  - 入口：[DIRECT_WRITEBACK_BRANCH.md](DIRECT_WRITEBACK_BRANCH.md)
  - 用途：把用户已明确描述的内容覆盖写回到受影响容器的 `overview / features / shared / common`。
- `question_backfill`
  - 入口：[QUESTION_BACKFILL_BRANCH.md](QUESTION_BACKFILL_BRANCH.md)
  - 用途：在初次写回后，把未收口问题整理出来并逐轮向用户追问，再回填到对应文档。
- `agents_readme_manager`
  - 入口：[AGENTS Branch Index](agents_branch/00_BRANCH_INDEX.md)
  - 用途：统一管理 `Octopus_OS/AGENTS.md + README.md`、`Octopus_OS/<Container>/AGENTS.md + README.md` 与 `Octopus_OS/Mother_Doc/docs/**/AGENTS.md + README.md` 三类路径的模板、扫描、回收与反推。

## Selection Rule

- 当目标是把已明确的需求直接写进文档结构时，进入 `direct_writeback`。
- 当目标是围绕未收口点持续问答、补齐设计缺口并回填文档时，进入 `question_backfill`。
- 当目标是 `AGENTS.md / README.md` 模板、索引结构、批量同步、反向采集时，进入 `agents_readme_manager`。
- 三条链都属于 `mother_doc` 阶段；不要把 `implementation` 或 `evidence` 行为混入这里。
