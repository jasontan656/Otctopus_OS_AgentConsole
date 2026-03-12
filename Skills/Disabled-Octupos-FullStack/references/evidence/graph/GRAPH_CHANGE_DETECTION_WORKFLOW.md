# Graph Change Detection Workflow

适用阶段：`evidence > graph`

## Inputs

- implementation diff 范围
- 文档 lifecycle 状态
- 文档节点与代码节点绑定关系

## Workflow

1. 从文档状态中识别 `modified` 范围。
2. 从 implementation 产物中识别已对齐代码范围。
3. 运行 graph detect-changes / impact 类命令。
4. 把差异结果写入 `reports/` 与 `indexes/`。

## Output

- graph-level impact report
- lifecycle-aware status index
- 可供前端和 CLI 共用的差异锚点
