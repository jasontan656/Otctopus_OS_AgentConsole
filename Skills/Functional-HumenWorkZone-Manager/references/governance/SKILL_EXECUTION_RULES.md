---
doc_id: functional_humenworkzone_manager.governance.execution_rules
doc_type: topic_atom
topic: Execution rules for Human_Work_Zone management tasks
anchors:
- target: SKILL_DOCSTRUCTURE_POLICY.md
  relation: pairs_with
  direction: lateral
  reason: Execution rules and doc-structure policy should stay aligned.
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends Human_Work_Zone tasks here for concrete rules.
---

# Skill Execution Rules

## 本地目的
- 本文承载 `Human_Work_Zone` 的最小执行规则，不扩写其他目录治理。

## 当前边界
- 当前只治理 `/home/jasontan656/AI_Projects/Human_Work_Zone`。
- 当前先把“使用这个技能”解释为：把任务范围固定到该目录，再执行收纳、整理、归类或归位。

## 局部规则
- 若用户明确点名 `Functional-HumenWorkZone-Manager`，默认不要越过 `Human_Work_Zone` 去操作其他目录。
- 若用户只是说“整理一下这个文件夹”，默认这里的“这个文件夹”就是 `Human_Work_Zone`。
- 当前阶段先不强行内置复杂分类法；具体收纳标准以后再补原子文档。

## 例外与门禁
- 若用户要求的动作明显超出 `Human_Work_Zone`，应先显式指出范围已经越界。
- 若后续新增专属脚本、清单或规则文档，必须同步更新门面与 routing。
