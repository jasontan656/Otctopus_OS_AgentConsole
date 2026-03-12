---
doc_id: "ui.dev.docs.domains.discovery_protocol"
doc_type: "topic_atom"
topic: "Discovery protocol for rendering governed sources inside the workbench"
anchors:
  - target: "00_GOVERNANCE_DOMAIN_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This discovery protocol belongs to the domain branch."
  - target: "../navigation/10_MENU_NAVIGATION_MODEL.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Discovered sources must appear through the stable menu taxonomy."
  - target: "../panels/20_DOCUMENT_GRAPH_PANEL_PROTOCOL.md"
    relation: "details"
    direction: "downstream"
    reason: "Document panels are one consumer of the discovery protocol."
  - target: "../panels/30_CODEGRAPH_PANEL_PROTOCOL.md"
    relation: "details"
    direction: "downstream"
    reason: "Code graph panels are another consumer of the discovery protocol."
---

# Discovery Protocol For Rendering Governed Sources

## 输入原则
- UI 不应靠硬编码 repo/page 常量决定“有哪些内容可展示”。
- UI 应读取受治理目录结构、manifest 文件、graph/runtime 产物或明确字段合同来判断可展示对象。
- 若某个治理域的字段不完整，UI 应将其标记为 unavailable 或 incomplete，而不是 silent fail。

## 最小发现单元
- `document_graph` 域的最小发现单元应至少包含：
  - source root
  - doc inventory 或 index entry
  - graph payload 或 graph path
  - reader target
- `code_graph` 域的最小发现单元应至少包含：
  - repo name
  - repo path or repo key
  - graph resource handles
  - available views such as clusters/processes/context

## 渲染投影原则
- 统一前端消费的是 viewer projection，而不是任意域的原始落盘格式。
- projection 至少要提供：
  - `domainId`
  - `entityId`
  - `title`
  - `status`
  - `entryActions`
  - `jumpTargets`
  - `panelHints`
- 当原始域 schema 增长时，应优先扩 projection adapter，不要让 panel 直接读取陌生字段。

## 失败表达
- 发现失败应明确分成：
  - missing source
  - invalid contract
  - stale runtime artifact
  - unsupported domain
- UI 必须把失败原因显示给人和 AI，而不是只把入口隐藏掉。
