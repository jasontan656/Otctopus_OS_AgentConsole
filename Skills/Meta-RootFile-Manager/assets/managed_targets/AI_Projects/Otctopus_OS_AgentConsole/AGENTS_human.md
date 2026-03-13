---
doc_id: meta_rootfile_manager.assets_managed_targets_ai_projects_otctopus_os_agentconsole_agents
doc_type: topic_atom
topic: Agents
anchors:
- target: ../../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理 `Otctopus_OS_AgentConsole` 路径规则之前，必须先运行：
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md" --json`

2. 当前受管 repo 身份
- Current concrete repo: `Otctopus_OS_AgentConsole`
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

5. 路径治理规范
- 产品运行态路径必须先识别唯一 `root`，再从 `root` 推导；禁止把作者机器上的绝对路径、`AI_Projects` 字面量或 `~/.codex` 当成唯一真源。
- 受本 repo 治理的产品路径默认包括：`<root>/.codex`、`<root>/console`、`<root>/Codex_Skill_Runtime`、`<root>/Codex_Skills_Result`、`<root>/Octopus_OS`、`<root>/Otctopus_OS_AgentConsole` 以及其他 root 下的受管 sibling 项目目录。
- skill 自身局部资源（如 `SKILL.md`、`references/`、`assets/`、`scripts/`）可相对当前 skill root 解析；但产品运行态路径、repo 镜像路径、runtime/result 路径、外部工作区路径必须回到 `root` 推导。
- 若当前机器处于 attach-existing-codex 场景，`<root>/.codex` 可以暂时不存在；此时仅 Codex home 允许回退到显式 `CODEX_HOME` 或检测到的现有 Codex 安装，其他产品路径仍必须保持 root-first。
- 新增或改写 skill / installer / contract / prompt 时，必须优先使用这套 root-first 规则，避免把旧机器路径重新写回 repo。

6. 同回合要求
- 如果本回合写入 `Otctopus_OS_AgentConsole`，必须从一开始就纳入 Git traceability；若任务内容涉及 Python 相关编辑，还必须把 `Dev-PythonCode-Constitution` 的阅读与 lint 纳入同回合范围。
- skill mirror 根目录固定为 `Otctopus_OS_AgentConsole/Skills/`；repo 根目录保留给产品文档、产品工具与正常代码库入口。
- 如果本回合编辑 skill，必须先在 `Otctopus_OS_AgentConsole/Skills/` 中的 mirror 副本完成编辑，禁止直接编辑 codex 安装目录下的对应 skill。
- skill 编辑完成后，若目标 skill 已存在于 codex 安装目录，必须同回合执行 `$SkillsManager-Mirror-To-Codex` 的 `Push`；若目标 skill 是新建且 codex 安装目录中尚不存在，必须同回合执行 `$SkillsManager-Mirror-To-Codex` 的 `Install`。
- 若任务内容涉及 Python 相关编辑，结束前必须完成 `Dev-PythonCode-Constitution` 的 lint。
- 如果本回合写入了 `Otctopus_OS_AgentConsole`，必须同回合 commit-and-push。

7. Repo-local skills 依赖环境
- 与 skills 执行相关的 Python 依赖，必须安装到 repo 根目录下的 `./.venv_backend_skills`，禁止依赖全局 Python site-packages。
- `./requirements-backend_skills.lock.txt` 是 Python 依赖锁定清单；当新增、升级、删除 Python 依赖时，必须同回合同步更新它。
- 与 skills 执行相关的前端依赖，必须安装并锁定在 repo 根目录下的 `./frontend_skills/` 中；该目录下的 `package.json` 与 `package-lock.json` 是前端依赖真源。
- 若当前任务需要新增 repo-local 依赖，允许 AI 根据任务内容自行决定所需依赖并直接安装；但安装位置只能是本 repo 的 `*_skills` 环境或其受管 manifest/lock 所在目录。
- 若后续出现其他类型依赖，也必须优先落在 `Otctopus_OS_AgentConsole` 目录内的 repo-local `*_skills` 环境或其对应 manifest/lock 文件中，禁止把全局环境当成长期依赖承载层。
- 当依赖集合发生变化时，必须同时保持 `Meta-RootFile-Manager` 内的治理映射模版与外部 `AGENTS.md` 内容同步。

