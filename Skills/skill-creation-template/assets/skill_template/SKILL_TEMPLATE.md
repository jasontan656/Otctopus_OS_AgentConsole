---
name: "${skill_name}"
description: ${description}
doc_id: "skill_creation_template.asset.basic_skill_template"
doc_type: "template_doc"
topic: "Basic skill facade template asset"
anchors:
  - target: "references/routing/TASK_ROUTING_TEMPLATE.md"
    relation: "implements"
    direction: "downstream"
    reason: "This asset routes to the task routing template in the current template pack."
  - target: "references/governance/SKILL_DOCSTRUCTURE_POLICY_TEMPLATE.md"
    relation: "governed_by"
    direction: "downstream"
    reason: "The template pack governs basic facades through the doc-structure policy template."
metadata:
  doc_structure:
    doc_id: "${skill_name}.entry.facade"
    doc_type: "skill_facade"
    topic: "Entry facade for ${skill_name}"
    anchors:
      - target: "references/routing/TASK_ROUTING.md"
        relation: "routes_to"
        direction: "downstream"
        reason: "The facade must route readers into the first task branch."
      - target: "references/governance/SKILL_DOCSTRUCTURE_POLICY.md"
        relation: "governed_by"
        direction: "downstream"
        reason: "Doc-structure policy is a mandatory governance branch."
---

# ${skill_name}

## 1. 技能定位
- [本文件只做门面入口，不承载深规则正文。]
- [写清本技能的唯一主轴与最小职责边界。]
- [若技能存在运行态规则，写明真实规则源来自 CLI 输出的 machine-readable contract。]

## 2. 必读顺序
1. [若有 runtime contract，先读取 runtime contract。]
2. 读取 `references/routing/TASK_ROUTING.md`。
3. 读取 `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`。
4. 再进入当前任务真正需要的 execution rules、tooling docs 或其他原子文档。

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- 治理层：
  - `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`
  - `references/governance/SKILL_EXECUTION_RULES.md`
- 工具层：
  - [本技能统一 CLI 入口或说明无专属 CLI tool]
- 运行合同层：
  - [若存在 runtime contract，写在这里]

## 4. 适用域
- 适用于：[明确本技能负责的任务类型]
- 不适用于：[明确排除域]
- [若依赖 companion skill，只写职责边界，不复制对方规则]

## 5. 执行入口
- [统一 CLI 入口命令]
- [门禁命令 / lint 命令 / contract 命令]
- [若无工具，明确说明入口即门面与固定文档]

## 6. 读取原则
- 门面只负责路由，不重新长回规则正文。
- `skill-doc-structure` 是创建与治理本技能时必须应用的显式规则。
- 若某条规则只属于单一 topic，应下沉到原子文档；不要继续堆在门面里。
- 若此 skill 属于模板或治理类 skill，可在下沉文档中使用 `技能本体 / 规则说明` 双段式，但门面仍应保持极简。

## 7. 结构索引
```text
<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
├── references/
│   ├── governance/
│   ├── routing/
│   ├── runtime/        # optional
│   └── tooling/
├── assets/
└── tests/
```
