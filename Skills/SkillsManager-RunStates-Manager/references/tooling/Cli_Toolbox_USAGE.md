---
doc_id: skillsmanager_runstates_manager.references.tooling.cli_toolbox_usage
doc_type: topic_atom
topic: CLI usage for SkillsManager-RunStates-Manager
---

# Cli_Toolbox Usage

## Read contract

```bash
python3 ./scripts/Cli_Toolbox.py contract --json
```

## Inspect governed type

```bash
python3 ./scripts/Cli_Toolbox.py inspect \
  --target-skill-root Skills/SkillsManager-GovTargetSkill \
  --json
```

## Scaffold runstate assets

```bash
python3 ./scripts/Cli_Toolbox.py scaffold \
  --target-skill-root Skills/SkillsManager-GovTargetSkill \
  --governed-type auto \
  --json
```

## Audit runstate readiness

```bash
python3 ./scripts/Cli_Toolbox.py audit \
  --target-skill-root Skills/SkillsManager-GovTargetSkill \
  --json
```
