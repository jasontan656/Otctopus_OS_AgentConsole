# Push Workflow

1. 读取 push directive。
2. 依据当前技能模板重建根层 `Octopus_OS/AGENTS.md`，并清理非法额外 `AGENTS.md`。
3. 重新执行 scan。
4. 自动 collect。
5. 返回 push、scan、collect 的组合结果。
