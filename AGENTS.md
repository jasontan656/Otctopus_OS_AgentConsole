# AGENTS.md - Codex Skills Mirror

[CODEX_SKILLS_MIRROR_CONTRACT - HARD ENFORCEMENT]

0. Scope
- 本合同适用于 `/home/jasontan656/AI_Projects/Codex_Skills_Mirror` 及其所有子技能目录。
- 根工作区运行钩子、push/lint 总规则仍由 `/home/jasontan656/AI_Projects/AGENTS.md` 管理；本文件补充 skills mirror 专属治理规则。

1. Load Order
- 进入本仓库任务时，先加载根工作区 `AGENTS.md`，再加载本文件。
- 若具体技能目录还有自己的运行合同，以“根工作区 -> 本仓库 -> 具体技能”的顺序叠加执行。

2. Runtime Guidance Rule
- 若某个技能提供 CLI 形式的运行合同、阶段指引、规则输出入口，模型必须先运行该 CLI，再执行技能动作。
- 禁止把技能内 markdown 文档直接当成运行态规则源，除非用户显式要求审计或比对 markdown。
- `SKILL.md` 在本仓库中只允许承担入口、边界、导航与审计路径说明，不得替代 CLI 运行合同。

3. Dual-Format Contract Rule
- 任何技能内的规则向、约束向、指引向内容，必须同时存在两份：
  - machine-readable 版本：`json` 或 `yaml`
  - 人类审计版本：markdown
- 若运行合同发生变更，必须在同一回合内完成双版本同步。
- 默认顺序：
  - 先改 machine-readable 合同
  - 再通过脚本或确定性流程刷新 markdown 审计版
- 禁止只改 markdown 不改 machine-readable 合同。

4. Template Sync Rule
- 若某个技能引入了可复用的技能治理模式、运行合同模式、文档同步模式，必须在同一回合评估并同步更新 `Meta-Skill-Template`。
- 禁止在单个技能里先落地新契约，却让模板体系继续输出旧模式。

5. Skill Boundary Rule
- 技能修改必须优先限定在具体技能目录内，禁止无目标地扫描或改写其他 sibling skills。
- 若任务已给出具体技能路径或具体目标文件，发现范围必须停留在这些路径内。
- 新建或改造技能一律在 `Codex_Skills_Mirror` 内完成，不在安装目录直接开发。

6. Verification Rule
- 影响了具体技能后，必须同步安装目录副本。
- 影响了具体技能后，必须对具体技能根目录运行 constitution lint。
- 写回合必须使用范围受限的 GitHub 提交，不得把本仓库无关改动一起提交。

7. Managed Default Docs Rule
- `Codex_Skills_Mirror/AGENTS.md` 属于常驻默认文档，必须纳入 `Meta-Default-md-manager` 的统一托管与索引。
- 若 mirror 仓新增新的常驻默认文档规则，也必须同步反映到 `Meta-Default-md-manager` 的 machine contract 与审计文档。
