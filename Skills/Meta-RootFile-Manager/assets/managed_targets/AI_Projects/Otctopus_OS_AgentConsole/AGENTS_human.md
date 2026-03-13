---
owner: "由 `$Meta-RootFile-Manager` 作为 `Otctopus_OS_AgentConsole` repository root container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
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

3. Runtime Rule Source
- CLI JSON 输出是该路径的运行时规则源。
- skill 内部 markdown 审计文件仅供人类审计，不可替代 CLI JSON。
- `Part B` 负责 machine payload；skills 治理顺序与最小语义入口以 `default_meta_skill_order` 为准。
- 路径、语言、依赖、tech stack、mirror/install、Git traceability 等具体规则若已在 `Part B` 或对应 `SkillsManager` 技能内声明，不在 `Part A` 重复展开。

4. Repo-local skills 依赖环境
- 与 skills 执行相关的 Python 依赖环境固定为 `./.venv_backend_skills`；对应锁文件为 `./requirements-backend_skills.lock.txt`。
- 与 skills 执行相关的前端依赖环境固定为 `./frontend_skills/`；对应真源为 `package.json` 与 `package-lock.json`。
- 若需要新增 repo-local 依赖，安装位置只能是本 repo 的 `*_skills` 环境或其受管 manifest/lock 所在目录，不得把全局环境当长期依赖承载层。

5. 同回合收口
- 如果本回合写入 `Otctopus_OS_AgentConsole`，必须同回合完成 Git traceability。
- 若任务内容涉及 Python 相关编辑，结束前必须完成 `Dev-PythonCode-Constitution` 的 lint。

6. 治理链约束
- 更新本文件时及相关内容时,必须使用 $Meta-RootFile-Manager 更新治理映射模版然后再回推至本文件,或者更新本文件但是必须使用技能的collect来反向更新,避免单点更新治理链断裂.
</part_A>

<part_B>

```json
{
  "owner": "由 `$Meta-RootFile-Manager` 作为 `Otctopus_OS_AgentConsole` repository root container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。",
  "entry_role": "repo_runtime_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "default_meta_skill_order": [
    "$SkillsManager-Production-Form (console product form and Skills surface governance)",
    "$SkillsManager-Naming-Manager (skill naming, family grouping, and registry governance)",
    "$SkillsManager-Creation-Template (governed skill creation and structure refit)",
    "$SkillsManager-Doc-Structure (skill markdown tree, metadata, and anchor graph governance)",
    "$SkillsManager-Tooling-CheckUp (skill tooling, techstack baseline, and runtime artifact governance)",
    "$SkillsManager-Mirror-To-Codex (sync edited skills to codex install)",
    "$meta-github-operation (Git traceability for repo writes)",
    "$skill-creator (Codex-readable skill formatter)",
    "$Dev-PythonCode-Constitution (Python governance and lint baseline)"
  ],
  "peer_summary_policy": {
    "available": true,
    "relation": "same_level_summary",
    "read_policy": "available_for_public_product_summary",
    "guidance": "same-level README.md is available and should be treated as the public English product summary for this repo"
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
    "use the returned target contract JSON as the runtime rule source"
  ],
  "runtime_constraints": [
    "stay within the concrete repo-local boundary defined by this payload",
    "all skill edits must happen under Otctopus_OS_AgentConsole/Skills as the codex skill installation mirror, then be pushed by SkillsManager; direct edits inside the codex installation folder are prohibited"
  ],
  "execution_modes": {
    "READ_EXEC": {
      "goal": "answer, inspect, classify, or route without changing files",
      "default_actions": [
        "prefer direct CLI contract output over opening markdown rule files",
        "open extra files only when the direct contract still leaves a real gap"
      ]
    },
    "WRITE_EXEC": {
      "goal": "edit files or trigger manager-owned write flows",
      "default_actions": [
        "state the intended write scope before editing"
      ]
    }
  },
  "forbidden_primary_runtime_pattern": [],
  "turn_end_actions": [
    "if dependency manifests or lock files changed, keep the AGENTS governance mapping synchronized in the same turn"
  ],
  "repo_name": "Otctopus_OS_AgentConsole"
}
```
</part_B>
