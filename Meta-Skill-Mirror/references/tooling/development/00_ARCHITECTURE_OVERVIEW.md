# Cli_Toolbox 开发文档架构总览

## 目标
- 提供单入口单向同步工具（mirror -> codex）。
- 将 mirror 根目录固定在非隐藏路径。
- 支持全量与单技能同步两种范围。

## 分层结构
- Entry Layer:
  - `scripts/Cli_Toolbox.py`
- Logic Layer:
  - 参数校验
  - mirror 根目录归一化
  - rsync 调用
- Contract Layer:
  - 结构化 JSON 输出合同

## 关键约束
- 入口脚本保持薄层，不承载业务分散逻辑。
- 只允许 mirror -> codex 唯一动作，不新增其他动作。
