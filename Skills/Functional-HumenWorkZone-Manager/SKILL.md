---
name: Functional-HumenWorkZone-Manager
description: 用于管理 Human_Work_Zone 文件夹，在用户收纳、整理或维护该目录时作为固定技能入口。
metadata:
  doc_structure:
    doc_id: Functional-HumenWorkZone-Manager.entry.facade
    doc_type: skill_facade
    topic: Entry facade for Functional-HumenWorkZone-Manager
    anchors:
    - target: references/routing/TASK_ROUTING.md
      relation: routes_to
      direction: downstream
      reason: The facade must route readers into the first task branch.
    - target: references/governance/SKILL_DOCSTRUCTURE_POLICY.md
      relation: governed_by
      direction: downstream
      reason: Doc-structure policy is a mandatory governance branch.
---

# Functional-HumenWorkZone-Manager

## 1. 技能定位
- 本文件只做门面入口，不承载深规则正文。
- 本技能的唯一主轴是：把 `/home/jasontan656/AI_Projects/Human_Work_Zone` 视为固定受管目录。
- 当你说要“用这个技能”时，默认含义就是对 `Human_Work_Zone` 做收纳、整理、归类、归位或局部维护。
- 当前已经内置一个明确子域：开源项目收纳与长期 inventory 维护。
- 当任务涉及把开源项目拉回本地、给开源项目落位、补 inventory 或统一命名时，必须进入下沉原子文档，不在门面即兴裁决。

## 2. 必读顺序
1. 先读取 `references/routing/TASK_ROUTING.md`。
2. 再读取 `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`。
3. 再读取 `references/governance/SKILL_EXECUTION_RULES.md`。
4. 若任务涉及开源项目管理，再进入 `references/runtime/` 下的对应原子流程文档。

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- 治理层：
  - `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`
  - `references/governance/SKILL_EXECUTION_RULES.md`
- 工具层：
  - 当前无专属 CLI；入口就是本门面与固定治理文档。

## 4. 适用域
- 适用于：整理 `Human_Work_Zone`、归档新资料、调整子目录、清理临时堆放内容、统一命名与保持该目录可读。
- 适用于：为 `Human_Work_Zone` 里的开源项目建立集中管理区、维护项目 inventory、规定拉取入库命名和 README 挂钩方式。
- 不适用于：越过 `Human_Work_Zone` 去治理整个 workspace，或替代其他 repo / skill 的专属目录治理。
- 若任务需要更复杂的归档策略、命名法或自动化脚本，再在本技能下继续补原子文档。

## 5. 执行入口
- 当前无专属 CLI。
- 当前入口即：`SKILL.md -> references/routing/TASK_ROUTING.md -> references/governance/SKILL_EXECUTION_RULES.md -> references/runtime/*.md`。
- 当用户明确提到使用 `Functional-HumenWorkZone-Manager` 时，默认把任务范围锁定到 `Human_Work_Zone`。

## 6. 读取原则
- 门面只负责路由，不重新长回规则正文。
- `SkillsManager-Doc-Structure` 是创建与治理本技能时必须应用的显式规则。
- 若某条规则只属于单一 topic，应下沉到原子文档；不要继续堆在门面里。
- 若此 skill 属于模板或治理类 skill，可在下沉文档中使用 `技能本体 / 规则说明` 双段式，但门面仍应保持极简。

## 7. 结构索引
```text
Functional-HumenWorkZone-Manager/
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
