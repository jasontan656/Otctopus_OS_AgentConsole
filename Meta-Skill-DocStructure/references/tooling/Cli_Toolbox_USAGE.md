---
doc_id: "tooling.usage.cli"
doc_type: "tooling_usage"
topic: "TypeScript CLI and viewer operations for Meta-Skill-DocStructure"
anchors:
  - target: "../runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The CLI and viewer commands operationalize the runtime contract."
  - target: "../ui/VIEWER_SERVICE_WORKFLOW.md"
    relation: "pairs_with"
    direction: "downstream"
    reason: "Service workflow complements the CLI commands."
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
- `Cli_Toolbox.preview_payload`
  - `npm run cli -- preview-payload --target <skill_root> --json`
- `Cli_Toolbox.rebuild_self_graph`
  - `npm run cli -- rebuild-self-graph --json`

## Viewer 命令
- `npm run dev`
  - 开发态实时页面，文档变化后自动刷新 payload。
- `npm run build`
  - 构建 production client。
- `npm run start`
  - 以 production 模式启动 viewer server。
- `npm run service:install`
  - 安装 user-level systemd service。

## 快速示例
```bash
cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Skill-DocStructure && npm run cli -- preview-payload --target /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Skill-DocStructure --json | sed -n '1,240p'
cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Skill-DocStructure && npm run dev | sed -n '1,40p'
cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Skill-DocStructure && npm run service:install | sed -n '1,80p'
```
