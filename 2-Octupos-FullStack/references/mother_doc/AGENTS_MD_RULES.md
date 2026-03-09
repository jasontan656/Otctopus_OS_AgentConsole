# AGENTS.md Rules For Mother_Doc

适用技能：`2-Octupos-FullStack`

## Fixed Role

- `agents.md` 只允许存在于 `Octopus_OS/Mother_Doc/**`。
- `Octopus_OS/<Container_Name>/` 这类实际工作目录容器不得创建 `agents.md`。
- `agents.md` 是当前 `Mother_Doc` 目录的固定索引入口。
- 它必须指向对等层 `README.md`，并索引下一层目录与当前层实体文档。

## Fixed Shape

每个 `agents.md` 必须固定包含：

1. `Current scope`
2. `Purpose`
3. `Peer`
4. `Index`
5. `Selection Rule`
