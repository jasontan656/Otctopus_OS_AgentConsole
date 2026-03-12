---
name: "Meta-code-graph-base"
description: "维护本地代码图谱底座：统一建图、查图、影响面分析、变更检测、资源视图与本地 wiki/map bundle 生成。运行产物固定落在 OctuposOS_Runtime_Backend/code_graph_runtime。"
---

# Meta-code-graph-base

## Overview

这个技能负责维护一个可持续更新的本地代码图谱系统，供章鱼OS与其他技能在施工前后读取。
它负责代码图谱的数据面、资源面与分析面，不再承担最终前端界面的宿主角色。

它覆盖的能力面：
- 仓库扫描与索引持久化
- 多语言静态解析
- 图谱建模与查询
- 影响面分析
- 变更检测
- 搜索增强
- 资源视图
- 本地 wiki / map bundle 生成

运行产物固定落在：
- `<root>/OctuposOS_Runtime_Backend/code_graph_runtime`

当前前端承载关系：
- 最终 UI / workbench 由 `Dev-VUE3-WebUI-Frontend` 承载。
- 本技能提供 repo registry、resource URI、map/wiki bundle 与本地运行产物，供前端技能读取或投影。
- code graph 展示规范、panel 组织、canvas 交互与视觉合同以 `Dev-VUE3-WebUI-Frontend` 为准。

实现来源声明：
- 当前 `assets/gitnexus_core` 并非从零独立重写，而是基于 `GitNexus` 的 `gitnexus/` 核心代码迁移后做本地裁剪与补丁。
- 现阶段的 Python 入口主要是 wrapper；底层核心引擎仍以上游迁移来的 TypeScript engine 为主。
- 对外说明、仓库发布与后续治理时，必须明确 `Meta-code-graph-base` 含有来自 `GitNexus` 的迁移/修改代码，而不是把整套 code graph core 描述成纯原创实现。
- `assets/gitnexus_core` 下必须保留独立的上游许可证与 notice；仓库根说明也必须同步声明该来源边界。

## Workflow

1. 先确认目标仓库是否已经建图：
```bash
./.venv_backend_skills/bin/python Skills/Meta-code-graph-base/scripts/meta_code_graph_base.py status
```

2. 如果未建图或已过期，先分析：
```bash
./.venv_backend_skills/bin/python Skills/Meta-code-graph-base/scripts/meta_code_graph_base.py analyze /abs/repo/path
```

3. 施工前，至少使用以下能力之一：
- `query`
- `context`
- `impact`
- `resource codegraph://repo/<name>/context`

4. 施工后，至少运行：
- `detect-changes`
- 需要时生成 `wiki`
- 若任务涉及 code graph 前端承载或 viewer 规划，继续参考 `Dev-VUE3-WebUI-Frontend` 的 `ui-dev/` 与 `frontend_dev_contracts/showroom_runtime/` 文档，而不是在本技能内重复发明 UI 合同。

## Commands

统一入口：
```bash
./.venv_backend_skills/bin/python Skills/Meta-code-graph-base/scripts/meta_code_graph_base.py <subcommand> [args...]
```

核心子命令：
- `analyze`
- `status`
- `list`
- `clean`
- `query`
- `context`
- `impact`
- `detect-changes`
- `rename`
- `augment`
- `resource`
- `map`
- `wiki`
- `cypher`

## Output Contract

运行产物集中于：
- `code_graph_runtime/registry`
- `code_graph_runtime/indexes`
- `code_graph_runtime/reports`
- `code_graph_runtime/maps`
- `code_graph_runtime/wiki`
- `code_graph_runtime/snapshots`

## Guardrails

- 不向 codex 安装目录同步。
- 不生成外部安装壳、Web UI、MCP transport。
- 不接入任何额外 LLM API 或交互式 provider 配置。
- 不把图谱能力简化成只会 `impact` 的最小试用品。
- 不在本技能内部另起一套独立前端产品合同；代码图谱的最终界面由受治理的统一前端工作台承载。
- 如果某项能力仍未完整实现，要显式标明，不伪装完成。

## References

- `references/migration_map.md`
- `references/runtime_layout.md`
- `references/viewer_handoff.md`
