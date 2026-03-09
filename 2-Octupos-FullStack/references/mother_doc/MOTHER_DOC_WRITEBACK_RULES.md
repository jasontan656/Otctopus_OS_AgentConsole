# Mother_Doc Writeback Rules

适用技能：`2-Octupos-FullStack`

## Writeback Model

- `mother_doc` 回填采用覆盖写入。
- 项目内部不规划文档版本。
- 任何受影响目录都必须同步刷新：
  - `README.md`
  - `agents.md`
  - `<folder_name>.md`
- 上述刷新只发生在 `Octopus_OS/Mother_Doc/**` 内，不写入实际工作目录容器。

## Structural Rule

- 目录结构变化后，父层索引与当前层实体说明都必须同步更新。
