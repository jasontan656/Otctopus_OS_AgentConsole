---
name: "skill-production-form"
description: "持续维护 console 目录的产品形态，并沉淀将 Skills 目录作为 console 产品化源面的本地设计历史。"
---

# Skill-Production-Form

## 1. 定位
- 本文件只做门面入口，不承载规则正文。
- 本技能的唯一主轴是：`console_product_form -> local_iteration_log -> next_console_productization_decision`。
- 本技能专门服务 `octopus-os-agent-console` 中 console 目录的持续产品化维护，把“console 目录现在处于什么产品形态、为什么这样组织、最近收敛了哪些边界、下一步还要塑什么”沉淀成稳定可读的技能上下文。
- 本技能聚焦“把 `Skills/` 目录作为 console 产品化源面来治理”的相关技能管理，而不是替代具体 domain skill 的实现本体。
- 本技能存在运行态规则；运行入口、日志路径与输出合同应以 `Cli_Toolbox.py` 的 machine-readable 输出为准。

## 2. 必读顺序
1. 先读取运行合同：
   - `python3 scripts/Cli_Toolbox.py working-contract --json`
2. 再读取当前 console 产品意图快照：
   - `python3 scripts/Cli_Toolbox.py intent-snapshot --json`
3. 若本回合要延续历史决策，先读取最近的本地设计变更：
   - `python3 scripts/Cli_Toolbox.py latest-log --json`
4. 当本回合形成新的 console 产品判断、目录边界收敛或技能产品化规则变更后，必须追加本地日志：
   - `python3 scripts/Cli_Toolbox.py append-iteration-log ...`
5. 若本回合只是在回答问题、不形成新的产品判断，可跳过日志写入，但不得跳过前 1 到 3 步的历史收敛。

## 3. 分类入口
- 运行合同层：
  - `references/runtime/WORKING_CONTRACT.json`
  - `references/runtime/WORKING_CONTRACT.md`
- 当前目标层：
  - `references/runtime/CURRENT_PRODUCT_INTENT.md`
- 历史记录层：
  - `references/runtime/ITERATION_LOG.md`
  - `references/runtime/LOG_ENTRY_TEMPLATE.md`
- 工具层：
  - `scripts/Cli_Toolbox.py`
- 测试层：
  - `tests/test_cli_toolbox.py`
- 运行边界层：
  - `/home/jasontan656/AI_Projects/AGENTS.md`
  - `/home/jasontan656/AI_Projects/octopus-os-agent-console/AGENTS.md`

## 4. 适用域
- 适用于：`octopus-os-agent-console` 的 console 目录产品形态收敛、`Skills/` 目录产品化治理、技能管理面命名/边界/运行面持续塑形。
- 适用于：当 AI 需要先理解“console 目录现在应该以什么产品形态存在”再继续推进技能治理时。
- 不适用于：替代具体 domain skill 的实现细节、替代 `skill-mirror-to-codex` 的同步职责、替代 Git 提交本身。
- 不适用于：长期公开 release 日志；本技能只承担 console 产品化阶段的本地连续性上下文。

## 5. 执行入口
- 统一入口：
  - `python3 scripts/Cli_Toolbox.py working-contract --json`
- 当前目标快照：
  - `python3 scripts/Cli_Toolbox.py intent-snapshot --json`
- 最近历史：
  - `python3 scripts/Cli_Toolbox.py latest-log --json`
- 追加本地迭代日志：
  - `python3 scripts/Cli_Toolbox.py append-iteration-log --title "<title>" --summary "<summary>" --decision "<decision>" --affected-path "<path>" --next-step "<next>"`

## 6. 读取原则
- 门面只做路由，规则正文下沉到 `references/runtime/` 与 `scripts/`。
- 先收敛“当前 console 产品意图”和“最近迭代历史”，再继续推进新的 console 产品化变更；不要脱离历史上下文直接补丁式决策。
- 本技能的本地设计变更日志是阶段性真源；新的关键 console 产品判断必须先落本地 markdown。
- 日志应记录真正的 console 产品化判断，而不是流水账式操作输出。
- 若本技能的工作流、日志字段或当前目标发生结构变化，同步更新门面、runtime contract、日志模板、脚本与测试。

## 7. 结构索引
```text
skill-production-form/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── Cli_Toolbox.py
├── references/
│   ├── runtime/
│   │   ├── WORKING_CONTRACT.json
│   │   ├── WORKING_CONTRACT.md
│   │   ├── CURRENT_PRODUCT_INTENT.md
│   │   ├── ITERATION_LOG.md
│   │   └── LOG_ENTRY_TEMPLATE.md
│   └── tooling/
└── tests/
    └── test_cli_toolbox.py
```
