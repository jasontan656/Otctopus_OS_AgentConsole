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
- 当前已经内置第二个稳定子域：备份管理与长期备份清单维护。
- 当前已经内置第三个稳定子域：开源项目分析与长期分析报告归档。
- 当前已经内置第四个稳定子域：书籍与阅读物管理、统一命名与 README 导航。
- 当前已经内置第五个稳定子域：临时项目管理与待清理项目清单维护。
- 当前已经内置第六个稳定子域：公司&文档集中收纳与公司清单 README 维护。
- 当前已经内置第七个稳定子域：外部调研报告集中收纳、重命名与总清单 README 维护。
- 当任务涉及把开源项目拉回本地、给开源项目落位、补 inventory 或统一命名时，必须进入下沉原子文档，不在门面即兴裁决。
- 当任务涉及“把某个文件夹备份一下”时，必须进入备份管理分支，按固定命名复制到备份目录，并同步更新备份 README。
- 当任务涉及“问某个开源项目的问题并沉淀答案”时，必须进入开源项目分析分支，按项目归档、记录问题上下文、结论和证据。
- 当任务涉及书籍、阅读资料、读书笔记或网页阅读物的收纳时，必须进入书籍分支，按统一命名规则整理并维护导航 README。
- 当任务涉及一次性小项目、短期试验项目或暂不确定是否长期保留的项目目录时，必须进入临时项目分支，按集中区规则收纳并维护项目清单 README。
- 当任务涉及公司资料、公司文档、公司图片视频或以公司名命名的一整批目录时，必须进入公司&文档分支，按集中区规则收纳并维护公司清单 README。
- 当任务涉及从外部收集回来的调研报告、资料包、AI 整理报告或证据附件时，必须进入外部调研报告分支，按内容重命名并维护总清单 README。

## 2. 必读顺序
1. 先读取 `references/routing/TASK_ROUTING.md`。
2. 再读取 `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`。
3. 再读取 `references/governance/SKILL_EXECUTION_RULES.md`。
4. 若任务涉及开源项目管理、备份管理、开源项目分析、书籍管理、临时项目管理、公司&文档管理或外部调研报告管理，再进入 `references/runtime/` 下的对应原子流程文档。

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
- 适用于：把任意待保留文件夹完整复制到备份区、按固定格式改名、并维护备份清单 README。
- 适用于：根据用户问题在开源项目里找答案，并把分析过程、结论、证据与当时上下文写成长期可追溯的项目分析报告。
- 适用于：把书籍、阅读资料、网页文章、学习笔记和阅读资料包统一迁入书籍区、按规则命名，并维护导航 README。
- 适用于：把一次性小项目、短期试验目录或待观察项目迁入临时项目区，并维护后续清理用的项目清单 README。
- 适用于：把公司资料目录迁入公司文档区、统一公司目录命名，并维护公司总清单 README。
- 适用于：把用 AI 从外部收集回来的调研报告、报告资料包或附带证据附件迁入外部调研报告区，按内容重命名并维护总清单 README。
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
