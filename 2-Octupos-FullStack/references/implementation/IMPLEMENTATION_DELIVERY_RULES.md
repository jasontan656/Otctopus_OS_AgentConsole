# Implementation Delivery Rules

适用阶段：`implementation`

## Delivery Standard

- 模型必须默认像独立人类开发者一样工作。
- 默认要主动做：
  - 依赖安装
  - 环境修复
  - 项目启动
  - 测试执行
  - 本地验证
  - 回填更新

## Blocked Rule

- 只有本地可控范围内的修复动作全部穷尽后，才允许写成真正 blocked。

## Handoff Rule

- 每轮批量文档更新转入实现后，必须在实现完成时整理出可供 `evidence` 追加 implementation batch 的对齐范围与差异摘要。
- implementation 本阶段不得直接写开发日志，也不得直接承担 Git / GitHub 留痕。
