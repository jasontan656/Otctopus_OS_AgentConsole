---
doc_id: skillsmanager_naming_manager.path.naming_policy.execution
doc_type: topic_atom
topic: Naming policy execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validation closes the naming policy chain.
---

# 命名规范实施

## 核心字段
- `canonical_id`
  - 技能的唯一安装名与注册主键。
  - 必须遵循所在治理族群的命名合同，不能与目录名、frontmatter `name`、显式调用名分离。
  - 对技能治理系列，统一使用 `SkillsManager-*` 的 Title-Case 连字符形式。
- `display_name`
  - 面向人类展示的标题。
  - 若某技能族群要求“调用名 = 安装名 = 目录名”，则 `display_name` 应与 `canonical_id` 保持一致。
- `prefix`
  - 技能族的第一层治理前缀，用于自然语言中的“某 prefix 系列”。
- `family`
  - 某 prefix 下的语义簇，用于表达一组承担相近职责的技能。
- `role_tag`
  - 更细粒度的职责标签，用于表达该技能在其 family 中承担的角色。

## 命名分层
- 第一层是 `canonical_id`，决定安装路径与 registry 主键。
- 第二层是 `display_name`，只影响人类可读性。
- 第三层是 `prefix / family / role_tag`，负责组织与批量调用语义。

## 当前可接受的前缀示意
- `SkillsManager`
  - 专门用于技能命名、创建、文档结构、镜像同步与相关治理动作。
- `Meta`
  - Meta 层治理、思维、流程与规则技能。
- `Workflow`
  - 明确以工作流交付为主轴的技能。
- `Functional`
  - 小范围任务入口或受限功能技能。

## 不允许的情况
- 同一技能在不同地方使用多个 `canonical_id`。
- 只改 `display_name`，不重新确认 `prefix / family` 是否仍成立。
- 只凭“看起来像同类”来判断 family，而不显式登记。
- 为了临时方便不断发明新 prefix，导致命名体系膨胀。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
