---
doc_id: "skill_creation_template.governance.staged_profile_reference"
doc_type: "topic_atom"
topic: "Reference for when and how to use the staged_cli_first profile"
anchors:
  - target: "../routing/PROFILE_ROUTING.md"
    relation: "details"
    direction: "upstream"
    reason: "Profile routing directs readers here when staged_cli_first is selected."
  - target: "SKILL_AUTHORING_CONTRACT.md"
    relation: "expands"
    direction: "upstream"
    reason: "This reference specializes the authoring contract for the staged profile."
  - target: "../runtime/SKILL_RUNTIME_CONTRACT.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "The runtime contract enumerates the staged output surface."
---

# Staged Profile Reference

## 何时进入 staged_cli_first
- 目标 skill 存在明确阶段顺序，而不是单一主轴动作。
- 当前阶段的读物边界、命令边界、graph 角色需要分别暴露。
- 阶段切换需要显式 discard policy，不能把上一阶段 focus 残留到下一阶段。

## staged profile 必需结构
- entry facade：`SKILL.md`
- task routing：至少一层 routing doc
- doc-structure governance：至少一份明确声明 SkillsManager-Doc-Structure 必须应用的原子文档
- runtime contract：JSON + markdown 审计版
- stage index：`references/stages/00_STAGE_INDEX.md`
- stage system template kit：
  - `CHECKLIST.json`
  - `DOC_CONTRACT.json`
  - `COMMAND_CONTRACT.json`
  - `GRAPH_CONTRACT.json`

## 应保留的治理特征
- `SKILL.md` 只做门面，不承载阶段正文。
- top-level resident docs 极少且固定。
- 进入任一阶段前先读 checklist。
- markdown 负责导航；真实运行边界由 machine-readable contracts 暴露。
- 阶段文档与 machine-readable contracts 分离维护。

## 不应带入模板的内容
- 来源 skill 的真实项目路径。
- 项目专有阶段名、交付物名、验收语义。
- 依赖单一仓库现实的 hard-coded env 或 graph 语义。

## 作者检查清单
- 这个 skill 真需要 staged，而不是 basic 吗？
- 是否已经先建 facade/routing/tree，再去补 stage contracts？
- resident docs 是否少而清楚？
- discard policy 是否已经写进 runtime contract 和 stage docs？
- 模板资产、生成器、tooling 文档与回归是否同步？
