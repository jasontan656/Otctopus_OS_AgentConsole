# Mother_Doc Entry Rules

适用技能：`2-Octupos-FullStack`

## Root Entry

- `Octopus_OS/Mother_Doc/` 是 Mother_Doc 容器根，不是完整文档树根。
- `Octopus_OS/Mother_Doc/docs/README.md` 是文档镜像根用途说明。
- `Octopus_OS/Mother_Doc/docs/AGENTS.md` 是文档镜像根索引入口。
- `Octopus_OS/Mother_Doc/docs/Mother_Doc.md` 是文档镜像根目录自身的实体说明。
- 进入任何具体容器前，先读取技能侧 `references/skill_native/10_PROJECT_BASELINE_INDEX.md` 与产品侧 `Octopus_OS/Mother_Doc/docs/Mother_Doc/project_baseline/`。
- 进入普通文档更新前，先读 [00_MOTHER_DOC_BRANCH_INDEX.md](00_MOTHER_DOC_BRANCH_INDEX.md) 判定子分支。
- 进入 `AGENTS.md / README.md` 管理任务前，先读 [AGENTS Branch Index](agents_branch/00_BRANCH_INDEX.md)。
- 每一层目录都延续同一规则：`README.md + AGENTS.md + <folder_name>.md`。
- 每个容器目录在三类固定文件之外，还必须固定具备：
  - `overview/`
  - `features/`
  - `shared/`
  - `common/`
- `Mother_Doc` 容器是特例；除上述固定层外，还固定具备 `project_baseline/`。
- `AGENTS.md` 管理由 3 个路径分支组成：
  - `Octopus_OS/AGENTS.md`
  - `Octopus_OS/<Container_Name>/AGENTS.md`
  - `Octopus_OS/Mother_Doc/docs/**/AGENTS.md`
- `Octopus_OS/Mother_Doc/docs/**/AGENTS.md` 仍然只负责文档树递归索引。
- 容器根与总容器根的 `AGENTS.md` 负责入口选域，不替代文档树内部索引。
- `Octopus_OS/Mother_Doc/graph/` 承载 `OS_graph` 资产，不属于 docs 树。
- `AGENTS.md` 之外的 markdown 必须带有 `Document Status + Block Registry`。
- 每个容器的 `common/` 固定承载：
  - `writing_guides/`
  - `code_abstractions/`
  - `dev_canon/`
- 每个容器的 `overview/` 固定承载：
  - `container_overview.md`
  - `capability_map.md`
  - `surface_index.md`
- 每个容器的 `features/` 固定承载：
  - `feature_catalog.md`
  - `active_requirements.md`
  - `open_questions.md`
- 每个容器的 `shared/` 固定承载：
  - `api_surfaces.md`
  - `event_and_message_flows.md`
  - `shared_contracts.md`
  - `cross_container_dependencies.md`
  - `open_questions.md`
- `common/code_abstractions/` 下固定再拆：
  - `architecture/`
  - `stack/`
  - `naming/`
  - `contracts/`
  - `operations/`

## Dynamic Expansion

- 影响面判断固定从默认全相关开始，再按高概率不相关域做减法。
- 容器集合不是封闭白名单。
- AI 必须依据项目描述判断是否新增容器。
- 新增容器后，必须同步新增工作目录容器与 `Mother_Doc/docs` 同名目录，并补齐三类固定文件与 `common/` 骨架。
- 若新增顶层容器，则必须同步补齐：
  - `Octopus_OS/<Container_Name>/AGENTS.md`
  - `Octopus_OS/Mother_Doc/docs/<Container_Name>/AGENTS.md`
- 新增容器后，相关模板也必须同步进入 `assets/mother_doc_agents/templates/` 并纳入统一 index。
