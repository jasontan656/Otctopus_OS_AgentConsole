---
doc_id: "skills_tooling_checkup.governance.common_redundant_wheel_patterns"
doc_type: "topic_atom"
topic: "Common semantic patterns that suggest skills tooling code may be rebuilding existing dependency capabilities"
anchors:
  - target: "TOOLING_REMEDIATION_PROTOCOL.md"
    relation: "implements"
    direction: "upstream"
    reason: "The remediation protocol can route detailed pattern examples into this dedicated atom."
  - target: "MANDATORY_TECHSTACK_BASELINE.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Pattern recognition depends on the current mandatory baseline."
---

# Common Redundant Wheel Patterns

## 本地目的
- 提供“哪些代码形态常常意味着重复造轮子”的稳定例子，减少每次 review 都靠临场措辞重述。

## 当前边界
- 本文只列常见模式，不直接授权自动替换。
- 是否真的进入修正，仍由 `TOOLING_REMEDIATION_PROTOCOL.md` 决定。

## 常见模式
- 手写 JSON / YAML shape 校验，而 repo 已有 `jsonschema`、`pydantic` 或 `PyYAML` 可以直接承接。
- 手写 frontmatter / markdown tokenizer，而 repo 已有 `python-frontmatter`、`gray-matter`、`markdown-it` 或 `markdown-it-py`。
- 手写 CLI argument plumbing / terminal rendering，而目标用途已经适合 `typer` / `rich`。
- 手写 watcher / HTTP helper，而语义已落在 `watchfiles` / `httpx`。
- 前端 tooling 中手写 schema guard、markdown parser、lint glue，而 `ajv`、`zod`、`markdown-it`、`markdownlint-cli2`、`eslint` 组合已足够表达。
- 工具代码将 runtime 日志、调试文件或审计痕迹散落到技能目录、repo 任意子目录或 home 临时路径，而没有显式收敛到 `/home/jasontan656/AI_Projects/Codex_Skill_Runtime`。
- 工具代码把默认结果、抓取内容或生成文件直接写入当前工作目录、技能目录或隐式 cache 目录，而没有显式收敛到 `/home/jasontan656/AI_Projects/Codex_Skills_Result`，也没有给定向产物暴露明确落点参数。
- 技能文档完全不说明日志落点与产物落点，导致只有读源码才能知道文件会写去哪里。
- 技能已经产生历史日志或产物，但修正只准备改未来代码，不准备纳入已有文件迁移或处置策略。

## 使用提醒
- 模式命中只是“怀疑”，不是结论。
- 只有当输入输出语义、异常路径、兼容要求和调用方预期都对齐时，才可推进替换。
