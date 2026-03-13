---
doc_id: dev_pythoncode_constitution.python_rules.project_integration
doc_type: topic_atom
topic: Python project integration governance
anchors:
- target: ../governance/SKILL_EXECUTION_RULES.md
  relation: implements
  direction: upstream
  reason: The execution rules route pytest, resource-loading, and pyproject integration topics here.
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends project-integration governance work into this atom.
---

# Python Project Integration Constitution

## 在项目中起什么作用
- 约束 Python 项目的测试导入模式、包内资源读取方式、`pyproject.toml` 元数据与 CLI entrypoint 声明。
- 让测试、打包与运行时资源访问都采用 Python 官方与 PyPA 推荐路径，而不是临时脚手架写法。

## 适用范围
- 适用于：pytest 测试目录、Python package 代码、`pyproject.toml`。
- 不适用于：非 Python 项目、未声明 package 的纯脚本目录、与 Python 无关的文档资产。

## 当前强制规则

### 1. Pytest Governance
1. 当目标项目已经声明 pytest 配置时，应启用 `importlib` import mode。
2. 当测试中使用自定义 marker 时，应启用 `strict_markers` 或等价 strict 配置。
3. 本技能默认不把“没有 pytest 配置的轻量脚本目录”直接视为违规；只有进入受管 pytest 配置面后才硬校验。

### 2. Resource Loading
1. package 内部资源读取优先使用 `importlib.resources`。
2. package 模块中不要依赖 `Path(__file__)` 或 `open(__file__...)` 去拼接包内资源路径。
3. CLI 临时文件、repo 外部配置文件不属于本条默认治理对象。

### 3. Packaging And Entrypoint
1. 当项目使用 `pyproject.toml` 的 `[project]` 元数据时，应显式声明 `[build-system]`。
2. `[project]` 应声明 `requires-python`。
3. 若 package 风格项目存在 `__main__.py` 或显式 CLI 模块，应通过 `[project.scripts]` 或 `[project.gui-scripts]` 暴露入口。
4. `src layout` 是推荐实践，但当前文档阶段只作为建议，不作为硬阻断 gate。

## 当前 lint gate 映射

| gate | 负责内容 |
|---|---|
| `pytest_governance_gate` | `importlib` mode、strict markers |
| `resource_loading_gate` | `importlib.resources` 与 `__file__` 资源读取边界 |
| `packaging_entrypoint_gate` | `[build-system]`、`requires-python`、`project.scripts` |

## 设计依据
1. pytest 官方 Good Integration Practices 推荐 `--import-mode=importlib`，并建议优先使用 `src` layout。
2. Python 官方 `importlib.resources` 是包资源读取的标准入口。
3. PyPA 文档明确要求现代 Python 项目使用 `pyproject.toml` 管理 build system 与项目元数据，CLI 入口通过 `[project.scripts]` 或 `[project.gui-scripts]` 声明。

## 必须做（Do）
1. 进入 pytest 配置面后，为测试启用 `importlib` mode。
2. 若测试使用自定义 marker，启用 strict marker 校验。
3. 在 package 内部通过 `importlib.resources` 读取包资源。
4. 在 `pyproject.toml` 中声明 build system、`requires-python` 与标准入口点。

## 不要做（Don't）
1. 不要让 pytest 继续依赖 path-precedence 导入作为默认机制。
2. 不要在 package 模块中通过 `__file__` 拼装包内资源路径。
3. 不要把 Python CLI 入口藏在 ad-hoc shell wrapper 或未声明的模块约定里。

## 最小验收
1. pytest 配置已启用 `importlib` mode，且自定义 marker 不会静默拼写漂移。
2. package 内资源读取通过 `importlib.resources` 完成。
3. 使用 `[project]` 的项目都声明了 build system、`requires-python` 与标准 entrypoint。
