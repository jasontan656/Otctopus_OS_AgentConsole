# mod_guidance

- 入口：`scripts/managed_guidance.py`
- 职责：读取 machine-readable 运行合同与阶段指引，并生成 markdown 审计版。
- 不变量：
  - 运行态只允许从 JSON 合同输出规则。
  - markdown 只供人类审计，不是模型运行规则源。
  - 合同变更后必须刷新审计 markdown。
