# AGENTS.md - Skills Governance Reminder

[SKILLS_GOVERNANCE_CONTRACT - HARD ENFORCEMENT]

0. Scope
- 本文件只承载技能规范治理合同。
- 本文件中的核心条款必须与 `Meta-Skill-Template` 并行存在并保持一致。

1. CLI Tooling Rule
- 技能内工具统一使用前缀 `Cli_Toolbox`。
- 若技能存在运行态规则、约束、指引，必须提供对应 CLI 输出入口。

2. Runtime Guidance Rule
- 模型禁止直接阅读 markdown 获取技能运行态规则、约束、指引。
- 运行态规则、约束、指引只能通过 CLI 输出的 machine-readable 合同获取。
- `SKILL.md` 只允许保留入口、描述、边界与导航；不得替代运行合同。

3. Dual-Format Rule
- 规则向、约束向、指引向内容必须同时存在两份：
  - machine-readable：`json` 或 `yaml`
  - 人类审计版：markdown
- markdown 只供人类审计，不是模型运行规则源。

4. Sync Rule
- 运行合同更新时，必须同步更新 machine-readable 版本与 markdown 审计版。
- 建议顺序：
  - 先更新 machine-readable 合同
  - 再通过确定性脚本或流程刷新 markdown 审计版
- 禁止只改 markdown 不改 machine-readable 合同。

5. GitHub Traceability Rule
- 如果本仓库在写入回合发生文件变动，则必须进行 GitHub 留痕；commit message 必须依据本轮实际变动内容编写。

6. Constitution/Lint Rule
- 只有本仓库与 `Octopus_OS` 承担宪法技能与静态 lint 收口责任。
- 当本仓库发生写入时，必须对实际被修改的具体 skill root 或具体仓库根运行 `Constitution-knowledge-base` static lint。
- 禁止把 `/home/jasontan656/AI_Projects` 当作 lint 目标；必须使用真实被影响的 concrete target root。
- 若 lint 非零退出或出现 `status=fail`，必须显式声明 `violation`，修复后重跑。
