# README.md Rules For Mother_Doc

适用技能：`2-Octupos-FullStack`

## Fixed Role

- `README.md` 是当前层的浓缩总结说明。
- 它不是索引，也不是目录实体说明。
- 它统一由 `mother_doc > agents_readme_manager` 规则约束，但在不同路径族里承担不同层级的总结职责。
- 当同层 `AGENTS.md` 已经足够判断动作时，`README.md` 是可选阅读。
- 当当前目录内容发生变化时，必须考虑维护同层 `README.md`。

## Content Rule

- 必须说明当前层是什么。
- 必须说明同层 `AGENTS.md` 与 `README.md` 的阅读关系。
- 在 `Mother_Doc/docs/**` 中，必须提示同层 `<folder_name>.md` 是当前目录自身的实体说明。
- 根层 `Octopus_OS/README.md` 必须是总容器层总结，不展开完整技能规则。
- 容器层 `Octopus_OS/<Container_Name>/README.md` 必须是当前容器的 AI-facing summary。
- `Mother_Doc/docs/**/README.md` 必须是当前目录范围、子域与关键文档的详细说明。
- 必须避免承担 `Document Status + Block Registry` 的职责；状态块属于文档本体控制层，不属于 README 用途说明正文。
