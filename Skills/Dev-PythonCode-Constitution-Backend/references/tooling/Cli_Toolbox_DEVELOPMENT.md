---
doc_id: "dev_pythoncode_constitution_backend.tooling.toolbox_development"
doc_type: "topic_atom"
topic: "Tooling development entry for the Python backend code constitution skill"
anchors:
  - target: "Cli_Toolbox_USAGE.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Usage and development docs are maintained as a pair."
  - target: "development/00_ARCHITECTURE_OVERVIEW.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Tooling development details live in the development subtree."
---

# Cli_Toolbox 开发文档（入口）

适用技能：`Dev-PythonCode-Constitution-Backend`

## 当前状态
- 当前已有一个真实 CLI：`run_python_code_lints.py`。
- 当前工具面只服务 Python 相关 lint；不再借用 `Constitution-knowledge-base` 的 lint 入口。
- 当前 lint 边界已收紧为“Python 文件 + 已确认的 Python 资产”，并移除了泛目录结构治理职责。
- 当前 lint 已扩展为“结构治理 + runtime safety”双轴：除胖文件与资产边界外，还包含 typing、subprocess、logging 三类 Python 工程安全 gate。

## 内联索引（阅读顺序）
1. 架构总览：`references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
2. 模块目录：`references/tooling/development/10_MODULE_CATALOG.yaml`
3. 分类索引：`references/tooling/development/20_CATEGORY_INDEX.md`
4. 模块文档模板：`references/tooling/development/modules/MODULE_TEMPLATE.md`
5. 变更记录：`references/tooling/development/90_CHANGELOG.md`

## 文档分类规则
- 入口文档只做导航与约束，不承载全部实现细节。
- 模块目录记录 tool alias、入口、状态与文档映射。
- 分类索引负责跨模块视图。
- 具体实现细节写入 `modules/<module_id>.md`。

## 同步维护约束（强制）
- 工具变更必须同步更新：
  - `Cli_Toolbox_USAGE.md`
  - `10_MODULE_CATALOG.yaml`
  - 对应模块文档
- 若工具会影响 facade / routing / atomic doc tree，必须同步更新 `references/routing/`、`references/governance/` 与 `references/python_rules/`。

## 版本变更记录
- 2026-03-12 初始化：创建 basic skill 骨架。
- 2026-03-12 迁移：接管 `Constitution-knowledge-base` 中的 Python 专属 lint 与胖代码治理职责。
