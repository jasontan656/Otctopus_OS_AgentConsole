---
doc_id: "tooling.changelog"
doc_type: "changelog"
topic: "Change log for Dev-VUE3-WebUI-Frontend"
anchors:
  - target: "00_ARCHITECTURE_OVERVIEW.md"
    relation: "tracks_changes_to"
    direction: "upstream"
    reason: "The changelog records architecture shifts that should be read against the overview."
  - target: "../../stages/00_STAGE_INDEX.md"
    relation: "tracks_changes_to"
    direction: "upstream"
    reason: "The changelog also records stage-surface changes."
---

# Change Log

## 2026-03-11
- 由 `SkillsManager-Creation-Template` 重建为 `staged_cli_first`。
- 将原 `SkillsManager-Doc-Structure/ui-dev/` 物理迁移到本技能。
- 将本技能定位从单一 viewer 提升为：
  - Vue3 Web UI 标准技能
  - 可运行 showroom
  - graph 可视化前端样本
