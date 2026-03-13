---
doc_id: dev_pythoncode_constitution.tooling.module_template
doc_type: topic_atom
topic: Template for future tooling modules in the Python code constitution skill
anchors:
- target: ../20_CATEGORY_INDEX.md
  relation: implements
  direction: upstream
  reason: Future module docs are routed from the tooling category index.
- target: ../90_CHANGELOG.md
  relation: pairs_with
  direction: lateral
  reason: Module changes should remain traceable in the changelog.
---

# 模块文档模板

## 模块标识
- `module_id`:
- `tool_alias`: `Cli_Toolbox.<tool_name>`
- `entrypoint`:

## 职责
- [只写真实存在模块的职责，不创建占位模块]

## 输入输出契约
- 输入：
- 输出：
- 失败模式：

## profile 适配
- `basic`:
- `staged_cli_first`:

## 回归检查
```bash
# 在新增真实模块后填写验证命令
```
