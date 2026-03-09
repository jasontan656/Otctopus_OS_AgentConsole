# Push Workflow

1. 读取 push directive。
2. 依据当前技能模板重建 `Octopus_OS/AGENTS.md`、`Octopus_OS/<Container>/AGENTS.md` 与 `Octopus_OS/Mother_Doc/docs/**/AGENTS.md`。
3. 重新执行 scan。
4. 自动 collect。
5. 返回 push、scan、collect 的组合结果。
