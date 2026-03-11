---
doc_id: "methodology.semantic_routing_tree"
doc_type: "methodology_doc"
topic: "Tree-first routing methodology for organizing skill-internal markdown docs"
anchors:
  - target: "../runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "expands"
    direction: "upstream"
    reason: "This methodology expands the runtime contract with concrete tree rules."
  - target: "../rules/00_RULE_SYSTEM_INDEX.md"
    relation: "belongs_to"
    direction: "downstream"
    reason: "The rule-system index routes readers from this methodology into narrower rule docs."
---

# Semantic Routing Tree

## 核心心智模型
- 文档结构应先是 `tree`，再是 `graph`。
- `tree` 负责主阅读路径，让模型从上往下逐层收敛应用域。
- `graph` 负责补充横向、跨层、跨分支关系，但不能替代主路径。
- 目标不是把所有内容堆成一个“大而全文档”，而是让模型只读当前分支真正需要的最小文档集。
- 本技能治理的是“入口节点如何把读者送入文档树，以及入口之后的树形组织方式”。

## 节点角色

### 1. 入口节点 `entry`
- 入口节点负责把读者送进文档树。
- 对多数 skill 而言，`SKILL.md` 就是入口节点。
- 在本技能里，入口节点承担 `tree root + first handoff` 的结构角色。

### 2. 分叉节点 `routing`
- 每个分叉节点只承载一个分叉轴线。
- 如果一个节点同时在做“进入写规范”与“按语言继续分支”，说明还要再拆一层。

### 3. 主题原子节点 `topic_atom`
- 只承载一个稳定 topic。
- 到达原子节点后，模型应已经知道自己为何来到这里。
- 原子节点只保留局部必需规则、局部例外、局部执行约束。

### 4. 索引节点 `index`
- 只做清单、索引、导航、汇总。
- 索引节点不应承担核心规则正文。

### 5. fewshot 示例节点 `example`
- fewshot 节点不是目标技能正文，而是供模型理解 tree 组织方式的真实示例。
- 示例必须是可追踪 tree，而不是一段抽象说明。

## 语义拆分流程
1. 先判断当前文档在回答哪个问题。
2. 再列出它当前混入了多少个独立语义轴线。
3. 若只有一个轴线，继续判断是否已是单一 topic。
4. 若存在多个轴线，先拆成上层入口或分叉节点，再把每个子轴线下沉为子文档。
5. 子文档写完后，再补 anchors，把树状主路径与横向依赖补齐。

## 主路径规则
- 顶层必须先有入口节点。
- 入口节点下方优先进入分叉节点，而不是直接撒出大量叶子文档。
- 分叉节点下面可以继续分叉，也可以直接落到原子节点。
- 主路径必须让模型知道“为什么读这个节点”和“下一步往哪走”。

## graph 规则
- 所有 markdown 文档都至少要有一个 anchor。
- `upstream/downstream` 优先表达主路径。
- `lateral/cross` 用于表达横向补充、跨层依赖、复用关系。
- graph 可以像蜘蛛网，但前提是 tree 主路径已经清晰。

## 写作要求
- 入口节点写“当前从哪里进入文档树”。
- 分叉文档写“当前按什么轴线分支、有哪些子入口、各入口边界是什么”。
- 原子文档写“单一规则、单一主题、单一局部执行面”。
- 索引文档写“清单与导航”，不要回填深层规则。
- fewshot 文档写“真实树形组织结果”，不要退化成口头总结。
