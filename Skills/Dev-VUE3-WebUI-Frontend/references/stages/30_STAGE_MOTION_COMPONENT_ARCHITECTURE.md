---
doc_id: "stages.motion_component_architecture"
doc_type: "stage_doc"
topic: "Motion language, reusable component boundaries, and code organization"
anchors:
  - target: "../../frontend_dev_contracts/layers/10_LAYER_TAXONOMY.md"
    relation: "details"
    direction: "downstream"
    reason: "The fixed layer catalog shapes how containers and components should be organized."
  - target: "../../frontend_dev_contracts/containers/model/10_CONTAINER_ROLE_TAXONOMY.md"
    relation: "details"
    direction: "downstream"
    reason: "The container taxonomy defines the stable container roles that shape component architecture."
  - target: "../../frontend_dev_contracts/showroom_runtime/VIEWER_STACK_AND_REUSE.md"
    relation: "details"
    direction: "downstream"
    reason: "The frontend contract stack doc expands the runtime component and layout implications."
  - target: "../../references/tooling/development/modules/mod_stage_contract_runtime.md"
    relation: "explained_by"
    direction: "downstream"
    reason: "The stage-contract runtime module explains how this architecture is surfaced in CLI contracts."
---

# Stage Motion Component Architecture

## 关注点
- 动效必须服务信息层级，不得抢夺 graph 阅读主线。
- 页面应逐步沉淀为可复用组件，而不是继续把所有逻辑堆在单文件里。
- 代码组织需要反映：
  - layer catalog
  - app shell 与 route scene
  - 工作区容器层
  - panel 容器层
  - 数据装配层
  - 可复用组件层
  - 运行时接线层

## 目标
- 让当前 viewer 进化为前端组件资产和交互准则的展厅。
