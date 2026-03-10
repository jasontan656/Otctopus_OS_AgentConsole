---
doc_id: "tooling.changelog"
doc_type: "changelog"
topic: "Change log for Meta-Skill-DocStructure"
anchors:
  - target: "00_ARCHITECTURE_OVERVIEW.md"
    relation: "tracks_changes_to"
    direction: "upstream"
    reason: "Architecture is the main thing this changelog evolves with."
---

# 变更记录

- 2026-03-11
  - 将原来的通用文档 graph 技能重构为只服务 skills 内部文档组织的技能。
  - 新增 runtime contract、anchor matrix、frontmatter template、graph/lint CLI 与测试。
