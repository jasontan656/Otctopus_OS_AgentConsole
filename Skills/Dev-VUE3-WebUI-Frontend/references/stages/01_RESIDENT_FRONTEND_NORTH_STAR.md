---
doc_id: "stages.resident.frontend_north_star"
doc_type: "resident_doc"
topic: "Long-lived north-star constraints for the staged Vue3 web UI frontend skill"
anchors:
  - target: "10_STAGE_FOUNDATION.md"
    relation: "details"
    direction: "downstream"
    reason: "Foundation-stage work expands the resident north-star constraints."
  - target: "../runtime/SKILL_RUNTIME_CONTRACT.md"
    relation: "governed_by"
    direction: "upstream"
    reason: "The runtime contract defines this doc as a resident boundary."
---

# Resident Frontend North Star

## 核心角色
- 这是一个前端标准技能，不是某一个页面的临时设计稿。
- 这个技能的站点必须同时是：
  - 多治理域内容的人类可视统一工作台
  - 文档 graph 的人类可视展厅
  - code graph 的统一承载面
  - Vue3 Web UI 最佳实践样本
  - 可演化的组件与交互实验场

## 长期不变约束
- graph 是一等公民，不允许退化为二级附属功能。
- 页面既服务设计判断，也服务结构判断。
- 可复用组件、动效、响应式、运行链都必须文档先行。
- 任何局部界面都应能回收到更高层规范，而不是孤立 patch。
- 统一前端壳可以承载多个治理域，但治理域语义必须显式区分，禁止把 doc graph、code graph、runtime evidence 压成一套扁平名词。
- 内容发现应以受治理目录结构、manifest 与字段合同为准，禁止用硬编码页面清单伪装自动发现。
- AI 协作入口必须是工作台的一等面，而不是 code graph 或文档 graph 的附属按钮。
