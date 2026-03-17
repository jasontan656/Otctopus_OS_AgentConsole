---
name: "Meta-Runtime-Selfcheck"
description: "Turn hook runtime self-repair contract. 在整个任务回合中持续监测问题；一旦出现问题，先在当前边界内立即修复，再把修复结果与残余风险合并进最终汇报。"
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
        reason: "Turn-hook self-repair is the default branch after reading the runtime contract."
---

# Meta-Runtime-Selfcheck

## 1. 工具入口
- 本技能运行时统一入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py runtime-contract --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic <topic> --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py paths --json`
  - `cat <command_file> | ./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py pre-exec-check --workdir <repo_or_cwd> --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py run-turn-hook --mode diagnose --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py watch-codex-sessions --once --json`
- 运行时诊断与写回入口：
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/runtime_pain_batch.py ">" --session-scope-mode all_threads --max-results 200`
  - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py run-turn-hook --mode repair --auto-repair --json`
- 模型读取 runtime contract、workflow、output 规则时必须优先走 CLI JSON；`SKILL.md` 只做门面。

## 2. 适用域
- 适用于：整个任务回合内的默认运行 hook；遇到问题立即启动，而不是等到 `turn end` 才启动。
- 适用于：工具错误、脚本失败、路径误用、犹豫不决、重复试错、文档缺口、技能描述不清、触发语气不准、模型 confused 与迷宫式流程。
- 适用于：发现问题后，先在当前边界内执行最小可验证修复，再把修复结果与残余风险合并进 final reply。
- 适用于：在执行前判断某个失败是否属于阶段内预期信号，并按白名单做“记录后放行”。
- 不适用于：未结束任务中途强插复盘叙事、把 pain provider 协议本身当主要用户叙事、无边界地自动改写大范围资产。

## 3. 必读顺序
1. 先执行 `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py runtime-contract --json`。
2. 当本回合进入 turn start / 中途卡壳 / turn end 收口时，用真实 carrier 运行 hook：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py run-turn-hook --mode diagnose --json`
3. 当命令即将触达 repo-local Python、lint、traceability 或其他受管 CLI 时，先跑：
   - `cat <command_file> | ./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py pre-exec-check --workdir <repo_or_cwd> [--stage <stage>] [--expected-failure-file <rules.json>] --json`
4. 当本回合任意时刻出现问题证据时，立即读取默认 turn hook workflow：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic turn-hook-self-repair --json`
5. 若当前阶段允许“预期失败白名单”，先读取：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic expected-failure-governance --json`
6. 若 hook 发现当前边界内存在可验证修复动作，再读取：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic self-repair-writeback --json`
7. 若任务涉及 runtime/result 路径时，再执行：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py paths --json`
8. 当最终汇报需要合并“已修复项 / 剩余风险 / 用户可继续裁决项”时，再读取：
   - `./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic final-reply-merge --json`
9. 只有当 CLI JSON 仍留下真实语义缺口时，才打开 human mirrors。

## 4. 运行边界
- 默认触发：本技能是整个回合内的默认 turn hook，不需要用户手动点名才可进入；在 `turn end` 前还必须再跑一次最终收口检查，并留下 turn audit。
- pre-exec 主线：当命令涉及 repo-local Python、lint、traceability 或其他高频运行痛点时，先用 `pre-exec-check` 做裁决，再决定执行或放行。
- 跳过条件：仅当本轮没有任何工具错误、路径误用、明显犹豫、重复失败、用户纠偏或流程迷路时，才不输出额外 hook 内容。
- 自修原则：若本轮发现的问题在当前回合内可被安全、局部、受管地修复，必须先修复再继续，不允许只留建议后收尾。
- 预期失败原则：回归测试、lint、contract 校验等在某些阶段可被白名单声明为“记录后放行”的预期失败；它们不能被静默吞掉，也不能被误当成立即覆盖掉的运行痛点。
- 写回边界：允许修正文档、技能描述、技能触发语气、工具入口说明与局部脚本合同；不允许借自检之名无边界扩张修改面。
- 输出规则：若发现问题，必须把 `已即时修复项 + 修复验证结果 + 剩余风险 + 用户后续可裁决项` 合并进 final reply，而不是单独开一轮空洞复盘。
- 数据源优先来自外部 pain provider；若未提供 `CODEX_RUNTIME_PAIN_PROVIDER` 或 `--memory-runtime`，必须退化为基于 Codex session turn evidence 的 governed selfcheck，不把 provider 缺失本身伪装成用户问题。

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
