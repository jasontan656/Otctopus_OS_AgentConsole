---
doc_id: skillsmanager_tooling_checkup.references_runtime_contracts_techstack_baseline_guide
doc_type: topic_atom
topic: TECHSTACK_BASELINE_GUIDE
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# TECHSTACK_BASELINE_GUIDE

<part_A>
- 本 guide 只解决一个问题：当前 repo 已经把哪些技能依赖栈治理成必用基线。
- 人类阅读时应把它当成“可疑重复造轮子”的判断锚点，而不是新增依赖提案。
- 模型运行时应通过 `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py directive --topic techstack-baseline --json` 获取 Part B。
</part_A>

<part_B>

```json
{
  "directive_name": "skills_tooling_checkup_techstack_baseline_guide",
  "directive_version": "1.0.0",
  "doc_kind": "guide",
  "topic": "techstack-baseline",
  "purpose": "Provide the repo-local mandatory baseline used to judge whether target tooling code is rebuilding existing stack capability.",
  "instruction": [
    "Treat the repo-local skills_required_techstacks baseline as the only mandatory replacement anchor for this skill.",
    "Python baseline includes pytest, ruff, PyYAML, jsonschema, pydantic, markdown-it-py, mdformat, python-frontmatter, typer, rich, httpx, and watchfiles.",
    "Vue3 and TypeScript baseline includes vue, typescript, @types/node, tsx, vitest, eslint, typescript-eslint, eslint-plugin-vue, vue-tsc, markdownlint-cli2, gray-matter, markdown-it, ajv, zod, and prettier."
  ],
  "workflow": [
    "Map the target implementation to the capability it is trying to provide.",
    "Check whether the mandatory baseline already covers that capability directly enough to replace, shrink, or delete the custom implementation.",
    "If the target logic still carries repo-specific orchestration, compatibility semantics, or domain policy beyond the baseline, keep that layer and only remove the truly generic wheel."
  ],
  "rules": [
    "Do not add new dependency requirements from this guide alone.",
    "Do not force replacement when the baseline cannot preserve target semantics.",
    "Pattern resemblance is only a suspicion signal; behavior alignment remains mandatory.",
    "Do not restate Python or TypeScript code-style rules here; this guide only decides capability overlap against existing dependencies."
  ]
}
```
</part_B>
