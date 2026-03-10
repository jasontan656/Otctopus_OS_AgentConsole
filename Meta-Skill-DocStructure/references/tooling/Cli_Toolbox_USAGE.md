---
doc_id: "tooling.usage.cli"
doc_type: "tooling_usage"
topic: "TypeScript CLI operations for Meta-Skill-DocStructure"
anchors:
  - target: "../runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The CLI commands operationalize the runtime contract."
  - target: "../../ui-dev/UI_DEV_ENTRY.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The embedded UI tool has its own dedicated entry."
---

# Cli_Toolbox 使用文档

适用技能：`Meta-Skill-DocStructure`

## CLI 工具清单
- `Cli_Toolbox.runtime_contract`
  - `npm run cli -- runtime-contract --json`
- `Cli_Toolbox.lint_doc_anchors`
  - `npm run cli -- lint-doc-anchors --target <skill_root> --json`
- `Cli_Toolbox.build_anchor_graph`
  - `npm run cli -- build-anchor-graph --target <skill_root> --json`
- `Cli_Toolbox.rebuild_self_graph`
  - `npm run cli -- rebuild-self-graph --json`

## 内置 UI 工具入口
- `ui-dev/UI_DEV_ENTRY.md`
  - UI 相关命令、测试与开发文档都在该子根目录内维护。

## 快速示例
```bash
cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Skill-DocStructure && npm run cli -- runtime-contract --json | sed -n '1,240p'
cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Skill-DocStructure && npm run cli -- build-anchor-graph --target /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Skill-DocStructure --json | sed -n '1,240p'
```
