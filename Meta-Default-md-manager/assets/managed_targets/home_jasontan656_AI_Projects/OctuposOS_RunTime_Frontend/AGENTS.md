# AGENTS.md - OctuposOS_RunTime_Frontend (Frontend Runtime Docs)

## 目录用途
- 本目录用于存放章鱼OS前端 runtime 任务包文档与证据。
- 允许内容：`plan.md`、`spec_3l.md`、`machine/*`、`task_evidence/*`、`trace_log.jsonl`、测试说明文档。
- 禁止内容：业务源码与可执行测试源码。

## 落盘边界（强制）
- 本目录内开发文档所描述的可执行前端代码，必须落盘到：`/home/jasontan656/AI_Projects/Octopus_CodeBase_Frontend`。
- 禁止将业务源码或可执行测试代码写入本 runtime 目录。

## 依赖与环境（强制）
- 目标 codebase 运行环境：`Node.js LTS`（非 Python venv）。
- 包管理器选择顺序：`pnpm-lock.yaml -> pnpm`，`yarn.lock -> yarn`，`package-lock.json -> npm`，无 lockfile 时默认 `npm`。
- 代码实现、依赖安装、测试执行必须在上述 Node.js 工具链环境下进行。
