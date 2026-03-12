---
doc_id: "ui.dev.docs.panels.catalog"
doc_type: "topic_atom"
topic: "Panel catalog for the future showroom canvas"
anchors:
  - target: "00_PANEL_CATALOG_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This panel catalog belongs to the panel branch."
  - target: "../../../frontend_dev_contracts/showroom_runtime/VIEWER_STACK_AND_REUSE.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The panel catalog must align with the generic showroom stack contract."
  - target: "20_DOCUMENT_GRAPH_PANEL_PROTOCOL.md"
    relation: "details"
    direction: "downstream"
    reason: "Document graph panels need a narrower protocol than the top-level panel catalog."
  - target: "30_CODEGRAPH_PANEL_PROTOCOL.md"
    relation: "details"
    direction: "downstream"
    reason: "Code graph panels need a narrower protocol than the top-level panel catalog."
---

# Showroom Panel Catalog

## Required Panels
- `Overview Panel`
  - Explains what the showroom is and what the user can open next.
- `Governance Domain Panel`
  - Shows the discovered governance domains and their current availability.
- `Document Graph Panel`
  - Exposes the active document package graph as a first-class surface.
- `Document Library Panel`
  - Lists available governed doc packs, folders, and docs and allows panel-driven navigation.
- `Document Reader Panel`
  - Reads the currently selected doc, follows anchors, and supports inline jump-outs.
- `Repo Library Panel`
  - Lists indexed repositories and their code graph availability.
- `Code Graph Panel`
  - Exposes the active repo graph, cluster/module entry points, and graph-native focus controls.
- `Code Reference Panel`
  - Shows symbol/file references, repo details, and graph-selected metadata.
- `AI Workspace Panel`
  - Hosts AI collaboration against the current workspace selection and its locator handles.
- `Runtime Intent Panel`
  - Explains the future runtime boundary and current docs-first status.

## Catalog Rules
- Each panel must have a clear reason to exist.
- Panels are not permanent columns; they are canvas-loaded surfaces.
- New panels must be introduced through menu actions, not hidden fixed layout slots.
- Domain-specific panels may share layout primitives, but they must keep their own titles, legends, and semantic affordances.
