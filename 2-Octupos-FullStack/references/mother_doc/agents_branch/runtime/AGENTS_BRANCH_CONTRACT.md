# Mother_Doc AGENTS/README Branch Contract

适用阶段：`mother_doc`

## Scope

- 管理 3 类路径：
  - `Octopus_OS/AGENTS.md + README.md`
  - `Octopus_OS/<Container_Name>/AGENTS.md + README.md`
  - `Octopus_OS/Mother_Doc/docs/**/AGENTS.md + README.md`
- 不管理实际工作目录容器。
- 不管理普通正文文档。

## Fixed Stages

- `scan`: 扫描当前 AGENTS/README 树现状。
- `collect`: 把当前 AGENTS/README 树反向采集回技能侧 registry。
- `push`: 从技能侧模板反推整棵 AGENTS/README 树，并刷新 registry。

## Assets

- `assets/mother_doc_agents/scan_report.json`
- `assets/mother_doc_agents/registry.json`
- `assets/mother_doc_agents/index.md`
- `assets/mother_doc_agents/collected_tree/`
- `assets/mother_doc_agents/templates/`
