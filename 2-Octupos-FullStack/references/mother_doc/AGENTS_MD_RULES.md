# AGENTS.md Rules For Mother_Doc

适用技能：`2-Octupos-FullStack`

## Fixed Role

- `agents.md` 是当前目录的固定索引入口。
- 它必须指向对等层 `README.md`，并索引下一层路径。
- 它服务于模型递归选域，不服务于版本记录。

## Fixed Shape

每个 `agents.md` 必须固定包含：

1. `Current scope`
2. `Purpose`
3. `Peer`
4. `Index`
5. `Selection Rule`

## Index Rule

- `Index` 中的每个 path 都必须有简短说明。
- 目录 path 说明下一层是什么域。
- 文件 path 说明该文件承载什么最小知识点。
- 当前层若无更深路径，也必须显式写 terminal 状态。

## Maintenance Rule

- 当前目录状态变化后，必须同步刷新当前层 `agents.md`。
- 新增或删除子路径后，必须同步刷新受影响父层 `agents.md`。
- `agents.md` 必须覆盖写回当前状态，不保留旧版本描述。
