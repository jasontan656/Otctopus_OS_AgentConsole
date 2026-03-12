[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理 `octopus-os-agent-console` 路径规则之前，必须先运行：
- `python3 /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/octopus-os-agent-console/AGENTS.md" --json`

2. 当前受管 repo 身份
- Current concrete repo: `octopus-os-agent-console`
- Current target kind: `AGENTS.md`
- `AGENTS.md` 应保持为 thin runtime entry；具体 routing/update 规则以返回的 JSON contract 为准。
- same-level `README.md` 已可用，可作为对外产品摘要入口。

3. 语言与表面边界
- 对外产品 `README.md` 与 `docs/` 中面向学习、测试、试用的说明必须使用英文。
- 面向终端用户的安装 wizard / TUI 必须提供英文与中文双语支持。
- skill 内核、治理合同、内部开发记录默认允许中文，英文仅在工程标识、命令、路径、API 与必要的公开接口名中使用。
- 面向 GitHub 的产品迭代日志与 commit subject 应优先使用英文，方便外部开发者阅读。

4. Runtime Rule Source
- CLI JSON 输出是该路径的运行时规则源。
- skill 内部 markdown 审计文件仅供人类审计，不可替代 CLI JSON。

5. 同回合要求
- 如果本回合写入 `octopus-os-agent-console`，必须从一开始就纳入 Git traceability；若任务内容涉及 Python 相关编辑，还必须把 `Dev-PythonCode-Constitution-Backend` 的阅读与 lint 纳入同回合范围。
- skill mirror 根目录固定为 `octopus-os-agent-console/Skills/`；repo 根目录保留给产品文档、产品工具与正常代码库入口。
- 如果本回合编辑 skill，必须先在 `octopus-os-agent-console/Skills/` 中的 mirror 副本完成编辑，禁止直接编辑 codex 安装目录下的对应 skill。
- skill 编辑完成后，若目标 skill 已存在于 codex 安装目录，必须同回合执行 `$SkillsManager-Mirror-To-Codex` 的 `Push`；若目标 skill 是新建且 codex 安装目录中尚不存在，必须同回合执行 `$SkillsManager-Mirror-To-Codex` 的 `Install`。
- 若任务内容涉及 Python 相关编辑，结束前必须完成 `Dev-PythonCode-Constitution-Backend` 的 lint。
- 如果本回合写入了 `octopus-os-agent-console`，必须同回合 commit-and-push。

6. Repo-local skills 依赖环境
- 与 skills 执行相关的 Python 依赖，必须安装到 repo 根目录下的 `./.venv_backend_skills`，禁止依赖全局 Python site-packages。
- `./requirements-backend_skills.lock.txt` 是 Python 依赖锁定清单；当新增、升级、删除 Python 依赖时，必须同回合同步更新它。
- 与 skills 执行相关的前端依赖，必须安装并锁定在 repo 根目录下的 `./frontend_skills/` 中；该目录下的 `package.json` 与 `package-lock.json` 是前端依赖真源。
- 若当前任务需要新增 repo-local 依赖，允许 AI 根据任务内容自行决定所需依赖并直接安装；但安装位置只能是本 repo 的 `*_skills` 环境或其受管 manifest/lock 所在目录。
- 若后续出现其他类型依赖，也必须优先落在 `octopus-os-agent-console` 目录内的 repo-local `*_skills` 环境或其对应 manifest/lock 文件中，禁止把全局环境当成长期依赖承载层。
- 当依赖集合发生变化时，必须同时保持 `Meta-RootFile-Manager` 内的治理映射模版与外部 `AGENTS.md` 内容同步。

7. Skills 必用 tech stack 基线
- `Skills/` 目录内若涉及 Python、Vue3、TypeScript、JSON、YAML、Markdown、lint、test、schema、CLI 或文档解析任务，必须优先使用 Part B 中 `skills_required_techstacks` 声明的受管 tech stack，禁止重复造轮子或绕开 repo-local `*_skills` 环境。
- 新增同类能力时，先判断现有必用 tech stack 是否已覆盖；仅在确有能力缺口时才允许增补依赖，并必须同回合更新 lock/manifest 与治理映射。

8. 治理链约束
- 更新本文件时及相关内容时,必须使用 $Meta-RootFile-Manager 更新治理映射模版然后再回推至本文件,或者更新本文件但是必须使用技能的collect来反向更新,避免单点更新治理链断裂.
</part_A>
