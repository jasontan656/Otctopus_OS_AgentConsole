---
doc_id: skillsmanager_naming_manager.references_registry_policy
doc_type: topic_atom
topic: 注册合同
anchors:
- target: ../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# 注册合同

## 目标
- 为所有技能提供统一注册模型，让“这个技能属于哪个 prefix/family、能否被某句自然语言一次性调度”有稳定依据。

## 当前 registry 文件
- 当前静态主表路径：`references/skill_registry.yaml`
- 在没有本地 CLI 的前提下，这份 YAML 就是当前回合可直接消费的 registry 锚点。

## 每个技能最少应登记的字段
- `canonical_id`
- `display_name`
- `prefix`
- `family`
- `role_tag`
- `status`
  - `active`
  - `deprecated`
  - `draft`
- `trigger_summary`
  - 一句话说明它在什么场景下应被调用

## 明确不纳入 registry 的信息
- 不记录技能之间的组合或协作关系。
- 不记录历史迁移来源或旧命名映射。
- registry 只负责稳定回答：技能当前叫什么、属于哪个 prefix/family、以什么角色参与路由。

## registry 的使用方式
- registry 是逻辑主表，不一定要求某个固定文件立刻存在。
- 只要你未来要做统一命名治理，就必须把技能当成“应被注册的对象”，而不是零散目录。
- 当用户说“使用某 prefix 系列全技能”时，模型应以 registry 字段为准，而不是凭目录名猜测。

## 注册写入语义
- 注册动作默认按 `canonical_id` 执行 upsert。
- 若 registry 中已存在相同 `canonical_id`，应更新已有条目的 `display_name`、`prefix`、`family`、`role_tag`、`status` 与 `trigger_summary`，而不是重复新增第二条记录。
- 只有当 `canonical_id` 在 registry 中不存在时，才应创建新的技能登记。
- 当用户口头要求“完成注册”，但该技能已经登记时，模型应把请求解释为“完成注册更新”。

## family 与 prefix 的关系
- prefix 是第一层聚类。
- family 是 prefix 下的语义分组。
- 一个技能默认只应有一个主 prefix 和一个主 family，避免同时归属多个主族导致路由歧义。
- 若某个 family 需要被自然语言稳定点名，可使用明确的 family code，例如 `[SKILL-GOV]`。

## 状态治理
- `active`
  - 当前可被正常调用和编排。
- `deprecated`
  - 仍可能被历史上下文提及，但不应作为新任务默认入口。
- `draft`
  - 已创建但尚未应被广泛路由。

## 迁移时要改什么
- 技能目录与 frontmatter `name`
- 显示名
- prefix / family / role_tag
- 用户自然语言中常用的系列称呼
- 若有历史命名说明，允许在其他文档单独维护，但不进入本 registry 模型

## OK 定义
- 模型能明确回答一个技能属于哪个 prefix 和 family。
- 模型能判断一句自然语言是否在请求单技能、family 技能集还是 prefix 全族。
- 改命名规范时，有清楚的注册字段作为迁移锚点。
- `[SKILL-GOV]` 这类治理族群能在 registry 中被直接枚举，而不是靠目录名猜测。
