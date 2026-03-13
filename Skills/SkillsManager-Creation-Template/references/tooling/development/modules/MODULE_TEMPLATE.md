---
doc_id: skill_creation_template.tooling.module_template
doc_type: module_doc
topic: Template for module-level development docs in this skill
anchors:
- target: ../20_CATEGORY_INDEX.md
  relation: implements
  direction: upstream
  reason: Module docs are routed from the tooling category index.
- target: ../90_CHANGELOG.md
  relation: pairs_with
  direction: lateral
  reason: Module updates should stay traceable in the changelog.
---

# <module_id> 模块开发文档模板

## 模块标识
- `module_id`:
- `tool_alias`: `Cli_Toolbox.<tool_name>`
- `entrypoint`:

## 职责
- [模块负责什么]

## 输入输出契约
- 输入：
- 输出：
- 失败模式：

## 依赖与边界
- 依赖：
- 禁止依赖：

## 回归检查
```bash
# 在此填写最小可运行验证命令
```

## 文档同步
- 使用文档已同步：是/否
- 模块目录已同步：是/否
