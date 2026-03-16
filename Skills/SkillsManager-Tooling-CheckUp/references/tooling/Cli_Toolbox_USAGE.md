---
doc_id: skillsmanager_tooling_checkup.references.tooling.cli_toolbox_usage
doc_type: topic_atom
topic: CLI usage for SkillsManager-Tooling-CheckUp
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: Tool usage is part of the governed runtime surface.
---

# Cli_Toolbox Usage

## Read runtime contract
```bash
python3 ./scripts/Cli_Toolbox.py contract --json
```

## Audit a target skill
```bash
python3 ./scripts/Cli_Toolbox.py audit \
  --target-skill-root /path/to/skill \
  --json
```
