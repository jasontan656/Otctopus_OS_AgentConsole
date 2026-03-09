# AGENTS/README Scan

- 先执行 `mother-doc-agents-contract`。
- 再执行 `mother-doc-agents-directive --stage scan`。
- 扫描 3 类路径中的 `AGENTS.md + README.md`：`Octopus_OS/AGENTS.md + README.md`、`Octopus_OS/<Container>/AGENTS.md + README.md`、`Octopus_OS/Mother_Doc/docs/**/AGENTS.md + README.md`。
- 只检查存在性、配套文件、模板映射和层级入口，不回写普通正文。
