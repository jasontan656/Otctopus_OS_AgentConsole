---
name: Meta-Agent-Browser
description: Manual-invoke browser automation skill for the external agent-browser tool, with CLI-first runtime contracts, fallback routing, and governed output defaults.
allowed-tools: Bash(agent-browser:*), Bash(./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py:*)
metadata:
  doc_structure:
    doc_id: meta_agent_browser.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Meta-Agent-Browser skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
---

# Meta-Agent-Browser

## 1. 工具入口
- 本技能运行时统一入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py contract --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py directive --topic <topic> --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py paths --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py dependencies --json`
- 可选的 skill-local wrapper：
  - `scripts/agent-browser-runtime-guard.sh`
  - `scripts/agent-browser-stable.sh`
- 模型读取运行时合同、路由、输出规则时，必须优先走 CLI JSON；`SKILL.md` 只做门面。

## 2. 适用域
- 适用于：用户显式要求 `$Meta-Agent-Browser`，或明确要求 browser automation 且需要走本 skill 的 agent-browser 包装层。
- 适用于：agent-browser 正常路径、fallback routing、Windows headed bridge 补充指引、skill-local 模板与默认产物治理。
- 不适用于：修改或安装全局 `agent-browser`、修补上游 npm 包、把其他浏览器 workflow family 的 domain policy 吞进本 skill。

## 3. 必读顺序
1. 先执行 `./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py contract --json`。
2. 按任务意图读取 directive：
   - 正常运行入口：`./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py directive --topic runtime-entry --json`
   - runtime 选择与 fallback：`./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py directive --topic fallback-routing --json`
   - 截图、PDF、auth state、trace、下载等产物：`./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py directive --topic output-governance --json`
3. 当任务涉及任何文件产物时，再执行 `./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py paths --json` 获取当前仓内解析结果。
4. 当任务涉及产品安装面、target-local 依赖安装路径或 browser asset 落点时，再执行 `./.venv_backend_skills/bin/python Skills/Meta-Agent-Browser/scripts/Cli_Toolbox.py dependencies --json`。
5. 只有当 CLI JSON 仍留下真实语义缺口时，才打开 human mirror 或 `references/browser-total-entry.md`、`references/windows-headed-bridge.md` 等补充文档。

## 4. 外部工具边界
- `agent-browser` 是外部前置工具，不属于本 skill 管辖面。
- 该前置工具的 target-local 安装与回滚应交给 Octopus OS product installer 消费 `EXTERNAL_RUNTIME_DEPENDENCIES.json` 完成。
- 本 skill 只负责：
  - 受控入口
  - skill-local wrapper
  - fallback routing
  - 默认产物落点
  - 模板与文档对齐
- 本 skill 不负责：
  - 安装 `agent-browser`
  - patch `agent-browser`
  - 管理上游包版本
  - 重写 `~/.agent-browser` 目录语义

## 5. 结构索引
```text
Meta-Agent-Browser/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── Cli_Toolbox.py
│   ├── meta-agent-browser-env.sh
│   ├── agent-browser-runtime-guard.sh
│   └── agent-browser-stable.sh
├── references/
│   ├── runtime_contracts/
│   ├── browser-total-entry.md
│   ├── windows-headed-bridge.md
│   └── ...
└── templates/
```
