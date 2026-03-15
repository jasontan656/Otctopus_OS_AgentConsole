---
name: SkillsManager-Doc-Structure
description: 治理技能内部文档组织方式、链路衔接方式与 reading-chain lint 的技能。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: skillsmanager_doc_structure.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Doc-Structure skill
    reading_chain:
    - key: target_shape
      target: ./path/primary_flow/21_TARGET_SHAPE.md
      hop: entry
      reason: target-shape checking is a top-level function entry.
    - key: path_chaining
      target: ./path/primary_flow/22_PATH_CHAINING.md
      hop: entry
      reason: path-chaining checking is a top-level function entry.
    - key: doc_writing
      target: ./path/primary_flow/23_DOC_WRITING.md
      hop: entry
      reason: doc-role checking is a top-level function entry.
    - key: reading_chain_lint
      target: ./path/primary_flow/24_READING_CHAIN_LINT.md
      hop: entry
      reason: reading-chain checking is a top-level function entry.
---

# SkillsManager-Doc-Structure

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能用于检查目标技能的文档组织是否成立。
- 检查范围包括：根目录形态、功能入口到下游节点的衔接、frontmatter 中 `reading_chain` 的下一跳语义，以及链路是否可编译。
- 这一步只审文档结构和阅读顺序，不替目标技能编写业务正文。

### 2. 技能约束
- 先判定目标技能属于哪种形态，再进入对应检查链路。
- `reading_chain` 必须表达模型下一步该读什么，以及 CLI 下一步该编译什么。
- CLI 只做硬结构 lint：根结构、线性/复合线性、下一跳存在性、reading-chain 可解析性与链路编译结果。
- `read-contract-context` 是当前技能自身的快捷合同编译入口；`read-path-context` 可作为等价别名保留。
- “每一层具体写得对不对”属于模型语义审查，不由 CLI 把正文模板硬编码死。

### 3. 顶层常驻合同
- 全局合同直接写在本门面中，不额外外跳到 CLI 合同。
- 后续阅读只沿当前选中的治理功能入口继续下沉。

## 2. 功能入口
- [目标形态检查]：`path/primary_flow/21_TARGET_SHAPE.md`
  - 作用：判断目标技能属于哪种形态，以及该形态的根组织是否成立。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry target_shape --selection <branch_keys> --json`
- [链路衔接检查]：`path/primary_flow/22_PATH_CHAINING.md`
  - 作用：检查门面到各层节点的下一跳是否按阅读顺序逐级下沉。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry path_chaining --selection <branch_keys> --json`
- [文档职责检查]：`path/primary_flow/23_DOC_WRITING.md`
  - 作用：检查不同节点是否承担了正确职责，没有越层或回流。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry doc_writing --selection <branch_keys> --json`
- [reading-chain 检查]：`path/primary_flow/24_READING_CHAIN_LINT.md`
  - 作用：检查 reading-chain 是否只表达阅读顺序、是否能正确编译整条上下文链路。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry reading_chain_lint --json`

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
