---
name: "Meta-code-graph-base"
description: "维护本地代码图谱底座：统一建图、查图、影响面分析、变更检测与资源视图。调用时必须显式提供 graph runtime 落点。"
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

运行产物不再有默认落点：
- 调用时必须预先设置 `META_CODE_GRAPH_RUNTIME_ROOT`
- 若未提供 runtime root，本技能直接拒绝执行
- 传入的 runtime root 就是 graph 产物根目录

当前前端承载关系：
- 最终 UI / workbench 由 `Dev-VUE3-WebUI-Frontend` 承载。
- 本技能提供 repo registry、resource URI 与本地 graph 运行产物，供前端技能读取或投影。
- code graph 展示规范、panel 组织、canvas 交互与视觉合同以 `Dev-VUE3-WebUI-Frontend` 为准。

实现来源声明：
- 当前 `assets/gitnexus_core` 并非从零独立重写，而是基于 `GitNexus` 的 `gitnexus/` 核心代码迁移后做本地裁剪与补丁。
- 当前对外调用入口以原生 TypeScript CLI 为主；运行时落点通过 `META_CODE_GRAPH_RUNTIME_ROOT` 显式注入。
- 对外说明、仓库发布与后续治理时，必须明确 `Meta-code-graph-base` 含有来自 `GitNexus` 的迁移/修改代码，而不是把整套 code graph core 描述成纯原创实现。
- `assets/gitnexus_core` 下必须保留独立的上游许可证与 notice；仓库根说明也必须同步声明该来源边界。

## Workflow

1. 先确认目标仓库是否已经建图：
```bash
cd /abs/repo/path && META_CODE_GRAPH_RUNTIME_ROOT=/abs/runtime/root node /abs/skill/root/assets/gitnexus_core/dist/cli/index.js status
```

2. 如果未建图或已过期，先分析：
```bash
META_CODE_GRAPH_RUNTIME_ROOT=/abs/runtime/root node /abs/skill/root/assets/gitnexus_core/dist/cli/index.js analyze /abs/repo/path
```

3. 施工前，至少使用以下能力之一：
- `resource codegraph://repo/<name>/context`
- `context`
- `query`
- `impact`

4. 施工后，至少运行：
- `detect-changes`
- 若任务涉及 viewer 或 debug 追踪，按需读取 `resource`
- 若任务涉及 code graph 前端承载或 viewer 规划，继续参考 `Dev-VUE3-WebUI-Frontend` 的 `ui-dev/` 与 `frontend_dev_contracts/showroom_runtime/` 文档，而不是在本技能内重复发明 UI 合同。

## Commands

统一入口：
```bash
META_CODE_GRAPH_RUNTIME_ROOT=/abs/runtime/root node /abs/skill/root/assets/gitnexus_core/dist/cli/index.js <subcommand> [args...]
```

补充约束：
- `status` 依赖当前 shell 的 `cwd` 解析目标 repo，因此应在目标仓库目录内执行。
- `query/context/impact/detect-changes/rename/cypher` 这类命令若不在目标 repo 目录执行，应显式补 `--repo <indexed_repo_name>`。
- 直接消费原生 CLI 时，先解析 `stdout`；若 `stdout` 为空，再回退解析 `stderr`。

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
- `cypher`

## Output Contract

运行产物集中于调用方提供的 runtime root：
- `<runtime-root>/registry`
- `<runtime-root>/indexes`
- `<runtime-root>/reports`
- `<runtime-root>/snapshots`

## Guardrails

- 不向 codex 安装目录同步。
- 不得偷偷回退到任何默认 runtime root；没有显式落点就直接失败。
- 不生成外部安装壳、Web UI、MCP transport。
- 不接入任何额外 LLM API 或交互式 provider 配置。
- 不把图谱能力简化成只会 `impact` 的最小试用品。
- 不在本技能内部另起一套独立前端产品合同；代码图谱的最终界面由受治理的统一前端工作台承载。
- 如果某项能力仍未完整实现，要显式标明，不伪装完成。

## References

- `references/model_consumption_contract.md`
- `references/migration_map.md`
- `references/runtime_layout.md`
- `references/viewer_handoff.md`
