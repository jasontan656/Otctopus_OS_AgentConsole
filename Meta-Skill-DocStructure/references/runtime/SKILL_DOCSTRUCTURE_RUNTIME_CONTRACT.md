---
doc_id: "runtime.contract.audit"
doc_type: "runtime_contract"
topic: "Audit version of the document-structure runtime contract"
anchors:
  - target: "../../SKILL.md"
    relation: "implements"
    direction: "upstream"
    reason: "This runtime contract is the concrete rule source behind the skill facade."
  - target: "../tooling/Cli_Toolbox_USAGE.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The CLI usage doc explains how to consume the runtime contract."
---

# Runtime Contract

## 合同目标
- 规范 skill 内部 markdown 文档的 frontmatter anchors。
- 输出可被模型和机械系统消费的 anchor graph JSON。
- 通过 TS CLI 提供 lint 与 self graph rebuild。

## 最小要求
- 每个 markdown 文档至少一个 anchor。
- anchor 目标必须存在于当前 skill root 内。
- `SKILL.md` 通过 `metadata.doc_structure` 暴露门面合同。
