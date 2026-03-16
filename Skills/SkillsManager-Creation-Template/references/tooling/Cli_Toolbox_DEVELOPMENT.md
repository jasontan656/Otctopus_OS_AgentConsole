---
doc_id: skillsmanager_creation_template.references.tooling.cli_toolbox_development
doc_type: topic_atom
topic: Development notes for SkillsManager-Creation-Template tooling
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: Tool development notes must stay synchronized with the implementation.
---

# Cli_Toolbox Development

## 模块边界
- `creation_contracts.py`
  - 读取 runtime contract、directive index 与 directive payload。
- `scaffold_models.py`
  - 定义 profile/request typed data。
- `profile_registry.py`
  - 管理支持的 profile 组合与默认推荐。
- `scaffold_renderer.py`
  - 根据 profile 渲染文件内容。
- `scaffold_writer.py`
  - 负责原子写入与覆盖策略。
- `scaffold_orchestrator.py`
  - 串联校验、渲染与写入。
- `Cli_Toolbox.py`
  - 只做参数解析与命令分发。

## 同步要求
- 只要 contract 字段、profile 组合、脚手架文件列表或 CLI 参数变动，就必须同步更新：
  - `references/runtime_contracts/`
  - `references/profiles/`
  - `references/tooling/`
  - `tests/`
