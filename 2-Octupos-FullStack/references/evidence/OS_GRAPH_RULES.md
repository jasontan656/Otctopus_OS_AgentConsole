# OS Graph Rules

适用阶段：`evidence`

## Core Definition

- `OS_graph` 是 `document graph + code graph + evidence graph` 的统一合同层。
- `OS_graph` 固定拆成四层：
  - `narrative_layer`
  - `contract_layer`
  - `implementation_layer`
  - `evidence_layer`

## Node Equivalence

- 目录 = 结构节点
- `README.md` = 当前层用途节点
- `AGENTS.md` = 当前层导航节点
- `<folder_name>.md` = 当前目录自身实体节点
- `overview/*.md` = narrative 节点
- `features/*.md` = narrative/contract 混合节点，按语义切片组织
- `shared/*.md` = contract 节点
- `Document Status + Block Registry` = 变更探测与实现待办节点
- 代码模块 = 实现节点
- helper = helper 节点
- development log entry = 时间线节点
- witness = evidence 节点

## Writeback Rule

- `evidence` 阶段必须把真实 witness 绑定回对应结构节点。
- `OS_graph` 不是只解释代码；它同时解释文档与代码。
- 文档节点与代码节点的绑定依据是“语义覆盖单元”，不是机械文件 1:1。
- graph 写回既要支持机械锚点关系，也要支持人类可视化连线。
