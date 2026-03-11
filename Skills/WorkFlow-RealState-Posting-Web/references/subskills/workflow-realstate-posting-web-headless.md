---
name: workflow-realstate-posting-web-headless
description: Routing reference for `无头模式`. Use this branch for WSL-based posting workflows through installed browser tools.
---

# WorkFlow-RealState-Posting-Web — Headless Branch Router

## Branch Intent
- Execute房源发布网页任务 in WSL using MCP tools without desktop GUI dependency.
- Keep Playwright CLI guidance and workflow references local to this branch.
- Use this branch as the first runtime fallback after `Meta-Agent-Browser`.

## Route Target (Hard)
- `subskills/workflow-realstate-posting-web-headless/CONTRACT.md`

## Branch Boundary
- This branch does not depend on Windows-side MCP commands.
- Do not import any headed-branch instructions during execution.
