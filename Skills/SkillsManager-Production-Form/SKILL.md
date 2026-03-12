---
name: "SkillsManager-Production-Form"
description: "持续维护 console 目录的产品形态，并沉淀将 Skills 目录作为 console 产品化源面的本地设计历史。"
---

# SkillsManager-Production-Form

## 1. 定位
- 本文件只做门面入口，不承载规则正文。
- 本技能的唯一主轴是：`console_product_form -> local_iteration_log -> next_console_productization_decision`。
- 本技能专门服务 `octopus-os-agent-console` 中 console 目录的持续产品化维护，把“console 目录现在处于什么产品形态、为什么这样组织、最近收敛了哪些边界、下一步还要塑什么”沉淀成稳定可读的技能上下文。
- 本技能聚焦“把 `Skills/` 目录作为 console 产品化源面来治理”的相关技能管理，而不是替代具体 domain skill 的实现本体。
- 当 console 产品化判断涉及 root file 受管文件时，本技能只负责声明边界与路由，真正的正文治理必须交给 `$Meta-RootFile-Manager`，不得直接编辑外部受管文件。
- 本技能存在运行态规则；运行入口、日志路径与输出合同应以 `Cli_Toolbox.py` 的 machine-readable 输出为准。
- 本技能的 active runtime 日志必须落盘到 `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/SkillsManager-Production-Form`；默认结果根为 `/home/jasontan656/AI_Projects/Codex_Skills_Result/SkillsManager-Production-Form`。
- `references/runtime/ITERATION_LOG.md` 仅保留为 legacy seed snapshot；新的迭代日志不得继续写回技能目录。

## 2. 必读顺序
1. 先读取运行合同：
   - `./.venv_backend_skills/bin/python Skills/SkillsManager-Production-Form/scripts/Cli_Toolbox.py working-contract --json`
2. 再读取当前 console 产品意图快照：
   - `./.venv_backend_skills/bin/python Skills/SkillsManager-Production-Form/scripts/Cli_Toolbox.py intent-snapshot --json`
3. 若本回合要延续历史决策，先读取最近的本地设计变更：
   - `./.venv_backend_skills/bin/python Skills/SkillsManager-Production-Form/scripts/Cli_Toolbox.py latest-log --json`
4. 若本回合涉及 root file 受管文件，必须先路由到 `$Meta-RootFile-Manager` 的受管流程；不得在本技能上下文里直接编辑外部受管文件。
5. 当本回合形成新的 console 产品判断、目录边界收敛或技能产品化规则变更后，必须追加本地日志：
   - `./.venv_backend_skills/bin/python Skills/SkillsManager-Production-Form/scripts/Cli_Toolbox.py append-iteration-log ...`
6. 若本回合只是在回答问题、不形成新的产品判断，可跳过日志写入，但不得跳过前 1 到 4 步的历史收敛。

## 3. 分类入口
- 运行合同层：
  - `references/runtime/WORKING_CONTRACT.json`
  - `references/runtime/WORKING_CONTRACT.md`
- 当前目标层：
  - `references/runtime/CURRENT_PRODUCT_INTENT.md`
- 历史记录层：
  - `references/runtime/ITERATION_LOG.md`
  - `references/runtime/LOG_ENTRY_TEMPLATE.md`
- 运行落盘层：
  - `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/SkillsManager-Production-Form/ITERATION_LOG.md`
  - `/home/jasontan656/AI_Projects/Codex_Skills_Result/SkillsManager-Production-Form/`
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
- 适用于：当 console 产品化决策触及 `AGENTS.md`、`README.md`、`LICENSE` 等 root file 受管文件时，为这些文件声明必须走 `$Meta-RootFile-Manager` 的治理链。
- 不适用于：替代具体 domain skill 的实现细节、替代 `SkillsManager-Mirror-To-Codex` 的同步职责、替代 Git 提交本身。
- 不适用于：绕过 `$Meta-RootFile-Manager` 直接维护 root file 受管文件正文。
- 不适用于：长期公开 release 日志；本技能只承担 console 产品化阶段的本地连续性上下文。

## 5. 执行入口
- 统一入口：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Production-Form/scripts/Cli_Toolbox.py working-contract --json`
- 当前目标快照：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Production-Form/scripts/Cli_Toolbox.py intent-snapshot --json`
- 最近历史：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Production-Form/scripts/Cli_Toolbox.py latest-log --json`
- 追加本地迭代日志：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Production-Form/scripts/Cli_Toolbox.py append-iteration-log --title "<title>" --summary "<summary>" --decision "<decision>" --affected-path "<path>" --next-step "<next>"`
- 运行时落盘约束：
  - 默认日志落点：`/home/jasontan656/AI_Projects/Codex_Skill_Runtime/SkillsManager-Production-Form/ITERATION_LOG.md`
  - 默认结果根：`/home/jasontan656/AI_Projects/Codex_Skills_Result/SkillsManager-Production-Form/`
  - 若未来新增定向产物型命令，必须支持显式产物路径；未指定时默认落入上述 result 根。

## 6. 读取原则
- 门面只做路由，规则正文下沉到 `references/runtime/` 与 `scripts/`。
- 先收敛“当前 console 产品意图”和“最近迭代历史”，再继续推进新的 console 产品化变更；不要脱离历史上下文直接补丁式决策。
- 若变更触及 root file 受管文件，先声明产品边界，再切换到 `$Meta-RootFile-Manager` 完成 collect / push / target-contract 等受管动作，不得在本技能上下文直接手改外部文件。
- 本技能的本地设计变更日志是阶段性真源；新的关键 console 产品判断必须先落本地 markdown。
- 历史日志迁移后，repo 内 `references/runtime/ITERATION_LOG.md` 只作为 bootstrap seed；active 写入必须留在 governed runtime root。
- 日志应记录真正的 console 产品化判断，而不是流水账式操作输出。
- 若本技能的工作流、日志字段或当前目标发生结构变化，同步更新门面、runtime contract、日志模板、脚本与测试。

## 7. 结构索引
```text
SkillsManager-Production-Form/
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
