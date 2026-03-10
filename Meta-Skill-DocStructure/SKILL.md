---
name: "Meta-Skill-DocStructure"
description: "治理 skills 内部文档组织、单 topic 原子文档与锚点图谱的技能。"
metadata:
  doc_structure:
    doc_id: "skill.entry.facade"
    doc_type: "skill_facade"
    topic: "Entry facade for the document-structure governance skill"
    anchors:
      - target: "references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
        relation: "governed_by"
        direction: "downstream"
        reason: "The runtime contract defines the document-structure rules and graph constraints."
      - target: "references/methodology/SEMANTIC_ROUTING_TREE.md"
        relation: "routes_to"
        direction: "downstream"
        reason: "The semantic routing tree doc explains how to split docs into facade, branch, and atomic nodes."
---

# Meta-Skill-DocStructure

## 1. 定位
- 本文件只做门面入口，不承载规则正文。
- 本技能只负责 skill 内部 markdown 文档的原子化、锚点化、树状路由化与 graph 化治理。
- 本技能只承载文档结构方法论本体，不承载其他扩展职责。

## 2. 必读顺序
1. 先读取运行合同：
   - `npm run cli -- runtime-contract --json`
2. 再读取语义拆分方法论：
   - `references/methodology/SEMANTIC_ROUTING_TREE.md`
3. 再读取 CLI 用法与开发文档：
   - `references/tooling/Cli_Toolbox_USAGE.md`
   - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`
4. 若任务涉及模板与 frontmatter，读取：
   - `assets/templates/ATOMIC_DOC_TEMPLATE.md`

## 3. 分类入口
- 运行合同层：
  - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md`
- 方法论层：
  - `references/methodology/SEMANTIC_ROUTING_TREE.md`
- 工具层：
  - `scripts/Cli_Toolbox.ts`
- 模板层：
  - `assets/templates/ATOMIC_DOC_TEMPLATE.md`
- 工具开发层：
  - `references/tooling/development/`

## 4. 适用域
- 适用于：skills 内 markdown 语义树拆分、门面文档设计、分叉节点设计、单 topic 原子文档、frontmatter anchors、graph JSON、文档 lint、self graph 重建。
- 不适用于：任何非文档结构治理任务。

## 5. 执行入口
- `npm run cli -- runtime-contract --json`
- `npm run cli -- lint-split-points --json`
- `npm run cli -- register-split-decision --target <skill_root> --doc <doc_path> --rule <rule_id> --decision <accepted|split_required> --note <text> --json`
- `npm run cli -- build-anchor-graph --json`
- `npm run cli -- rebuild-self-graph --json`

## 6. 读取原则
- `SKILL.md` 只负责路由。
- 文档结构规则以 CLI JSON 与下沉合同为准。
- 文档结构应先形成清晰 tree，再用 anchors 把必要的跨层关系织成 graph。
- 若文档承担多个 topic 或多个独立分叉轴线，应优先拆分而不是堆补丁。
- 模型应从门面 -> 分叉节点 -> 主题原子节点逐层收敛读取，不默认通读整个 skill。

## 7. 结构索引
```text
Meta-Skill-DocStructure/
├── SKILL.md
├── agents/
├── assets/
├── references/
│   ├── methodology/
│   ├── runtime/
│   └── tooling/
├── scripts/
├── src/
└── tests/
```
