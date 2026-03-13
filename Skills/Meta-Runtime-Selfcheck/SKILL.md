---
name: "Meta-Runtime-Selfcheck"
description: "Manual-invoke-only post-task runtime selfcheck. 在任务运行结束后，分析上一回合中的犹豫、工具失败、脚本失败、引导不足、模型 confused 与迷宫式流程，并输出完整痛点报告和整改方案。"
metadata:
  doc_structure:
    doc_id: "meta_runtime_selfcheck.entry.facade"
    doc_type: "skill_facade"
    topic: "Entry facade for the Meta-Runtime-Selfcheck skill"
    anchors:
      - target: "references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md"
        relation: "routes_to"
        direction: "downstream"
        reason: "The facade must send runtime execution to the CLI-first contract."
      - target: "references/runtime_contracts/DIAGNOSE_WORKFLOW_human.md"
        relation: "routes_to"
        direction: "downstream"
        reason: "Diagnosis is the default branch after reading the runtime contract."
---

# Meta-Runtime-Selfcheck

## 1. 工具入口
- 本技能运行时统一入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py runtime-contract --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic <topic> --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py paths --json`
- 真正执行诊断或修复回写时使用：
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/runtime_pain_batch.py ">" --session-scope-mode all_threads --max-results 200`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/runtime_pain_batch.py 修复 --manual-repair-applied --manual-repair-path <changed_file> --verify-cmd <verify_cmd>`
- 模型读取 runtime contract、workflow、output 规则时必须优先走 CLI JSON；`SKILL.md` 只做门面。

## 2. 适用域
- 适用于：任务或运行结束后的上一回合复盘。
- 适用于：模型犹豫、工具失败、脚本失败、引导不足、文档缺失、confused 状态与迷宫式流程。
- 不适用于：未结束的任务中途调度、自动代码修复编排、把 pain provider 协议本身当主要叙事。

## 3. 必读顺序
1. 先执行 `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py runtime-contract --json`。
2. 按任务意图读取 directive：
   - 默认诊断：`./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic diagnose-workflow --json`
   - 显式修复回写：`./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic repair-writeback --json`
   - 日志与产物治理：`./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic output-governance --json`
3. 任务涉及 runtime/result 路径时，再执行 `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py paths --json`。
4. 只有当 CLI JSON 仍留下真实语义缺口时，才打开 human mirrors。

## 4. 运行边界
- 仅手动触发：只有用户明确输入 `$Meta-Runtime-Selfcheck` 或明确点名此技能时才允许执行。
- 默认目标是输出痛点报告与完整整改方案，而不是自动落盘修复。
- `修复` 只表示“在手工改动已完成后执行验证与 resolved writeback”，不代表本技能自动替你改文件。
- 数据源来自外部 pain provider；若未提供 `CODEX_RUNTIME_PAIN_PROVIDER` 或 `--memory-runtime`，运行会返回结构化错误。

## 5. 结构索引
```text
Meta-Runtime-Selfcheck/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── Cli_Toolbox.py
│   ├── runtime_pain_batch.py
│   └── runtime_pain_*.py
├── references/
│   └── runtime_contracts/
└── tests/
```
