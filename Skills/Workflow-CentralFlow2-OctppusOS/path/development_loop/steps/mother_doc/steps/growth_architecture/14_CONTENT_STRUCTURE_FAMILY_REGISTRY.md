---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.growth_architecture.content_structure_family_registry
doc_type: topic_atom
topic: Mother doc content structure family registry
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: 注册完内容结构家族后，再进入实际生长决策。
---

# 文档内容结构家族注册表

当前允许的 `content_family`：
- `root_index_auto`
- `overview_narrative`
- `overview_mapping`
- `branch_overview`
- `layer_taxonomy_root`
- `layer_item_doc`
- `container_item_doc`
- `contract_spec_doc`

使用规则：
- `content_family` 负责约束“这一类文档怎么写”，它与 `display_layer`、`doc_kind` 正交。
- 同一 `content_family` 的文档必须共享稳定的结构骨架；模型应主动把同类内容写得更像同一种工件，而不是今天一个标题集、明天另一套标题集。
- 若需要新增新的 `content_family`，模型应主动先回答：
  - 它专门承载什么语义？
  - 为什么现有内容结构家族不足以承载？
  - 它是否能被同类文档复用？
- 一旦注册新的 `content_family`，它就属于固定框架的一部分；后续同类文档必须继续复用，不得平行再造一套。

## 当前结构骨架
- `root_index_auto`
  - `## 当前职责`
  - `## 自动目录结构图`
  - `## 自动目录清单`
  - `## 根入口约束`
- `overview_narrative`
  - `## 来源`
  - `## 当前节点职责`
  - `## 当前内容`
- `overview_mapping`
  - `## 来源`
  - `## 当前节点职责`
  - `## 当前内容`
- `branch_overview`
  - `## 来源`
  - `## 当前节点职责`
  - `## 当前内容`
  - `## 当前延伸规则`
- `layer_taxonomy_root`
  - `## 来源`
  - `## 当前节点职责`
  - `## 当前内容`
  - `## 当前延伸规则`
- `layer_item_doc`
  - `## 来源`
  - `## 当前节点职责`
  - `## 当前内容`
  - `## 当前延伸边界`
- `container_item_doc`
  - `## 来源`
  - `## 当前节点职责`
  - `## 当前内容`
  - `## 当前承载边界`
- `contract_spec_doc`
  - `## 来源`
  - `## 当前节点职责`
  - `## 当前规则`
  - `## 当前配置`

## 主动生长说明
- 靠近根入口的 `content_family` 应优先服务人类阅读、框架理解和高层叙事。
- 越向外延伸的 `content_family`，越应主动服务模型执行、参数落盘、规则钉死与原子决策。
- 模型在中后层文档里可以大胆采用自己最擅长的原子化写法，但前提是同层同类文档必须继续共享同一个 `content_family`。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
