---
name: "Meta-Runtime-Selfcheck"
description: "Turn-end runtime selfcheck contract. 在每个任务回合结束前，对本轮执行进行自检；顺利则跳过，有问题则先即时自修或沉淀修复建议，并把可优化点合并进 final reply。"
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
        reason: "Turn-end selfcheck is the default branch after reading the runtime contract."
---

# Meta-Runtime-Selfcheck

## 1. 工具入口
- 本技能运行时统一入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py runtime-contract --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic <topic> --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py paths --json`
- 运行时诊断与写回入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/runtime_pain_batch.py ">" --session-scope-mode all_threads --max-results 200`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/runtime_pain_batch.py 修复 --manual-repair-applied --manual-repair-path <changed_file> --verify-cmd <verify_cmd>`
- 模型读取 runtime contract、workflow、output 规则时必须优先走 CLI JSON；`SKILL.md` 只做门面。

## 2. 适用域
- 适用于：每个任务回合 `turn end` 前的默认运行自检。
- 适用于：工具错误、脚本失败、路径误用、犹豫不决、重复试错、文档缺口、技能描述不清、触发语气不准、模型 confused 与迷宫式流程。
- 适用于：在当前回合内能安全收口的问题，先即时自修；不能即时收口的问题，合并为 final reply 内的优化建议。
- 不适用于：未结束任务中途强插复盘叙事、把 pain provider 协议本身当主要用户叙事、无边界地自动改写大范围资产。

## 3. 必读顺序
1. 先执行 `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py runtime-contract --json`。
2. 再读取默认 turn-end 自检 workflow：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic turn-end-selfcheck --json`
3. 若自检发现当前回合内存在可安全收口的问题，再读取：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic self-repair-writeback --json`
4. 若任务涉及 runtime/result 路径时，再执行：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py paths --json`
5. 若需要把建议合并进 final reply，再读取：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic final-reply-merge --json`
6. 只有当 CLI JSON 仍留下真实语义缺口时，才打开 human mirrors。

## 4. 运行边界
- 默认触发：本技能是 `turn end` 默认自检合同，不需要用户手动点名才可进入。
- 跳过条件：若本轮运行顺利，没有工具错误、路径误用、明显犹豫、重复失败、用户纠偏或流程迷路，则跳过自检输出，不增加 final 噪音。
- 自修原则：若本轮发现的问题在当前回合内可被安全、局部、受管地修复，可先修复再收尾。
- 写回边界：允许修正文档、技能描述、技能触发语气、工具入口说明与局部脚本合同；不允许借自检之名无边界扩张修改面。
- 输出规则：若发现问题，必须把 `问题清单 + 可优化点建议 + 是否已即时修复 + 剩余风险` 合并进 final reply，而不是单独开一轮空洞复盘。
- 数据源来自外部 pain provider；若未提供 `CODEX_RUNTIME_PAIN_PROVIDER` 或 `--memory-runtime`，可退化为基于本轮可见运行证据的轻量自检，不把 provider 缺失本身伪装成用户问题。

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
