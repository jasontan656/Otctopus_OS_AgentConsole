---
name: SkillsManager-Doc-Structure
description: 治理技能内部文档组织方式、链路衔接方式与 anchor lint 的技能。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: skillsmanager_doc_structure.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Doc-Structure skill
    anchors:
    - target: ./path/00_SKILL_ENTRY.md
      relation: routes_to
      direction: downstream
      reason: The facade exposes only the next-hop entry layer.
---

# SkillsManager-Doc-Structure

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能只负责一件事：治理目标技能创建完成后的文档组织形态。
- 本技能自身采用 `guide_with_tool` 的 `tool/lint` 形态。
- 本技能不负责在目标技能里创建 scaffold；它只读取目标技能的既有结构并做 lint。
- 本技能治理的是：
  - 根目录形态
  - `SKILL.md` 门面职责
  - `path/` 内逐级下沉的阅读链路
  - 各层文档的衔接关系
  - anchors 的存在性与指向有效性
  - 基于既有规则的模型语义审查工作流

### 2. 技能约束
- 根目录只允许：`SKILL.md`、`path/`、`agents/`、`scripts/`。
- 不允许继续保留：`references/`、`assets/`、`src/`、`tests/` 作为主组织轴。
- 本技能只治理“如何组织文档”，不承担目标技能业务语义的编写。
- 规则不再集中写成总则；每条规则必须跟着自己的工作步骤下沉到 `path/` 链路里。
- CLI 只做硬结构 lint：根结构、线性/复合线性、下一跳存在性、anchor 存在性。
- “每一层具体写得对不对”属于模型语义审查，不由 CLI 把正文模板硬编码死。

### 3. 顶层常驻合同
- 全局合同直接写在本门面中，不额外外跳到 CLI 合同。
- 后续阅读只沿 `path/00_SKILL_ENTRY.md` 继续下沉。

## 2. 唯一入口
- [技能主入口]：`path/00_SKILL_ENTRY.md`
  - 作用：把读者送入文档结构治理主线，按单线顺序读取根形态、链路衔接、文档职责与 anchor lint。

## 3. 目录结构图
```text
SkillsManager-Doc-Structure/
├── SKILL.md
├── agents/
├── path/
└── scripts/
```
- `path/`：本技能唯一的方法论承载面，所有合同、工作步骤和校验都沿链路下沉。
- `scripts/`：Python CLI、lint 运行时与回归测试。
- `agents/`：agent runtime config。
