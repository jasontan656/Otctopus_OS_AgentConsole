# Cli_Toolbox 开发文档架构总览

## 目标
- 提供单入口导入工具，先自动导航，再进入 `Push` 或 `Install`。
- 将 mirror 根目录固定在非隐藏路径。
- 支持全量与单技能两种范围。
- 在产品化仓库形态下，确保全量同步不会把产品层对象推入 codex 安装目录。

## 分层结构
- Entry Layer:
  - `scripts/Cli_Toolbox.py`
- Logic Layer:
  - 参数校验
  - mirror 根目录归一化
  - 目标存在性检测
  - 模式路由
  - Push 下的 rsync 调用
  - 全量 Push 下的技能根发现
  - Install 下的外部技能链返回
- Contract Layer:
  - 结构化 JSON 输出合同

## 关键约束
- 入口脚本保持薄层，不承载业务分散逻辑。
- `Push` 与 `Install` 为独立模式。
- `Install` 不直接落盘安装目录，而是把执行权交给外部技能链。
