# Scan Instruction

> Audit copy generated from `references/stages/scan/DIRECTIVE.json`.
> Runtime models must call `python3 scripts/Cli_Toolbox.py directive --stage scan --json` instead of reading this markdown for guidance.

- 只处理 scan 阶段。
- 运行态只允许通过 Cli_Toolbox.directive 读取本阶段 machine-readable 指引。
- 禁止把 references/stages/scan/*.md 当作运行规则源，除非用户显式要求审计 markdown。
- 输出目标固定为 assets/managed_targets/scan_report.json。
