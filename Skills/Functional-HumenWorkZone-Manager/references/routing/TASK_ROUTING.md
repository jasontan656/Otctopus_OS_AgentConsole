---
doc_id: functional_humenworkzone_manager.routing.task_routing
doc_type: routing_doc
topic: Route readers by Human_Work_Zone management intent
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: The skill facade routes Human_Work_Zone tasks into this first routing document.
- target: ../governance/SKILL_DOCSTRUCTURE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Doc-structure policy remains the mandatory governance branch.
---

# Task Routing

## 当前分叉轴线
- 本文只按“Human_Work_Zone 管理意图”分流，不扩到整个 workspace。

## 分支一：先锁定目录范围
- 默认受管目录是 `/home/jasontan656/AI_Projects/Human_Work_Zone`。
- 先读 `../governance/SKILL_EXECUTION_RULES.md`，确认本技能当前只管理这个目录本身。

## 分支二：执行收纳或整理
- 当用户说“收纳”“整理”“归位”“归档”时，先读 `../governance/SKILL_EXECUTION_RULES.md`。
- 当前先使用最小规则集执行，不预设复杂目录法。

## 分支三：后续扩展
- 若未来补充命名规范、分类法、清单规则或专属 CLI，再从这里新增更细的下沉文档。
