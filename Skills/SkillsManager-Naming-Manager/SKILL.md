---
name: SkillsManager-Naming-Manager
description: 治理技能命名规范、注册模型、自然语言集合解析与重命名重组规则的技能。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: skillsmanager_naming_manager.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the SkillsManager-Naming-Manager skill
---

# SkillsManager-Naming-Manager

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能用于统一治理技能命名、注册模型、prefix/family 归类、自然语言集合调用语义与重命名重组顺序。
- 本技能只治理命名与注册语义，不替代模板创建、文档结构治理、镜像同步或 Git 推送本身。
- 当前形态为 `guide_with_tool`；门面直接暴露功能入口，深层正文沿各入口继续下沉。

### 2. 技能约束
- 进入任一功能入口后，沿当前动作闭环继续阅读：
  - `contract`
  - `execution`
  - `validation`
- 注册请求默认按 `canonical_id` 执行 upsert；命中现有条目时更新原记录，不并列新增第二条。
- `scripts/` 只承载链路编译型 CLI，不再把 CLI JSON 当成独立规则真源。
- `read-contract-context` 输出的是文档真源的编译结果；`read-path-context` 可作为等价别名保留。

### 3. 顶层常驻合同
- 全局合同直接写在本门面中，不额外外跳到 CLI 合同。
- 后续阅读只沿当前选中的功能入口继续下沉。
- 命名治理优先于局部展示偏好；改名时先改治理定义，再改消费方称呼。

## 2. 功能入口
- [命名规范]：`path/naming_policy/00_NAMING_POLICY_ENTRY.md`
  - 作用：定义 `canonical_id / display_name / prefix / family / role_tag` 的命名规则与分层边界。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry naming_policy --json`
- [注册治理]：`path/registry_governance/00_REGISTRY_GOVERNANCE_ENTRY.md`
  - 作用：定义 registry 主表模型、upsert 语义与当前技能注册快照。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry registry_governance --json`
- [调用语义]：`path/invocation_semantics/00_INVOCATION_SEMANTICS_ENTRY.md`
  - 作用：把自然语言中的单技能、family、prefix 与技能族调用收敛为稳定解析规则。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry invocation_semantics --json`
- [重命名与重组]：`path/rename_reorg/00_RENAME_REORG_ENTRY.md`
  - 作用：约束整体改名、prefix/family 调整与组织架构迁移时的固定顺序。
  - 快捷阅读：`python3 ./scripts/Cli_Toolbox.py read-contract-context --entry rename_reorg --json`

## 3. 目录结构图
```text
SkillsManager-Naming-Manager/
├── SKILL.md
├── agents/
├── path/
│   ├── naming_policy/
│   ├── registry_governance/
│   ├── invocation_semantics/
│   └── rename_reorg/
└── scripts/
```
- `path/`：本技能唯一的文档承载面，所有命名、注册、调用语义与改名重组规则都沿入口链路下沉。
- `scripts/`：链路编译 CLI 与回归测试。
- `agents/`：agent runtime config。
