---
name: "meta-topic-anchor-graph"
description: "把大文档拆成 topic 单一的树状节点，并用父子索引、横向/纵向/跨层锚点维护可导航的文档图。用于创建、重构或治理技能文档、规范文档、计划文档与知识库，使模型能沿 domain / subdomain / topic atom 逐层收敛语义，而不是在混合大文档中跳读。"
---

# meta-topic-anchor-graph

## 1. 目标
- 把文档系统建成“树为主干、锚点成边”的 `topic anchor graph`。
- 让每个文档节点只承载一个稳定 topic，不把多个职责硬塞进同一节点。
- 优先把内容继续拆小，而不是继续扩写单个大文档；前提是路径始终清晰。
- 不预设固定层深；只定义节点角色、关系约束与扩展协议。

## 2. 必读顺序
1. 先读取 `references/topic-anchor-graph-contract.md`，确认 node、anchor、single-topic boundary 的定义。
2. 再按当前任务选模板：
   - `assets/templates/ROOT_INDEX_TEMPLATE.md`
   - `assets/templates/TOPIC_ATOM_TEMPLATE.md`
3. 真正写文档前，先显式列出：
   - 当前 topic boundary
   - 父路径
   - 必要 anchors
   - 是否需要继续拆分
4. 若任务是改已有文档，先丢弃“继续往原文追加章节”的惯性，改为按节点重分配内容。

## 3. 分类入口
- 结构合同层：
  - `references/topic-anchor-graph-contract.md`
- 模板层：
  - `assets/templates/ROOT_INDEX_TEMPLATE.md`
  - `assets/templates/TOPIC_ATOM_TEMPLATE.md`
- 预留扩展层：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`

## 4. 适用域
- 适用于：把技能文档、规则文档、计划文档、知识库或说明树重构为可导航、可拆分、可继续延展的 topic graph。
- 适用于：任何需要让模型从上位域一路收敛到碎片化原子文档的任务。
- 不适用于：代码静态分析图谱、运行时依赖图、单次短便签，或本就不需要长期扩展的临时文本。
- 不替代 `Meta-code-graph-base`；那个技能处理代码图谱，本技能处理文档语义图谱。

## 5. 执行入口
- 最小执行协议：
  - 先定义根节点与主导航路径。
  - 再把候选内容切成 topic candidates。
  - 逐个做 single-topic boundary 检查；不纯就继续拆。
  - 只把摘要留在上游，把细节压到下游原子节点。
  - sibling、依赖、前置、跨层关系一律通过 anchors 表达，不靠重复粘贴。
- 模板入口：
  - `assets/templates/ROOT_INDEX_TEMPLATE.md`
  - `assets/templates/TOPIC_ATOM_TEMPLATE.md`
- 当前版本无 CLI；若未来补工具，必须先更新 `references/tooling/` 文档再落脚本。

## 6. 读取原则
- tree 是导航主脊梁，graph 是语义关系层；不要把二者混成一个无边界大纲。
- 上游节点负责路由与裁剪，下游节点负责承载细节。
- 关系通过 anchor 明示，正文不要偷偷埋“顺口一提式”的跨主题依赖。
- 不确定该不该拆时，默认继续拆；只有当继续拆已经不能提升语义纯度时才停。
- 允许横向、纵向、跨层 anchor，但不得破坏主路径可读性。
- 任何节点一旦出现明显 topic drift，就必须拆成多个节点并回填锚点。

## 7. 结构索引
```text
meta-topic-anchor-graph/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── topic-anchor-graph-contract.md
│   └── tooling/
└── assets/
    └── templates/
        ├── ROOT_INDEX_TEMPLATE.md
        └── TOPIC_ATOM_TEMPLATE.md
```
