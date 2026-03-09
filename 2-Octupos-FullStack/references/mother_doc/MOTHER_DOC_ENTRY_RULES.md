# Mother_Doc Entry Rules

适用技能：`2-Octupos-FullStack`

## Root Entry

- `Octopus_OS/Mother_Doc/` 是 Mother_Doc 容器根，不是完整文档树根。
- `Octopus_OS/Mother_Doc/docs/README.md` 是文档镜像根用途说明。
- `Octopus_OS/Mother_Doc/docs/agents.md` 是文档镜像根索引入口。
- `Octopus_OS/Mother_Doc/docs/Mother_Doc.md` 是文档镜像根目录自身的实体说明。
- 每一层目录都延续同一规则：`README.md + agents.md + <folder_name>.md`。
- `agents.md` 只存在于 `Octopus_OS/Mother_Doc/docs/**` 这棵文档树内。
- `Octopus_OS/<Container_Name>/` 这类实际工作目录容器不承载 `agents.md`。
- `Octopus_OS/Mother_Doc/graph/` 承载 `OS_graph` 资产，不属于 docs 树。
- `agents.md` 之外的 markdown 必须带有 `Document Status + Block Registry`。

## Dynamic Expansion

- 容器集合不是封闭白名单。
- AI 必须依据项目描述判断是否新增容器。
- 新增容器后，必须同步新增工作目录容器与 `Mother_Doc/docs` 同名目录，并补齐三类固定文件与 `common/` 骨架。
