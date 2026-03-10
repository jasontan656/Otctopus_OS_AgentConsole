---
doc_id: "runtime.contract.audit"
doc_type: "runtime_contract"
topic: "Audit version of the document-structure runtime contract"
anchors:
  - target: "../../SKILL.md"
    relation: "implements"
    direction: "upstream"
    reason: "This runtime contract is the concrete rule source behind the skill facade."
  - target: "../methodology/SEMANTIC_ROUTING_TREE.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The semantic routing tree doc expands how docs should be split before anchors are written."
---

# Runtime Contract

## 合同目标
- 规范 skill 内部 markdown 文档的语义树拆分与 frontmatter anchors。
- 输出可被模型和机械系统消费的 anchor graph JSON。
- 通过 TS CLI 提供 lint 与 self graph rebuild。

## 最小要求
- 每个 skill 必须先有门面文档。
- 主阅读路径必须先能表达为语义 tree，再允许补充 graph。
- 每个 markdown 文档至少一个 anchor。
- anchor 目标必须存在于当前 skill root 内。
- `SKILL.md` 通过 `metadata.doc_structure` 暴露门面合同。

## 节点角色
- `skill_facade`：顶层门面，只做最小说明与路由。
- `routing_doc`：承载一个分叉轴线，把读者送入下一级子主题。
- `topic_atom`：承载单一稳定 topic，不再混入多个平级大分叉。
- `index_doc`：只做索引与导航，不承载核心规则正文。

## 结构规则
- 先拆 `facade`，再拆 `routing`，最后下沉到 `topic_atom`。
- 一个文档若同时出现多个独立语义轴线，应继续拆分。
- 横向或跨层关系只能作为 graph 补充，不能替代主路径。
