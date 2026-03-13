---
doc_id: "dev_telegram_constitution.governance.doc_structure_policy"
doc_type: "topic_atom"
topic: "Doc-structure policy for the Telegram interface constitution skill"
anchors:
  - target: "../routing/TASK_ROUTING.md"
    relation: "implements"
    direction: "upstream"
    reason: "Telegram task routing must pass through the doc-structure policy."
  - target: "SKILL_EXECUTION_RULES.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Doc-structure policy and execution rules are the two core governance atoms."
---

# Skill Doc-Structure Policy

## 强制声明
- `SkillsManager-Doc-Structure` 是创建与治理本技能时必须显式应用的规则。
- 若当前结构与 `facade -> routing -> topic atom` 原则冲突，优先整体重建结构，而不是局部补丁。

## 必做项
- 以 `SKILL.md` 入口为 tree root，向下至少补齐一层 routing doc。
- Telegram 深规则下沉到 `references/telegram/*.md` 单 topic 原子文档。
- 所有 markdown 文档补齐 `doc_id/doc_type/topic/anchors` frontmatter。
- 新增 topic 时优先按“能力面 / 技术栈 / 交付边界 / Mini App 合同”四类扩展，而不是回填到门面。

## 双段式约定
- 本技能不是模板 skill，不要求 `技能本体 / 规则说明` 双段式。
- 若未来出现需要双段式的局部治理文档，也不得回流到入口节点。
