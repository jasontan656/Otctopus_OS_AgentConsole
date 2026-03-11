---
name: "Meta-code-graph-base"
description: "维护本地代码图谱底座：统一建图、查图、影响面分析、变更检测、资源视图与本地 wiki/map bundle 生成。运行产物固定落在 OctuposOS_Runtime_Backend/code_graph_runtime。"
---

# Meta-code-graph-base

## Overview

这个技能负责维护一个可持续更新的本地代码图谱系统，供章鱼OS与其他技能在施工前后读取。

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
- `/home/jasontan656/AI_Projects/OctuposOS_Runtime_Backend/code_graph_runtime`

## Workflow

1. 先确认目标仓库是否已经建图：
```bash
python3 /home/jasontan656/AI_Projects/octopus-os-agent-console/Meta-code-graph-base/scripts/meta_code_graph_base.py status
```

2. 如果未建图或已过期，先分析：
```bash
python3 /home/jasontan656/AI_Projects/octopus-os-agent-console/Meta-code-graph-base/scripts/meta_code_graph_base.py analyze /abs/repo/path
```

3. 施工前，至少使用以下能力之一：
- `query`
- `context`
- `impact`
- `resource codegraph://repo/<name>/context`

4. 施工后，至少运行：
- `detect-changes`
- 需要时生成 `wiki`

## Commands

统一入口：
```bash
python3 /home/jasontan656/AI_Projects/octopus-os-agent-console/Meta-code-graph-base/scripts/meta_code_graph_base.py <subcommand> [args...]
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
- 如果某项能力仍未完整实现，要显式标明，不伪装完成。

## References

- `references/migration_map.md`
- `references/runtime_layout.md`
