# 2-Octupos-FullStack Tooling & Workflow Contract

## Contract Header

- `contract_name`: `octopus_fullstack_os_workflow_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`

## Top-Level Resident Docs

- `rules/FULLSTACK_SKILL_HARD_RULES.md`
- `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- `references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md`
- `/home/jasontan656/AI_Projects/AGENTS.md`

## Phase Read Policy

- 单阶段执行时，只读取当前阶段 checklist 与当前阶段直接需要的文档。
- 多阶段连续执行时，阶段切换后必须：
  - 保留 top-level resident docs
  - 重读当前阶段 checklist / doc / command / graph contracts
  - 丢弃上一阶段的阶段文档与局部 focus

## Implementation Policy

- `implementation` 必须像独立人类开发者一样推进：
  - 发现问题
  - 安装依赖
  - 修复环境
  - 运行测试
  - bring-up 服务
  - 验证交付
- doc-code drift 必须被显式识别并修复。

## Evidence Policy

- `evidence` 必须以 `OS_graph` 统一文档 graph 与代码 graph。
- evidence 必须绑定回同一层级结构中的模块、helper、父级目录与 witness 节点。
