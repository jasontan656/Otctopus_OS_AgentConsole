---
doc_id: skill_creation_template.asset.toolbox_module_template
doc_type: template_doc
topic: Template for a generated skill's module development doc
anchors:
- target: ../20_CATEGORY_INDEX.md
  relation: implements
  direction: upstream
  reason: Module templates are routed from the tooling category index template.
- target: ../90_CHANGELOG.md
  relation: pairs_with
  direction: lateral
  reason: Module updates should remain traceable in the changelog template.
---

# <module_id> 模块开发文档模板

## 模块标识
- `module_id`:
- `tool_alias`: `Cli_Toolbox.<tool_name>`
- `entrypoint`:

## 职责
- [模块职责]

## 输入输出契约
- 输入：
- 输出：
- 失败模式：

## 适用 tooling surface
- CLI entry:
- runtime-facing assets:
- output governance:

## 回归检查
```bash
# 填写验证命令
```
