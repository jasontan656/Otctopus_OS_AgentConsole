# 模块文档模板说明

## 当前用途
- `SkillsManager-Naming-Manager` 当前没有本地 CLI 模块。
- 本文件仅作为未来若新增工具时的文档模板保留，不参与当前运行态。

## 未来新增模块时的最小字段
- `module_id`
- `tool_alias`
- `entrypoint`
- `responsibility`
- `inputs`
- `outputs`
- `failure_modes`
- `regression_checks`

## 使用规则
- 只有在真实新增本地 CLI 后，才复制本模板并创建具体模块文档。
- 新增模块文档时，必须同步更新 `10_MODULE_CATALOG.yaml` 与 `Cli_Toolbox_USAGE.md`。
