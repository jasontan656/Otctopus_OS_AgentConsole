# Mother_Doc Branch Index

适用阶段：`mother_doc`

## Purpose

- `mother_doc` 阶段先读本索引，再进入具体子分支。
- 当前阶段只分两条链：
  - `content_writeback`
  - `agents_manager`
- 先选链，再读该链下的规则、workflow、示例与工具入口。

## Branch Entry

- `content_writeback`
  - 入口：[CONTENT_WRITEBACK_BRANCH.md](CONTENT_WRITEBACK_BRANCH.md)
  - 用途：普通 Mother_Doc 文档覆盖写回、状态回填与目录骨架维护。
- `agents_manager`
  - 入口：[AGENTS Branch Index](agents_branch/00_BRANCH_INDEX.md)
  - 用途：只管理 `Octopus_OS/Mother_Doc/docs/**/AGENTS.md` 的模板、扫描、回收与反推。

## Selection Rule

- 当目标是普通文档正文、状态块、容器骨架或 common 文档时，进入 `content_writeback`。
- 当目标是 `AGENTS.md` 模板、索引结构、批量同步、反向采集时，进入 `agents_manager`。
- 两条链都属于 `mother_doc` 阶段；不要把 `implementation` 或 `evidence` 行为混入这里。
