---
name: "meta-skill-docstructure"
description: "规范 skills 内部文档组织的治理技能。用于在 skill folder 内建立单 topic 原子文档、frontmatter 锚点规范、anchor graph JSON、lint 脚本与文档拆分工作流。仅在组织或校验 skill 内部文档时使用，不用于普通 repo 文档或 code graph。"
metadata:
  short-description: "治理 skills 内部文档组织、锚点图和 lint 工作流"
  doc_structure:
    doc_id: "skill.entry.facade"
    doc_type: "skill_facade"
    topic: "Meta-Skill-DocStructure entry facade and routing contract"
    anchors:
      - target: "references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
        relation: "governed_by"
        direction: "downstream"
        reason: "Detailed runtime rules and workflow live in the runtime contract."
      - target: "references/tooling/Cli_Toolbox_USAGE.md"
        relation: "executed_via"
        direction: "downstream"
        reason: "Operational commands are documented in the usage guide."
---

# Meta-Skill-DocStructure

## 1. 应用域
- 只服务 `skills` 内部文档组织。
- 目标对象是 skill folder 内的 `SKILL.md`、runtime 文档、tooling 文档、模板文档与其他内部说明文档。
- 不处理任意 repo 普通文档，不处理代码依赖图，不替代 `Meta-code-graph-base`。

## 2. 核心目标
- 让 skill 内部文档尽可能原子化，每份文档只承载一个稳定 topic。
- 要求每份 markdown 文档至少声明一个 anchor，但不要求 all-to-all 全连接。
- 允许跳文档、跳层、一个文档关联多个文档；主张形成对模型更友好的 spiderweb graph。
- 用 frontmatter、lint、JSON graph 与 split matrix 把这个规范机械化，而不是只停留在口头方法论。

## 3. 内部思考链
1. 锁定目标 skill root，确认只在 skill 边界内工作。
2. 清点全部 markdown 文档，读取 frontmatter anchor 合同。
3. 判断每份文档是否 single-topic；若 topic 漂移，优先拆分。
4. 用 `anchor_query_matrix.json` 检查“是否该拆分”的关键词信号。
5. 运行 lint，确认每份文档至少一个 anchor，且 target 合法。
6. 构建或重建 anchor graph JSON，给后续脚本和模型机械消费。

## 4. 工作流
1. 先读取 runtime contract：
   - `python3 scripts/Cli_Toolbox.py runtime-contract --json`
2. 先 lint，再改文档：
   - `python3 scripts/Cli_Toolbox.py lint-doc-anchors --target <skill_root> --json`
3. 需要看图时构建 graph：
   - `python3 scripts/Cli_Toolbox.py build-anchor-graph --target <skill_root> --json`
4. 修改本技能自身文档后，必须回写：
   - `python3 scripts/Cli_Toolbox.py rebuild-self-graph --json`

## 5. 工具与资产
- CLI 入口：`scripts/Cli_Toolbox.py`
- runtime contract：
  - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.json`
  - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md`
- frontmatter 模板：`assets/templates/DOC_FRONTMATTER_TEMPLATE.yaml`
- 原子文档模板：`assets/templates/ATOMIC_DOC_TEMPLATE.md`
- 机械矩阵：`assets/runtime/anchor_query_matrix.json`
- 自身 graph：`assets/runtime/self_anchor_graph.json`

## 6. 读取顺序
1. `SKILL.md`
2. `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md`
3. `references/tooling/Cli_Toolbox_USAGE.md`
4. 需要实现细节时，再读 `references/tooling/development/*`

## 7. Guardrails
- 任何 markdown 文档都不得做成“零锚点孤岛”。
- 至少一个 anchor 的意思是：它必须能指向一个真实上下游或横向补充文档；不是要求与所有文档互连。
- anchor 关系允许跨层与跨段，但必须保持 target 可解析、relation 可判定、reason 可解释。
- 若 lint 给出 atomicity warning，默认先考虑拆分，而不是继续扩写原文档。
