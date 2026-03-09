# Push Workflow

1. 读取 push directive。
2. 依据当前技能模板重建根层与容器层的 `AGENTS.md + README.md`，并刷新 `Mother_Doc/docs/**` 的 `AGENTS.md` 与 README 模板镜像。
3. 重新执行 scan。
4. 自动 collect。
5. 返回 push、scan、collect 的组合结果。
