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
    - target: ./path/primary_flow/21_TARGET_SHAPE.md
      relation: routes_to
      direction: downstream
      reason: target-shape checking is a top-level function entry.
    - target: ./path/primary_flow/22_PATH_CHAINING.md
      relation: routes_to
      direction: downstream
      reason: path-chaining checking is a top-level function entry.
    - target: ./path/primary_flow/23_DOC_WRITING.md
      relation: routes_to
      direction: downstream
      reason: doc-role checking is a top-level function entry.
    - target: ./path/primary_flow/24_ANCHOR_LINT.md
      relation: routes_to
      direction: downstream
      reason: anchor checking is a top-level function entry.
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
- 后续阅读只沿当前选中的治理功能入口继续下沉。

## 2. 功能入口
- [目标形态检查]：`path/primary_flow/21_TARGET_SHAPE.md`
  - 作用：判断目标技能属于哪种形态，以及该形态的根组织是否成立。
- [链路衔接检查]：`path/primary_flow/22_PATH_CHAINING.md`
  - 作用：检查门面到各层节点的下一跳是否按阅读顺序逐级下沉。
- [文档职责检查]：`path/primary_flow/23_DOC_WRITING.md`
  - 作用：检查不同节点是否承担了正确职责，没有越层或回流。
- [锚点检查]：`path/primary_flow/24_ANCHOR_LINT.md`
  - 作用：检查 anchors 是否只连接必要关系，没有替代物理结构。

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
