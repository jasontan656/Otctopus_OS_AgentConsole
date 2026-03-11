# Browser Total Entry

## Purpose
- 提供浏览器任务的统一总入口。
- 在 runtime 不明确时，先给出稳定主路径，再给出逐级兜底，而不是让模型在多个浏览器方法论之间来回猜。

## Default Strategy
1. Primary: `Meta-Agent-Browser` with `agent-browser`
2. Fallback-1: WSL `无头模式` browser workflow
3. Fallback-2: Windows bridge `有头模式` visual browser workflow

## Routing Rule
- 默认优先使用 `agent-browser`。
- 出现以下问题时，切换到 `无头模式`：
  - `agent-browser` runtime guard 无法恢复
  - daemon/socket 持续异常
  - 当前任务更适合 Playwright/MCP 风格的 snapshot-interact loop
- 出现以下问题时，再切换到 Windows bridge `有头模式`：
  - 需要桌面可见验证
  - 需要 Windows Edge 专属行为
  - WSL 无头路径无法稳定完成任务

## Execution Ladder
### Level 1: Agent-Browser First
- Prepare runtime:
```bash
scripts/agent-browser-runtime-guard.sh
```
- Prefer stable session wrapper:
```bash
scripts/agent-browser-stable.sh --session qa open https://example.com
scripts/agent-browser-stable.sh --session qa wait --load networkidle
scripts/agent-browser-stable.sh --session qa snapshot -i
```

### Level 2: Headless Browser Fallback
- Route to:
  - `$CODEX_HOME/skills/WorkFlow-RealState-Posting-Web/subskills/workflow-realstate-posting-web-headless/CONTRACT.md`
- Use when:
  - 需要 WSL 内稳定执行
  - `agent-browser` 失效但 headless MCP/Playwright 正常
  - 当前任务可以接受无 GUI 验证

### Level 3: Windows Headed Bridge Fallback
- Route to:
  - `references/windows-headed-bridge.md`
- Use when:
  - 需要桌面可视化验证
  - 需要 Windows Edge + `win_chrome_devtools`
  - 无头路径无法满足交互或证据要求

## Guardrails
- 不要在一开始就默认跳过 `agent-browser`。
- 只有在上一级失败、或任务特征明确不适合时，才升级到下一级。
- 切换 runtime 时，要显式说明切换原因，避免多种浏览器方法同时混跑。
- 若任务本身是房源发布类自动化，再把浏览器 runtime 路由到 `WorkFlow-RealState-Posting-Web` 的对应分支。