8. Skills 必用 tech stack 基线
- `Skills/` 目录内若涉及 Python、Vue3、TypeScript、JSON、YAML、Markdown、lint、test、schema、CLI 或文档解析任务，必须优先使用 Part B 中 `skills_required_techstacks` 声明的受管 tech stack，禁止重复造轮子或绕开 repo-local `*_skills` 环境。
- 新增同类能力时，先判断现有必用 tech stack 是否已覆盖；仅在确有能力缺口时才允许增补依赖，并必须同回合更新 lock/manifest 与治理映射。

9. 治理链约束
- 更新本文件时及相关内容时,必须使用 $Meta-RootFile-Manager 更新治理映射模版然后再回推至本文件,或者更新本文件但是必须使用技能的collect来反向更新,避免单点更新治理链断裂.
</part_A>

<part_B>

```json
{
  "entry_role": "repo_runtime_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "default_meta_skill_order": [
    "$meta-github-operation (after any write to Otctopus_OS_AgentConsole, commit-and-push the repo for Git traceability; Git push is not a substitute for syncing the codex installation directory)",
    "$SkillsManager-Mirror-To-Codex (edit skills only in the product repo mirror paths, never directly in the codex installation directory; after editing, use Push for already-installed skills and Install for newly created skills)",
    "$SkillsManager-Creation-Template ( should be considered to imply if there is no specific user request on how skill should be created (prioritize user request than template) )",
    "$skill-creator (for skill standard formatter to ensure codex reads it properly, do not use its template for skill creation)",
    "$Dev-PythonCode-Constitution (for Python-related fat-file checks, split guidance, and lint runs when the task edits Python code)"
  ],
  "peer_summary_policy": {
    "available": true,
    "relation": "same_level_summary",
    "read_policy": "available_for_public_product_summary",
    "guidance": "same-level README.md is available and should be treated as the public English product summary for this repo"
  },
  "language_policy": {
    "conversation_and_internal_coordination": "Chinese-first",
    "public_product_readme_and_docs": "English-only",
    "wizard_user_interface": "Bilingual English/Chinese required",
    "internal_skill_core_and_governance_docs": "Chinese allowed for internal iteration",
    "git_iteration_logs_for_github": "English-preferred"
  },
  "skills_required_techstacks": {
    "python_backend": [
      "pytest",
      "ruff",
      "PyYAML",
      "jsonschema",
      "pydantic",
      "markdown-it-py",
      "mdformat",
      "python-frontmatter",
      "typer",
      "rich",
      "httpx",
      "watchfiles"
    ],
    "vue3_typescript_frontend": [
      "vue",
      "typescript",
      "@types/node",
      "tsx",
      "vitest",
      "eslint",
      "typescript-eslint",
      "eslint-plugin-vue",
      "vue-tsc",
      "markdownlint-cli2",
      "ajv",
      "zod",
      "gray-matter",
      "markdown-it",
      "prettier"
    ]
  },
  "turn_start_actions": [
    "use the returned target contract JSON as the runtime rule source",
    "classify the turn as READ_EXEC or WRITE_EXEC",
    "when task contents include skill/runtime/product path usage, identify the concrete product root first and derive governed runtime paths from that root before editing",
    "if the turn will write Otctopus_OS_AgentConsole, plan same-turn Git traceability from the start; if task contents include Python related edits, also plan Dev-PythonCode-Constitution reading and lint from the start",
    "if the task needs repo-local dependencies, read the backend/frontend skills environment manifests before installing or invoking tooling",
    "if the task needs new repo-local dependencies, the AI may choose them from task evidence and install them into the governed *_skills environments before use",
    "if the task touches Skills/, read skills_required_techstacks first and treat it as the mandatory baseline before introducing new stacks or writing custom equivalents",
    "if the turn touches language surfaces, enforce outward English docs and inward Chinese development boundaries before editing",
    "if the turn will edit a skill, treat the mirror copy under Otctopus_OS_AgentConsole/Skills as the only editable source and determine whether downstream sync must be Push or Install",
    "if task contents include Python related edits, read Dev-PythonCode-Constitution through SKILL.md -> TASK_ROUTING -> SKILL_EXECUTION_RULES before editing"
  ],
  "runtime_constraints": [
    "treat CLI JSON as the primary runtime rule source",
    "do not use audit markdown as the primary execution guide",
    "stay within the concrete repo-local boundary defined by this payload",
    "choose READ_EXEC or WRITE_EXEC by actual write intent, not by file type alone",
    "when this repo is written, keep same-turn Git traceability in scope; if task contents include Python related edits, keep same-turn Dev-PythonCode-Constitution lint in scope",
    "product/runtime paths must resolve from the product root; do not hardcode author-machine absolute paths or treat AI_Projects literals as the only valid install root",
    "skill-local resources may resolve from current skill roots, but repo mirrors, codex runtime paths, result paths, and product workspaces must use root-first derivation",
    "when <root>/.codex is absent, only Codex home lookup may fall back to explicit CODEX_HOME or an attached existing Codex installation; other governed product paths remain root-first",
    "public-facing product README and docs must remain English-only",
    "end-user wizard and installation TUI surfaces must support both English and Chinese",
    "skill core docs, governance contracts, and internal iteration artifacts may remain Chinese-first",
    "GitHub-facing product iteration logs and commit subjects should prefer English wording",
    "skills runtime dependencies must be installed into repo-local *_skills environments or their tracked manifest/lock files, not global environments",
    "the AI may decide which repo-local dependencies are needed for the active task, but every installation must stay inside the governed repo-local environments and be reflected in the tracked lock or manifest files",
    "when the task touches Skills/, treat skills_required_techstacks as the mandatory baseline and do not reinvent equivalent local parsing, lint, markdown, schema, test, CLI, or runtime stacks without an explicit user override",
    "keep requirements-backend_skills.lock.txt in sync with the Python dependencies installed into .venv_backend_skills",
    "keep frontend_skills/package.json and frontend_skills/package-lock.json in sync with the frontend dependency set used by skills tasks",
    "for skill changes, edit the mirror copy under Otctopus_OS_AgentConsole/Skills and never directly edit the codex installation directory",
    "all product-repo skill roots live under Otctopus_OS_AgentConsole/Skills and repo root is not a syncable skill container",
    "product-facing docs and product tools must not be pushed into the codex installation directory; only syncable skill roots and .system may flow downstream",
    "after skill edits, use SkillsManager-Mirror-To-Codex Push for already-installed skills or Install for newly created skills before closing the turn"
  ],
  "execution_modes": {
    "READ_EXEC": {
      "goal": "answer, inspect, classify, or route without changing files",
      "default_actions": [
        "prefer direct CLI contract output over opening markdown rule files",
        "open extra files only when the direct contract still leaves a real gap",
        "treat README.md as the public English summary instead of inferring product positioning from internal skill docs"
      ]
    },
    "WRITE_EXEC": {
      "goal": "edit files or trigger manager-owned write flows",
      "default_actions": [
        "apply the default meta sequence before editing",
        "state the intended write scope before editing",
        "edit the minimal correct scope that matches the user intent",
        "for public product surfaces, keep English-only wording and avoid leaking internal Chinese governance content",
        "for skill edits, write only the mirror copy under Otctopus_OS_AgentConsole/Skills and do not directly edit the codex installed copy",
        "after skill edits, run SkillsManager-Mirror-To-Codex Push for existing installed skills or Install for newly created skills",
        "if task contents include Python related edits, run Dev-PythonCode-Constitution lint on the concrete Python-related target scope before closing the turn",
        "complete same-turn commit-and-push when Otctopus_OS_AgentConsole files are written"
      ]
    }
  },
  "forbidden_primary_runtime_pattern": [
    "Do not treat audit markdown paths as the main runtime instructions.",
    "Do not require the model to open a chain of markdown files just to learn the next skill to use.",
    "Do not emit only path metadata when the real need is direct action guidance."
  ],
  "turn_end_actions": [
    "if task contents include Python related edits, run Dev-PythonCode-Constitution lint on the concrete Python-related target scope",
    "if dependency manifests or lock files changed, keep the repo-local skills environments and AGENTS governance mapping synchronized in the same turn",
    "if the turn updated the mandatory Skills tech stack baseline, keep skills_required_techstacks and the repo-local environment lock or manifest files synchronized in the same turn",
    "if the turn edited a skill, complete SkillsManager-Mirror-To-Codex Push or Install before closing the turn",
    "if the turn wrote Otctopus_OS_AgentConsole, complete same-turn commit-and-push before closing the turn"
  ],
  "repo_name": "Otctopus_OS_AgentConsole"
}
```
</part_B>
