---
doc_id: skillsmanager_tooling_checkup.references_tooling_development_modules_mod_directive
doc_type: topic_atom
topic: directive 模块开发文档
---

# directive 模块开发文档

## 模块标识
- `module_id`: `directive`
- `tool_alias`: `Cli_Toolbox.directive`
- `entrypoint`: `scripts/Cli_Toolbox.py`

## 职责
- 按 `--topic` 输出具体 contract/workflow/instruction/guide payload。
- 保证模型读到的是直接 JSON 指令，而不是路径跳转提示。

## 输入输出契约
- 输入：
  - `--topic <topic>`
  - `--json`
- 输出：
  - `references/runtime_contracts/` 下与 topic 对应的 JSON payload
- 失败模式：
  - 未知 topic 时返回 `unknown_directive_topic`

## 当前 topics
- `read-audit`
- `remediation`
- `output-governance`
- `techstack-baseline`
- `tooling-entry`

## 回归检查
```bash
cd <repo-root> && python3 -m pytest tests/test_cli_toolbox.py
```
