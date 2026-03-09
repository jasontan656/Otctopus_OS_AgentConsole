# Mother_Doc Writeback Rules

适用技能：`2-Octupos-FullStack`

## Writeback Model

- `mother_doc` 回填采用覆盖写入。
- 项目内部不规划文档版本。
- 版本控制仅由部署与仓库历史统一承载。

## Writeback Sequence

1. 先确认强化后的用户意图与完整影响面。
2. 递归读取目标作用域链路。
3. 更新受影响目录与文件的当前状态内容。
4. 同步刷新受影响目录的 `agents.md` 与 `README.md`。
5. 同步刷新任何新增或删除目录导致变更的父层索引。

## Status Rule

- 文件与文件夹都必须更新到当前状态。
- 不保留“未来计划版本”“旧版说明”“兼容过渡索引”。
- 任何旧索引文件若已被 `agents.md` 取代，必须删除。
