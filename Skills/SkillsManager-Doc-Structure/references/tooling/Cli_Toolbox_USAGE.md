---
doc_id: skillsmanager_doc_structure.references.tooling.cli_toolbox_usage
doc_type: topic_atom
topic: CLI usage for SkillsManager-Doc-Structure
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: Tool usage is part of the governed runtime surface.
---

# Cli_Toolbox Usage

## Inspect a target
```bash
python3 ./scripts/Cli_Toolbox.py inspect --target /path/to/skill --json
```

## Lint a target
```bash
python3 ./scripts/Cli_Toolbox.py lint --target /path/to/skill --json
```

## Compile workflow context
```bash
python3 ./scripts/Cli_Toolbox.py compile-context \
  --target /path/to/skill \
  --entry development_loop \
  --selection primary_step \
  --json
```
