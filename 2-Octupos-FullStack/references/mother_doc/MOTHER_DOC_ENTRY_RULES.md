# Mother_Doc Entry Rules

适用技能：`2-Octupos-FullStack`

## Root Entry

- `Octopus_OS/Mother_Doc/README.md` 是镜像根用途说明。
- `Octopus_OS/Mother_Doc/agents.md` 是镜像根索引入口。
- `Octopus_OS/Mother_Doc/Mother_Doc.md` 是镜像根目录自身的实体说明。
- 每一层目录都延续同一规则：`README.md + agents.md + <folder_name>.md`。

## Dynamic Expansion

- 容器集合不是封闭白名单。
- AI 必须依据项目描述判断是否新增容器。
- 新增容器后，必须同步新增工作目录容器与 `Mother_Doc` 同名目录，并补齐三类固定文件与 `common/` 骨架。
