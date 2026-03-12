# Viewer Handoff

## Purpose

This skill owns the local code graph runtime artifacts and query surface.
It does not own the final viewer shell anymore.

The governed frontend host is:
- `Skills/Dev-VUE3-WebUI-Frontend`

## Handoff Model

- `Meta-code-graph-base` provides:
  - indexed repository registry
  - `codegraph://` resource handles
  - repo maps
  - local wiki bundles
  - impact / query / context / detect-changes output
- `Dev-VUE3-WebUI-Frontend` provides:
  - app shell
  - menu / canvas / panel organization
  - domain-aware viewer projection
  - code graph visual presentation
  - AI workbench entry

## UI Planning Rule

When the task concerns code graph UI, do not define a second independent viewer contract here.
Read and update the frontend skill's showroom/workbench docs instead, then consume this skill's runtime artifacts from that frontend shell.
