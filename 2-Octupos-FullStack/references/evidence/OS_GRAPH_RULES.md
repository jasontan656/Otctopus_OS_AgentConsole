# OS Graph Rules

适用阶段：`evidence`

## Core Definition

- `OS_graph` 是 `document graph + code graph + evidence graph` 的统一合同层。

## Node Equivalence

- 目录 = 结构节点
- `README.md` = 当前层用途节点
- `agents.md` = 当前层导航节点
- `<folder_name>.md` = 当前目录自身实体节点
- 代码模块 = 实现节点
- helper = helper 节点
- witness = evidence 节点

## Writeback Rule

- `evidence` 阶段必须把真实 witness 绑定回对应结构节点。
- `OS_graph` 不是只解释代码；它同时解释文档与代码。
