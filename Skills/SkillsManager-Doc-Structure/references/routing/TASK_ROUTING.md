---
doc_id: skillsmanager_doc_structure.references.routing.task_routing
doc_type: topic_atom
topic: Task routing for profile-aware doc governance
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This routing guide belongs to the governed skill tree under the facade.
---

# SkillsManager-Doc-Structure Task Routing

## 任务入口
- 当任务是“这个技能属于哪种拓扑”，先运行 `inspect`。
- 当任务是“这个技能的门面、references 或 workflow 是否成立”，运行 `lint`。
- 当任务是“给我编译最小上下文”，运行 `compile-context`。

## 拓扑读取顺序
1. 先看 `metadata.skill_profile.doc_topology`。
2. 若 metadata 缺失，再看根目录实际结构：
   - `path/` 存在且有 workflow 文档：`workflow_path`
   - `references/` 存在：`referenced`
   - 否则：`inline`

## 约束
- 不再以旧 `skill_mode` 或旧 family shape 作为首要判断轴。
- `references/` 与 `workflow_path` 并列存在时，应按 `workflow_path` 解释，因为 workflow 正文本来就应与治理规则分层。
