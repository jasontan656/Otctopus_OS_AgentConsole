---
doc_id: "runtime.contract.audit"
doc_type: "runtime_contract"
topic: "Audit version of the document-structure runtime contract"
anchors:
  - target: "../../SKILL.md"
    relation: "implements"
    direction: "upstream"
    reason: "This runtime contract is the concrete rule source behind the skill facade."
  - target: "../rules/00_RULE_SYSTEM_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The rule-system index expands how docs should be organized before anchors are written."
---

# Runtime Contract

## 合同目标
- 规范 skill 内部 markdown 文档从入口节点往下的 tree-first 组织、frontmatter 与 anchors。
- 输出可被模型和机械系统消费的 anchor graph JSON。
- 通过 TS CLI 提供 lint、split 决策注册与 self graph rebuild。
- 以三条知识轨和三条 workflow 轨组织本技能自身的知识面。

## 最小要求
- 每个 skill 必须先有入口节点。
- 主阅读路径必须先能表达为语义 tree，再允许补充 graph。
- 每个 markdown 文档至少一个 anchor。
- anchor 目标必须存在于当前 skill root 内。
- `SKILL.md` 通过 `metadata.doc_structure` 暴露入口合同。

## 节点角色
- `entry_node`：文档树入口，只负责把读者送进下一级。
- `routing_doc`：承载一个分叉轴线，把读者送入下一级子主题。
- `topic_atom`：承载单一稳定 topic，不再混入多个平级大分叉。
- `index_doc`：只做索引与导航，不承载核心规则正文。
- `example_doc`：fewshot 样例节点，用真实树形结构示范组织方式。

## 结构规则
- 先确定入口节点，再拆 `routing`，最后下沉到 `topic_atom`。
- 一个文档若同时出现多个独立语义轴线，应继续拆分。
- 横向或跨层关系只能作为 graph 补充，不能替代主路径。
- 规则轨、fewshot 轨、元信息轨应各有独立入口。
- 查询、架构组织、单文件写作三条 workflow 也应各有独立入口。

## split lint 规则
- split 候选点一旦出现，不再只作为 warning，而是默认进入阻断态。
- 阻断态意味着：当前文档必须二选一：
  - 当场拆分解决。
  - 由用户显式决策后写入 `assets/runtime/split_decision_registry.json`。
- 已登记为 `accepted` 的候选点，在同一内容 fingerprint 下不再重复阻断。
- 已登记为 `split_required` 的候选点，会持续阻断直到文档被真正拆分或重写。
