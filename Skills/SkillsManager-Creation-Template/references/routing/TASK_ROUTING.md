---
doc_id: skill_creation_template.routing.task_routing
doc_type: routing_doc
topic: Route readers by task intent inside the skill template control plane
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This is the first routing layer under the facade.
- target: ../governance/SKILL_DOCSTRUCTURE_ENFORCEMENT.md
  relation: routes_to
  direction: downstream
  reason: Create and govern tasks must adopt doc-structure governance first.
- target: ../routing/PROFILE_ROUTING.md
  relation: routes_to
  direction: downstream
  reason: Skill-mode-sensitive tasks must continue through skill-mode routing.
- target: ../indexes/DOC_TREE.md
  relation: routes_to
  direction: downstream
  reason: Template-pack maintenance may need the full doc tree index.
---

# Task Routing

## 当前分叉轴线
- 本文只按“任务意图”分流，不处理 `skill_mode` 选择或工具细节。

## 分支一：创建新 skill
- 先读：`../governance/SKILL_DOCSTRUCTURE_ENFORCEMENT.md`
- 再读：`PROFILE_ROUTING.md`
- 然后进入：
  - `../governance/SKILL_AUTHORING_RULES.md`
  - `../governance/SKILL_ARCHITECTURE_PLAYBOOK.md`

## 分支二：治理既有 skill
- 先读：`../governance/SKILL_DOCSTRUCTURE_ENFORCEMENT.md`
- 再读：`../governance/SKILL_AUTHORING_RULES.md`
- 若涉及模板类型重构，再转入：`PROFILE_ROUTING.md`
- 若涉及模板包联动，再补：`../indexes/DOC_TREE.md`

## 分支三：维护模板包与生成器
- 先读：`../indexes/DOC_TREE.md`
- 再读：`../governance/SKILL_ARCHITECTURE_PLAYBOOK.md`
- 脚本或命令变更时，再进入 tooling docs 与模块文档。
