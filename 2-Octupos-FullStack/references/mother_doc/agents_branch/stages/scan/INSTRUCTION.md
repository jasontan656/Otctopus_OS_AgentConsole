# AGENTS Scan

- 先执行 `mother-doc-agents-contract`。
- 再执行 `mother-doc-agents-directive --stage scan`。
- 扫描 3 类路径中的 `AGENTS.md`：`Octopus_OS/AGENTS.md`、`Octopus_OS/<Container>/AGENTS.md`、`Octopus_OS/Mother_Doc/docs/**/AGENTS.md`。
- 只检查存在性、配套文件和层级入口，不回写正文。
