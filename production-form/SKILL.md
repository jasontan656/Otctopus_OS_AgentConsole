---
name: "production-form"
description: "临时产品塑形技能：持续承载当前 Octopus OS 产品化任务，维护本地设计变更日志，并为 AI 提供稳定的历史上下文入口。"
---

# Production-Form

## 1. 定位
- 本文件只做门面入口，不承载规则正文。
- 本技能的唯一主轴是：`current_product_form -> local_iteration_log -> next_design_decision`。
- 本技能专门服务当前进行中的 `Octopus OS / octopus-os-agent-console` 产品塑形任务，把“现在到底在做什么、为什么这么做、最近改了什么、接下来要收敛什么”沉淀成可持续读取的内部技能上下文。
- 本技能是临时快速迭代技能；在完整产品形态切换完成前，设计变更历史先记录在本地 markdown，后续再把主要迭代日志切回 GitHub。
- 本技能存在运行态规则；运行入口、日志路径与输出合同应以 `Cli_Toolbox.py` 的 machine-readable 输出为准。

## 2. 必读顺序
1. 先读取运行合同：
   - `python3 scripts/Cli_Toolbox.py working-contract --json`
2. 再读取当前产品意图快照：
   - `python3 scripts/Cli_Toolbox.py intent-snapshot --json`
3. 若本回合要延续历史决策，先读取最近的本地设计变更：
   - `python3 scripts/Cli_Toolbox.py latest-log --json`
4. 当本回合形成新的设计判断、边界收敛或产品结构变更后，必须追加本地日志：
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
- 适用于：当前 `Octopus OS` 产品形态收敛、产品边界塑形、安装/清理模型、语言规范、技能与产品分层、临时阶段的本地设计历史沉淀。
- 适用于：当 AI 需要先理解“这个产品现在发展到哪一层了”再继续推进时。
- 不适用于：替代具体 domain skill 的实现细节、替代 `skill-mirror-to-codex` 的同步职责、替代 Git 提交本身。
- 不适用于：完整稳定版发布后的长期公开 release 记录；那一阶段应逐步转回 GitHub 为主的迭代日志模式。

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
- 先收敛“当前产品意图”和“最近迭代历史”，再继续推进新的产品变更；不要脱离历史上下文直接补丁式决策。
- 本技能的本地设计变更日志是阶段性真源；在完整产品形态切换前，新的关键设计判断必须先落本地 markdown。
- 日志应记录真正的产品判断，而不是流水账式操作输出。
- 若本技能的工作流、日志字段或当前目标发生结构变化，同步更新门面、runtime contract、日志模板、脚本与测试。

## 7. 结构索引
```text
production-form/
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
