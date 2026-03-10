# Scan Workflow

1. Load the active scan rule assets.
2. Match governed files by exact filename rules and optional keyword rules.
3. Apply the disallowed path list.
4. Produce a human-reviewable managed target list.
5. Lint every discovered managed file against its structure template.
6. Output either stdout or a json result file under the corresponding `Codex_Skill_Runtime` folder.
