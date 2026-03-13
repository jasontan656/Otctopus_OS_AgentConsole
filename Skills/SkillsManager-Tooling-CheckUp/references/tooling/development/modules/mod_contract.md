---
doc_id: skillsmanager_tooling_checkup.references_tooling_development_modules_mod_contract
doc_type: topic_atom
topic: contract 模块开发文档
anchors:
- target: ../../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# contract 模块开发文档

## 模块标识
- `module_id`: `contract`
- `tool_alias`: `Cli_Toolbox.contract`
- `entrypoint`: `scripts/Cli_Toolbox.py`

## 职责
- 输出 `SkillsManager-Tooling-CheckUp` 的 runtime contract JSON。
- 作为模型进入本技能时的第一跳。

## 输入输出契约
- 输入：
  - `--json`
- 输出：
  - `references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json` 的 payload
- 失败模式：
  - 合同文件缺失或非法 JSON 时直接失败

## 回归检查
```bash
cd <repo-root> && python3 -m pytest tests/test_cli_toolbox.py
```
