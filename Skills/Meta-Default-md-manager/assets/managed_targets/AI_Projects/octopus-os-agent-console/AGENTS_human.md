[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理 `octopus-os-agent-console` 路径规则之前，必须先运行：
- `python3 /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/Meta-Default-md-manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/octopus-os-agent-console/AGENTS.md" --json`

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
- skill 编辑完成后，若目标 skill 已存在于 codex 安装目录，必须同回合执行 `$skill-mirror-to-codex` 的 `Push`；若目标 skill 是新建且 codex 安装目录中尚不存在，必须同回合执行 `$skill-mirror-to-codex` 的 `Install`。
- 若任务内容涉及 Python 相关编辑，结束前必须完成 `Dev-PythonCode-Constitution-Backend` 的 lint。
- 如果本回合写入了 `octopus-os-agent-console`，必须同回合 commit-and-push。

6. Repo-local skills 依赖环境
- 与 skills 执行相关的 Python 依赖，必须安装到 repo 根目录下的 `./.venv_backend_skills`，禁止依赖全局 Python site-packages。
- `./requirements-backend_skills.lock.txt` 是 Python 依赖锁定清单；当新增、升级、删除 Python 依赖时，必须同回合同步更新它。
- 与 skills 执行相关的前端依赖，必须安装并锁定在 repo 根目录下的 `./frontend_skills/` 中；该目录下的 `package.json` 与 `package-lock.json` 是前端依赖真源。
- 若后续出现其他类型依赖，也必须优先落在 `octopus-os-agent-console` 目录内的 repo-local `*_skills` 环境或其对应 manifest/lock 文件中，禁止把全局环境当成长期依赖承载层。
- 当依赖集合发生变化时，必须同时保持 `Meta-Default-md-manager` 内的治理映射模版与外部 `AGENTS.md` 内容同步。
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
    "$meta-github-operation (after any write to octopus-os-agent-console, commit-and-push the repo for Git traceability; Git push is not a substitute for syncing the codex installation directory)",
    "$skill-mirror-to-codex (edit skills only in the product repo mirror paths, never directly in the codex installation directory; after editing, use Push for already-installed skills and Install for newly created skills)",
    "$skill-creation-template ( should be considered to imply if there is no specific user request on how skill should be created (prioritize user request than template) )",
    "$skill-creator (for skill standard formatter to ensure codex reads it properly, do not use its template for skill creation)",
    "$Dev-PythonCode-Constitution-Backend (for Python-related fat-file checks, split guidance, and lint runs when the task edits Python code)"
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
  "turn_start_actions": [
    "use the returned target contract JSON as the runtime rule source",
    "classify the turn as READ_EXEC or WRITE_EXEC",
    "if the turn will write octopus-os-agent-console, plan same-turn Git traceability from the start; if task contents include Python related edits, also plan Dev-PythonCode-Constitution-Backend reading and lint from the start",
    "if the task needs repo-local dependencies, read the backend/frontend skills environment manifests before installing or invoking tooling",
    "if the turn touches language surfaces, enforce outward English docs and inward Chinese development boundaries before editing",
    "if the turn will edit a skill, treat the mirror copy under octopus-os-agent-console/Skills as the only editable source and determine whether downstream sync must be Push or Install",
    "if task contents include Python related edits, read Dev-PythonCode-Constitution-Backend through SKILL.md -> TASK_ROUTING -> SKILL_EXECUTION_RULES before editing"
  ],
  "runtime_constraints": [
    "treat CLI JSON as the primary runtime rule source",
    "do not use audit markdown as the primary execution guide",
    "stay within the concrete repo-local boundary defined by this payload",
    "choose READ_EXEC or WRITE_EXEC by actual write intent, not by file type alone",
    "when this repo is written, keep same-turn Git traceability in scope; if task contents include Python related edits, keep same-turn Dev-PythonCode-Constitution-Backend lint in scope",
    "public-facing product README and docs must remain English-only",
    "end-user wizard and installation TUI surfaces must support both English and Chinese",
    "skill core docs, governance contracts, and internal iteration artifacts may remain Chinese-first",
    "GitHub-facing product iteration logs and commit subjects should prefer English wording",
    "skills runtime dependencies must be installed into repo-local *_skills environments or their tracked manifest/lock files, not global environments",
    "keep requirements-backend_skills.lock.txt in sync with the Python dependencies installed into .venv_backend_skills",
    "keep frontend_skills/package.json and frontend_skills/package-lock.json in sync with the frontend dependency set used by skills tasks",
    "for skill changes, edit the mirror copy under octopus-os-agent-console/Skills and never directly edit the codex installation directory",
    "all product-repo skill roots live under octopus-os-agent-console/Skills and repo root is not a syncable skill container",
    "product-facing docs and product tools must not be pushed into the codex installation directory; only syncable skill roots and .system may flow downstream",
    "after skill edits, use skill-mirror-to-codex Push for already-installed skills or Install for newly created skills before closing the turn"
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
        "for skill edits, write only the mirror copy under octopus-os-agent-console/Skills and do not directly edit the codex installed copy",
        "after skill edits, run skill-mirror-to-codex Push for existing installed skills or Install for newly created skills",
        "if task contents include Python related edits, run Dev-PythonCode-Constitution-Backend lint on the concrete Python-related target scope before closing the turn",
        "complete same-turn commit-and-push when octopus-os-agent-console files are written"
      ]
    }
  },
  "forbidden_primary_runtime_pattern": [
    "Do not treat audit markdown paths as the main runtime instructions.",
    "Do not require the model to open a chain of markdown files just to learn the next skill to use.",
    "Do not emit only path metadata when the real need is direct action guidance."
  ],
  "turn_end_actions": [
    "if task contents include Python related edits, run Dev-PythonCode-Constitution-Backend lint on the concrete Python-related target scope",
    "if dependency manifests or lock files changed, keep the repo-local skills environments and AGENTS governance mapping synchronized in the same turn",
    "if the turn edited a skill, complete skill-mirror-to-codex Push or Install before closing the turn",
    "if the turn wrote octopus-os-agent-console, complete same-turn commit-and-push before closing the turn"
  ],
  "repo_name": "octopus-os-agent-console"
}
```
</part_B>
