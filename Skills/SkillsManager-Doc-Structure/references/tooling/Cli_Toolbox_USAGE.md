---
doc_id: tooling.usage.cli
doc_type: tooling_usage
topic: CLI usage for querying document architecture, validating tree shape, and rebuilding self graph
anchors:
- target: ../runtime/SKILL_DOCSTRUCTURE_RUNTIME_OVERVIEW.md
  relation: implements
  direction: upstream
  reason: The CLI is the machine-readable execution surface of the runtime contract.
- target: ../workflows/10_QUERY_FLOW.md
  relation: routes_to
  direction: downstream
  reason: The query workflow explains how to consume CLI outputs when navigating a target skill.
---

# Cli_Toolbox Usage

## 命令集合
- 先进入 skill 根目录：`cd Skills/SkillsManager-Doc-Structure`
- 再执行：
  - `npm run cli -- runtime-contract --json`
  - `npm run cli -- lint-doc-anchors --target <skill_root> --json`
  - `npm run cli -- lint-split-points --target <skill_root> --json`
  - `npm run cli -- register-split-decision --target <skill_root> --doc <doc_path> --rule <rule_id> --decision <accepted|split_required> --note <text> --json`
  - `npm run cli -- build-anchor-graph --target <skill_root> --json`
  - `npm run cli -- rebuild-self-graph --json`
- 兼容读取入口：`./.venv_backend_skills/bin/python Skills/SkillsManager-Doc-Structure/scripts/Cli_Toolbox.py contract --json`

## 使用原则
- 完整工具面由 `scripts/Cli_Toolbox.ts` 提供；上面的 Python wrapper 只负责 `contract --json`。
- 查询目标 skill 时，先判断要进入规则轨、fewshot 轨还是元信息轨，再跑 CLI JSON。
- 设计或改写文档树时，先读规则轨与 workflow 轨，再跑 CLI JSON。
- `lint-doc-anchors` 负责验证基础 metadata 与 anchor 约束。
- `lint-split-points` 命中后，默认视为阻断，不再只是 warning。
- 若用户明确决定当前文档暂不拆分，使用 `register-split-decision` 写入 registry。
- graph 相关结论优先来自 CLI JSON，不直接从 markdown 规则推断。
- `rebuild-self-graph` 负责把当前 skill 的 graph 回写到 `assets/runtime/self_anchor_graph.json`。
