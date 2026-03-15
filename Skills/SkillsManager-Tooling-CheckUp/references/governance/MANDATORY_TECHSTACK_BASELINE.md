---
doc_id: skills_tooling_checkup.governance.mandatory_techstack_baseline
doc_type: topic_atom
topic: Mandatory repo-local tech stack baseline for skills tooling remediation
---

# Mandatory Techstack Baseline

## 本地目的
- 收敛当前 repo 已治理为必用内容的 skills tech stack。
- 让“是否属于重复造轮子”有稳定判断基线，而不是每次靠临场印象决定。

## 当前边界
- 本文只记录已存在于 repo 治理合同中的必用依赖栈。
- 本文不负责新增依赖；若依赖基线需要变更，应交回 repo 合同治理链，而不是在本技能内私改。

## Python backend baseline
- 测试与断言：`pytest`
- lint / format-oriented static governance: `ruff`
- YAML 解析：`PyYAML`
- JSON / schema 校验：`jsonschema`
- typed data validation / normalization: `pydantic`
- Markdown 解析：`markdown-it-py`
- Markdown formatting: `mdformat`
- frontmatter 解析：`python-frontmatter`
- CLI framework: `typer`
- terminal rendering: `rich`
- HTTP client: `httpx`
- file watching: `watchfiles`

## Vue3 / TypeScript frontend baseline
- runtime / component layer: `vue`
- language / type layer: `typescript`, `@types/node`
- TS execution / test / lint / typecheck: `tsx`, `vitest`, `eslint`, `typescript-eslint`, `eslint-plugin-vue`, `vue-tsc`
- Markdown / text / schema: `markdownlint-cli2`, `gray-matter`, `markdown-it`, `ajv`, `zod`
- formatting: `prettier`

## 判断准则
- 若目标代码正在手写这些依赖已经直接覆盖的通用能力，应优先判断为可疑重复造轮子。
- 若目标代码是 domain-specific orchestration、repo-specific policy、或依赖无法直接表达的语义，则不应机械替换。
- “可疑重复造轮子”不是自动替换命令；只有在行为边界清楚、可验证、不丢语义时才进入修正。
- 本文不负责 Python/TypeScript 语言代码规范正文；胖文件、typing、异常风格与语言专属 lint 细则应交回对应 constitution。
