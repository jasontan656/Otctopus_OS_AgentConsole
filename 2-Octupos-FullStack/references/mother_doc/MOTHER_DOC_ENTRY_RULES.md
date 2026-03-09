# Mother_Doc Entry Rules

适用技能：`2-Octupos-FullStack`

## Root Entry

- `Octopus_OS/Mother_Doc/` 是 Mother_Doc 容器根，不是完整文档树根。
- `Octopus_OS/Mother_Doc/docs/README.md` 是文档镜像根用途说明。
- `Octopus_OS/Mother_Doc/docs/AGENTS.md` 是文档镜像根索引入口。
- `Octopus_OS/Mother_Doc/docs/Mother_Doc.md` 是文档镜像根目录自身的实体说明。
- 进入普通文档更新前，先读 [00_MOTHER_DOC_BRANCH_INDEX.md](00_MOTHER_DOC_BRANCH_INDEX.md) 判定子分支。
- 进入 `AGENTS.md` 管理任务前，先读 [AGENTS Branch Index](agents_branch/00_BRANCH_INDEX.md)。
- 每一层目录都延续同一规则：`README.md + AGENTS.md + <folder_name>.md`。
- `AGENTS.md` 只存在于 `Octopus_OS/Mother_Doc/docs/**` 这棵文档树内。
- `Octopus_OS/<Container_Name>/` 这类实际工作目录容器不承载 `AGENTS.md`。
- `Octopus_OS/Mother_Doc/graph/` 承载 `OS_graph` 资产，不属于 docs 树。
- `AGENTS.md` 之外的 markdown 必须带有 `Document Status + Block Registry`。
- 每个容器的 `common/` 固定承载：
  - `writing_guides/`
  - `code_abstractions/`
  - `dev_canon/`
- `common/code_abstractions/` 下固定再拆：
  - `architecture/`
  - `stack/`
  - `naming/`
  - `contracts/`
  - `operations/`

## Dynamic Expansion

- 容器集合不是封闭白名单。
- AI 必须依据项目描述判断是否新增容器。
- 新增容器后，必须同步新增工作目录容器与 `Mother_Doc/docs` 同名目录，并补齐三类固定文件与 `common/` 骨架。
- 若新增目录会进入 `Mother_Doc/docs/**`，则必须同步补齐该目录的 `AGENTS.md`，并纳入 `agents_manager` 分支的 scan / collect / push 管理。
