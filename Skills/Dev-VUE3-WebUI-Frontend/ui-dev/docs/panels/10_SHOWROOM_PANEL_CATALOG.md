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
---

# Showroom Panel Catalog

## Required Panels
- `Overview Panel`
  - Explains what the showroom is and what the user can open next.
- `Graph Panel`
  - Exposes the document graph as a first-class surface.
- `Document Library Panel`
  - Lists available docs and allows panel-driven navigation.
- `Document Reader Panel`
  - Reads the currently selected doc and follows anchors.
- `Runtime Intent Panel`
  - Explains the future runtime boundary and current docs-first status.

## Catalog Rules
- Each panel must have a clear reason to exist.
- Panels are not permanent columns; they are canvas-loaded surfaces.
- New panels must be introduced through menu actions, not hidden fixed layout slots.
