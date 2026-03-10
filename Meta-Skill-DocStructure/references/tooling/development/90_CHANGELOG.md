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
  - 将原来的 Python CLI 全量迁到 TypeScript。
  - 新增 `Vue3 + Vue Flow + watcher server + systemd` viewer 运行栈。
  - 将 `SKILL.md` 变成页面默认入口正文。
  - 新增 `ui-dev/` 子根目录，并把 UI 相关代码、脚本、systemd 与开发文档统一收敛进去。
  - 将 UI payload 组装、UI tests 与 UI 定位/组织文档进一步收拢到 `ui-dev/`，根技能退回普通技能骨架。
